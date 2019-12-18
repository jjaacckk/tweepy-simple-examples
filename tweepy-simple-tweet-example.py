import tweepy, sys

"""enter your consumer key, consumer secret, access key, and access secret"""
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_KEY = ''
ACCESS_SECRET = ''

auth= tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

def tweetFunc(tweet):
    try:
        api.update_status(tweet)
        
    except tweepy.TweepError as e:
        print(e.reason)

tweetFunc(sys.argv[1])
