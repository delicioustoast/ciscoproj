import urllib, json

# this function outputs the reddit traffic stats in JSON format
def pullStats(subreddit):
    url = "https://www.reddit.com/r/" + subreddit + "/about/traffic.json"
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    return data