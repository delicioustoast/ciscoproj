import urllib, json
from datetime import datetime
from numpy import median
import time

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
Converts epoch time to day of week
"""
def ep_to_day(ep):
    return time.strftime("%A", time.gmtime(ep))

"""
Returns the median number of pageviews of each day of week as a dictionary
"""
def day_stats(day_list):
    days_views = {
            'Sunday':[],
            'Monday':[],
            'Tuesday':[],
            'Wednesday':[],
            'Thursday':[],
            'Friday':[],
            'Saturday':[]
        }
    days_median = dict.fromkeys(days_views.keys())
    for epoch_time, unique_visitors, pageviews, subscribers in day_list:
        day_of_week = ep_to_day(epoch_time)
        days_views[day_of_week].append(pageviews)
    for day, pageviews_list in days_views.iteritems():
        days_median[day] = int(median(pageviews_list))
    return days_median