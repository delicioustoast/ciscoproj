import urllib, json
from datetime import datetime
from numpy import median
import time
from collections import defaultdict

"""
Outputs the subreddit traffic stats in JSON format
The arrays in the "days" array is laid out like: [epoch time, uniques, pageviews, subscriptions]
The arrays in both the "hours" and "months" arrays are laid out like: [epoch time, uniques, pageviews]
"""
def pull_stats(subreddit):
    url = "https://www.reddit.com/r/" + subreddit + "/about/traffic.json"
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    
    return data

"""
Converts epoch time to day of week or hour
"""
def get_time(ep, time_type):
    time_dict = {
        "day": "%A",
        "hour": "%H"
    }

    return time.strftime(time_dict[time_type], time.gmtime(ep))

"""
Returns the median number of pageviews of each day of week as a dictionary
"""
def get_stats(views_list, time_type):
    all_pageviews = defaultdict(lambda: [], {})

    for i in views_list:
        i_time = get_time(i[0], time_type)
        all_pageviews[i_time].append(i[2])

    median_pageviews = dict.fromkeys(all_pageviews.keys())
    for i_time, pageviews_list in all_pageviews.iteritems():
        median_pageviews[i_time] = int(median(pageviews_list))

    return median_pageviews
