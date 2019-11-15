# regex_matcher

## Description

It is python application which matches the content of a group of URLs to specified REGEX strings asynchronously and efficienty.

Input- Takes in a JSON file with the following structure:

```

{
'URL': ['regex1', 'regex2'.....]
}

```
Example:

```
{
  
  "http://python.org": ["<[^/>]+/>"],
  "https://www.youtube.com/": ["^a...s$","(<div class=\"deg\">.*?</div>)"],
  "https://www.google.com/": ["</[^/>]+>"]

}

```
Output- Returns a JSON file with matched content of each URL and REGEX

```

{

    'URL': {
            'REGEX': [matched content values]

            }
}

```

## Design Decisions:

1. I used standard python libraries for this task and used asyncio and aiohttp for IO operations (fetching url's content)

Why: In this task, there could be network latency in getting the content of the URLs and hence, I chose to go the async way.
Other operations (matching regex) can be efficiently performed on the system.

2. I/O: I used command line arguments (argparse) so that the user could specify the input files and the periodicity.

3. The data of each timestamp is stored in a separate file, with the timestamp embedded in the filename. I did'nt setup a 
database considering this to be a demo task.

4. Pytest: I used pytest to test few corner cases of the utils function.

5. Sphinx: To autogenerate documentation for the utils and test file.



## Setting up Environment (Installation):


```
pip install pipenv
pipenv install
pipenv shell
```
This should create a pip environment and install all dependencies in your system


## Usage

To run the code: 

python url_regex_matcher.py -f <filenpath> -i <interval(in seconds)>

Example: 
```
python url_regex_matcher.py -f ./datasets/data.json -i 150

```


## Testing:

```
pytest

```

## Documentation

The documentation is automatically generated by Sphinx. To read it, type:

```
firefox docs/_build/html/index.html
```

