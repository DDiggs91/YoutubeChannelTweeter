from bs4 import BeautifulSoup
import requests
import twitter
import datetime

base = 'https://www.youtube.com/user/Northernlion/videos?view=57&flow=grid'
r = requests.get(base)
page = r.text
soup = BeautifulSoup(page, 'html.parser')

videos = soup.find('h3', attrs={'class': 'yt-lockup-title'})

watch_title = videos.contents[0]['title']
watch_link = videos.contents[0]['href']

tweet_text = watch_title + ': https://www.youtube.com' + watch_link + ' via @Youtube'

with open('data//logs.txt', 'r') as f:
    most_recent_attempt = f.readlines()[-1]

with open('data//previous_tweet.txt', 'w+') as f:
    if f != tweet_text:
        new_tweet = True
        f.seek(0)
        f.truncate()
        f.write(tweet_text)
    else:
        new_tweet = False
        with open('data//logs.txt', 'a') as fh:
            fh.write('\nYour most recent YT video has not updated since the last check')
            fh.write(datetime.datetime.strftime(datetime.datetime.now(), ', %c'))

with open('twitter_keys.txt') as f:
    twitter_keys = []
    for line in f:
        twitter_keys.append(line.rstrip())
api = twitter.Api(consumer_key=twitter_keys[0],
                  consumer_secret=twitter_keys[1],
                  access_token_key=twitter_keys[2],
                  access_token_secret=twitter_keys[3])

try:
    status = api.PostUpdate(tweet_text, )
    with open('data//logs.txt', 'a') as f:
        f.write('\nThe following message was tweeted : ' + tweet_text)
        f.write(datetime.datetime.strftime(datetime.datetime.now(), ', %c'))
except UnicodeDecodeError:
    with open('data//logs.txt', 'a') as f:
        f.write('\nYour message could not be encoded.  Perhaps it contains non-ASCII characters?')
        f.write(datetime.datetime.strftime(datetime.datetime.now(), ', %c'))
except twitter.error.TwitterError:
    with open('data//logs.txt', 'a') as f:
        f.write('\nYour tweet was too long to be tweeted. Long title?')
        f.write(datetime.datetime.strftime(datetime.datetime.now(), ', %c'))
