from flask import Flask, request, url_for, render_template, redirect, flash
import models
from datetime import datetime
import praw
# import urllib, json
app = Flask(__name__)

@app.route('/')
def hello_person():
    return render_template('results.html', showGraph=False)

@app.route('/analysis', methods=['POST'])
def analysis():
    error = None

    if request.form["subreddit"] == "":
        error = "Please enter a subreddit."
        return render_template('results.html', showGraph=False, error=error)

    try:
        subreddit_data = models.pull_stats(request.form["subreddit"])
    except (praw.errors.NotFound, praw.errors.InvalidSubreddit):
        error = "Could not retrieve data."
        return render_template('results.html', showGraph=False, error=error)

    daychart_info, best_day = models.get_stats(subreddit_data["day"], "day")
    hourchart_info, best_hour = models.get_stats(subreddit_data["hour"], "hour")
    best_hour = datetime.strptime(best_hour, "%H").strftime("%I %p")

    top_subreddits = models.get_top_subreddits(10)

    should_analyze_words = request.form.getlist('check') 
    top_words = None
    if should_analyze_words:
        top_words = models.get_top_words(request.form["subreddit"], 5)

    return render_template('results.html', subreddit=request.form["subreddit"], 
        daychartInfo=daychart_info, hourchartInfo=hourchart_info, bestDay=best_day, bestHour=best_hour, showGraph=True,
        topSubreddits=top_subreddits, topWords=top_words)

#TODO: remove app.debug?
#TODO: add readme
if __name__ == '__main__':
    app.debug = True
    app.secret_key = "It's a secret"
    app.run()