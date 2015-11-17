from flask import Flask, request, url_for, render_template, redirect, flash
import models
import urllib, json
app = Flask(__name__)

@app.route('/')
def hello_person():
    return """
        <p>What subreddit do you want to analyze?</p>
        <form method="POST" action="%s"><input name="subreddit" /><input type="submit" value="Go!" /></form>
        """ % (url_for('greet'),)

#TODO: error handling for nonexistent subreddit
@app.route('/greet', methods=['POST'])
def greet():
    subreddit_data = models.pull_stats(request.form["subreddit"])
    daychart_info = models.get_stats(subreddit_data["day"], "day")
    hourchart_info = models.get_stats(subreddit_data["hour"], "hour")
    # return """
    #     <p>%s</p>
    #     <p><a href="%s">Back to start</a></p>
    #     """ % (greeting, url_for('hello_person'))
    return render_template('results.html', subreddit=request.form["subreddit"], daychartInfo=daychart_info, hourchartInfo=hourchart_info)

#TODO: remove app.debug?
if __name__ == '__main__':
    app.debug = True
    app.run()