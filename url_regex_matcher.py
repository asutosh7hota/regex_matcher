import time
import sched
import sys
import utils

if __name__ == '__main__':
    """Task: To process a group of URL and their specified Regex (s) for each URL
    and match all the specified regex (s) for a URL to the content (HTML) of each URL
    Usage: python url_regex_matcher.py -f <filename> -i <interval>
    Example:
    python url_regex_matcher.py -f ./datasets/data.json -i 150
    :type filename: string
    :param filename: Absolute path to the data file (JSON)
    :type interval: int
    :param interval: Time(in seconds) at which the scheduler periodically runs the regex
    checks"""
    # Input the filename and schedule interval,
    # script checks the data again after every interval and saves output file with timestamp
    Args = utils.parse_args(sys.argv[1:])

    # Initialise scheduler
    Sched = sched.scheduler(time.time, time.sleep)
    # Run the function until keyboard interrupt
    try:
        # Run the check first time, then repeat periodically
        Sched.enter(1, 1, utils.run,
                           (Args.filename,
                            str(time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime()))))
        interval = Args.interval
        print(
            f'Scheduler Mode: Fetching and Matching every {interval} secs ')
        while True:
            # Execute the scheduler periodically until keyboard interrupt by user
            Sched.enter(interval, 1, utils.run,
                               (Args.filename,
                                str(time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime()))))
            Sched.run(blocking=True)
    except KeyboardInterrupt as e:
        print(' Stopped by the user.')
        