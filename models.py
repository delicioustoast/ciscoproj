# import urllib, json
from datetime import datetime
from numpy import median
import time
from collections import defaultdict
import praw

"""
Outputs the subreddit traffic stats in JSON format
The arrays in the "days" array is laid out like: [epoch time, uniques, pageviews, subscriptions]
The arrays in both the "hours" and "months" arrays are laid out like: [epoch time, uniques, pageviews]
"""
def pull_stats(subreddit):
    url = "https://www.reddit.com/r/" + subreddit + "/about/traffic.json"
    r = praw.Reddit(user_agent='DT Subreddit Activity Application')
    data = r.request_json(url)
    
    return data

"""
Converts epoch time to day of week or hour (in PST)
"""
def get_time(ep, time_type):
    pst_offset = 3600*8 # the difference between GMT and PST is -8 hours
    time_dict = {
        "day": "%A",
        "hour": "%H"
    }

    return time.strftime(time_dict[time_type], time.gmtime(ep - pst_offset))

"""
Returns the median number of pageviews as a dictionary and the highest median value as a string
"""
def get_stats(views_list, time_type):
    all_pageviews = defaultdict(lambda: [], {})

    for i in views_list:
        i_time = get_time(i[0], time_type)
        all_pageviews[i_time].append(i[2])

    median_pageviews = dict.fromkeys(all_pageviews.keys())
    for i_time, pageviews_list in all_pageviews.iteritems():
        median_pageviews[i_time] = int(median(pageviews_list))

    return median_pageviews, max(median_pageviews.keys(), key=(lambda k: median_pageviews[k]))
"""
Returns n most active subreddits
"""
def get_top_subreddits(n):
    subreddit_list = []
    r = praw.Reddit(user_agent='DT Subreddit Activity Application')
    popular_subreddits = r.get_popular_subreddits(limit=n)
    for subreddit in popular_subreddits:
        subreddit_list.append(subreddit)
    return subreddit_list