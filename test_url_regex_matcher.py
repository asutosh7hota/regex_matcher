import asyncio
import utils

# Empty dataset
result_1 = {}

# URL groups with empty regex list to match
result_2 = {"https://www.youtube.com/": {}, "https://www.google.com/": {}}

# Ideal dataset: URLS + regex strings
result_3 = {"https://www.youtube.com/": {"^a...s$": [], "(<div class=\"deg\">.*?</div>)": []}}

class TestClass:

    """
    Checks base cases and edge cases for util functions

    """

    # Check base case for argparse
    def test_base_argparse(self):
        """
        Test 1: Checks the base case of argparse python.

        If the regex_matcher.py script is run withot any
        arguments, the defalt values shall load.

        Example: python url_regex_matcher.py

        Default filepath: './datasets/data.json' |
        Default interval (secs):  100

        """
        args = []
        parser = utils.parse_args(args)
        assert parser.filename == './datasets/data.json'
        assert parser.interval == 100
    # Test different input data to evaluate the regex_matcher
    def test_regex_matcher(self):

        """
        Test corner cases for regex_matcher.py with different kind of inputs
        test 1: Input- Empty JSON file |
        test 2: Input- Group list of URLs with empty regex values to match |
        test 3: Input- URLs with regex but no successful matches

        """

        # Input data: Empty JSON file
        test_1 = utils.regex_matcher('./datasets/data_1.json')
        # Input data: Valid URLs but empty REGEX values
        test_2 = utils.regex_matcher('./datasets/data_2.json')
        # Input data with no REGEX matches
        test_3 = utils.regex_matcher('./datasets/data_3.json')

        assert test_1 == result_1
        assert test_2 == result_2
        assert test_3 == result_3

    def test_fetch(self):

        """
        Testing the Asynchronous Fetch function
        loop1: Empty URL list |
        loop2: Invalid group of URLs |
        loop3: Mixture of vaid and invalid URLs
        """


        # Demo data for testing
        # Fetching empty urls
        data_1 = utils.load_dataset('./datasets/data_1.json')
        # Fetching Invalid URLS
        data_2 = {
            
            "https://www.youtub479749274927e.com/": [],
            "https://www.goog893749374le.com/": []
                }
        # Fetching a group of invalid and valid URLS:
        data_3 = {
            "https://www.youtub479749274927e.com/": [],
            "http://python.org": ["(<div class=\"deg\">.*?</div>)"],
            "http://google.com": ["(<div class=\"deg\">.*?</div>)"]
                }

        loop_1 = asyncio.get_event_loop()
        fetched_content_1 = loop_1.run_until_complete(utils.gather_urls(data_1.keys()))
        # Fetch returns no value
        assert fetched_content_1 == []
        # Fetch returns empty strings for each invalid url
        loop_2 = asyncio.get_event_loop()
        fetched_content_2 = loop_2.run_until_complete(utils.gather_urls(data_2.keys()))
        assert fetched_content_2 == ['', '']
        # Fetch returns empty string for invalid URL and content (str) for valid urls
        loop_3 = asyncio.get_event_loop()
        fetched_content_3 = loop_3.run_until_complete(utils.gather_urls(data_3.keys()))
        assert fetched_content_3[0] == ''
        assert len(fetched_content_3) == 3
