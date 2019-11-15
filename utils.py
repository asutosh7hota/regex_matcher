import re
import json
import argparse
import asyncio
import aiohttp

"""
This script has all the utilities functions for the regex matcher.
"""

# Setup arguments for command line input


def parse_args(args):
    """
    Takes in arguments for running the url_regex_matcher.py file.
    :type args: list
    :param args: A list of filepath and interval
    Filepath: Absolute path of the file
    Interval: Time at which the scheduler periodically runs the regex checks
    """
    ap = argparse.ArgumentParser()
    ap.add_argument('-f', '--filename', type=str,
                    help='Add the file path of input data', default='./datasets/data.json')
    ap.add_argument(
        '-i', '--interval', type=int,
        help='Time interval for scheduler in seconds (Default: 100 secs)',
        default=100)
    return ap.parse_args()


# Load the json dataset and return a dictionary
def load_dataset(filepath):
    """
    Load the dataset (JSON) from directory
    :type filepath: string
    :param filepath: Absolute path of the file
    """
    with open(filepath, 'r') as fp:
        data = json.load(fp)
    return data

# Gather all the URLS from the dictionary
async def gather_urls(urls):
    """
    Creates a collection of URLs to be fetched assynchronously and fetches the content by
    calling the fetch method.
    :type urls: list or iterator of a dict.keys()
    :param urls: Can take a list of urls or a collection of all the keys in a python dict.
    """
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        return await asyncio.gather(*tasks)

# Fetch the content for each URL, return empty strings if invalid URL
async def fetch(session, url):
    """
    Asynchronously fetches the content of a list of URLs
    :type session: aiohttp.ClientSession()
    :param session: asyncio session event
    :type url: string
    :param url: A URL
    """
    try:
        async with session.get(url) as response:
            return await response.text()
    except:
        print('Error in Connection, Re-check Internet Connection or URL')
        return ''

# Traverse through the input data and find the matches for each URL and REGEX
def regex_matcher(filepath):
    """
    Get the data from dictionary and return a output dictionary with regex matches
    for every url and corresponding REGEX
    :type filepath: string
    :param filepath: Absolute path of the input JSON file
    """
    data = load_dataset(filepath)
    urls = data.keys()
    loop = asyncio.get_event_loop()
    fetched_content = loop.run_until_complete(gather_urls(urls))
    output_dict = {}
    for idx, url in enumerate(data):
        matches = {}
        for regex in data[url]:
            matches[regex] = re.findall(regex, fetched_content[idx])
        output_dict[url] = matches
    return output_dict

# Save the matched content with the given regex for each url
def save_output(data, time):
    """
    Gets the output dictionary and saves the output with a timestamp
    :type data: dict
    :param data: Output dictionary with regex matches for every url and corresponding REGEX
    :type time: string
    :param time: Timestamp with date and time
    """
    with open('./out_' + time + '.json', 'w') as fp:
        json.dump(data, fp)


# Function to be used by scheduler to repeat tasks continuously till exit by user
def run(filepath, time):
    """
    Util function used to schedule the whole process periodically,
    Runs the different util functions to input, process and save
    output JSON file
    :type filepath: string
    :param filepath: Absolute path of the input JSON file
    :type time: string
    :param time: Timestamp with date and time
    """
    result = regex_matcher(filepath)
    save_output(result, time)
    