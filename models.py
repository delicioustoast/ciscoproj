# import urllib, json
from datetime import datetime
from numpy import median
import time
from collections import defaultdict
import praw
import re

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

"""
Updates word_dict based on words in word_list, excluding any words in the blacklist
"""
def note_words(word_list, word_dict, blacklist):
    for word in word_list:
        processed_word = re.sub(ur"[^\w\d'\s]+",'',word).lower()
        if processed_word not in blacklist and processed_word != "":
            word_dict[processed_word] += 1

"""
gets most frequent words of positive score posts and return a dictionary containing these words and their frequencies
"""
def get_top_words(subreddit, posts):
    good_words = defaultdict(lambda: 0, {})
    common_words = set(line.strip() for line in open('common-words.txt'))
    r = praw.Reddit(user_agent='DT Subreddit Activity Application')
    subreddit = r.get_subreddit(subreddit)
    top = subreddit.get_top(params={'t': 'all'}, limit=posts) # For a more potentially accurate set of top comments, increase the limit (but it'll take longer)
    all_comments = []
    for submission in top: 
        submission_comments = praw.helpers.flatten_tree(submission.comments)
        #don't include non comment objects such as "morecomments"
        real_comments = [comment for comment in submission_comments if isinstance(comment, praw.objects.Comment)]
        all_comments += real_comments

    all_comments.sort(key=lambda comment: comment.score, reverse=True)

    top_comments = all_comments[:25] #top 25 comments
    for comment in top_comments:
        if comment.score > 0:
            comment_text = comment.body.split()
            note_words(comment_text, good_words, common_words)

    return sorted(good_words.iteritems(), key=lambda (k, v): (-v, k))[:10]
