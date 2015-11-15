from flask import Flask, request, url_for
import models
import urllib, json
app = Flask(__name__)

@app.route('/')
def hello_person():
    return """
        <p>Who do you want me to say "Hi" to?</p>
        <form method="POST" action="%s"><input name="subreddit" /><input type="submit" value="Go!" /></form>
        """ % (url_for('greet'),)

@app.route('/greet', methods=['POST'])
def greet():
    greeting = models.pullStats(request.form["subreddit"])
    # url = "https://www.reddit.com/r/personalfinance/about/traffic.json"
    # response = urllib.urlopen(url)
    # data = json.loads(response.read())
    # data = json.dumps(data)
    return """
        <p>%s</p>
        <p><a href="%s">Back to start</a></p>
        """ % (greeting, url_for('hello_person'))

if __name__ == '__main__':
    app.debug = True
    app.run()