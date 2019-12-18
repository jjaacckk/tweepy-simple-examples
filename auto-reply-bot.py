import tweepy, string, time, math

"""enter your own consumer key, consumer secret, access key, and access secret"""
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_KEY = ''
ACCESS_SECRET = ''


auth= tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)


def get_user_likes_avg(user_name):
    """returns the average number of user likes for up to 60 tweets"""
    f_create = open('replied.txt', 'w+')
    f_create.close()
    tweetId_list = []
    last = 0
    likes_sum = 0
    tweet_count = api.get_user(user_name).statuses_count
    for status in api.user_timeline(screen_name = user_name, include_rts = False):
        tweetId_list.append(status.id)
        likes_sum += api.get_status(status.id).__dict__['favorite_count']
        
    if api.get_user(user_name).statuses_count > 20:
        for status in api.user_timeline(screen_name = user_name, max_id = tweetId_list[-1], include_rts = False):
            tweetId_list.append(status.id)
            likes_sum += api.get_status(status.id).__dict__['favorite_count']
            
    if api.get_user(user_name).statuses_count > 40:
        for status in api.user_timeline(screen_name = user_name, max_id = tweetId_list[-1], include_rts = False):
            tweetId_list.append(status.id)
            likes_sum += api.get_status(status.id).__dict__['favorite_count']
    
    tweetId_list = list(dict.fromkeys(tweetId_list))

    likes_avg = float(likes_sum) / float(len(tweetId_list))
    return '{:.2f}'.format(likes_avg)



def get_past_tweet_num(user_name):
    """returns list of mentions"""
    tweetId_list = []
    last = 0
    tweet_count = api.get_user(user_name).statuses_count
    for status in api.user_timeline(screen_name = user_name, include_rts = False):
        tweetId_list.append(status.id)
    return len(tweetId_list)



def mentions_reply():
    """automatically replies to a tweet mentioning your twitter"""
    mentions = api.mentions_timeline()
    if bool(mentions):
        for i in mentions:
            dict_mentions = i.__dict__
            tweet_id = dict_mentions['id_str']
            f_read = open('replied.txt', 'r')
            if f_read.mode == 'r':
                id_contents = f_read.readlines()
                tweet_id_check = tweet_id + '\n'
                if tweet_id_check not in id_contents:
                    f_read.close()
                    
                    tweet_text = dict_mentions['text'].encode("utf-8")
                    tweet_user_dict = dict_mentions['user'].__dict__
                    tweet_user_follower_count = tweet_user_dict['followers_count']
                    tweet_user_name = tweet_user_dict['screen_name']
                    tweet_text = tweet_text.decode("utf-8")
                    tweet_text = tweet_text.replace("@[your twitter] ", "")
                    avg_likes = get_user_likes_avg(tweet_user_name)
                    user_tweet_count = get_past_tweet_num(tweet_user_name)
                    
                    
                    f_write = open('replied.txt', 'a')
                    f_write.write('{}\n'.format(tweet_id))
                    f_write.close()
                    try: 
                        api.update_status("@[your twitter] tweeted \"@{} out of the past {} tweets, you have had an average of {} likes. You currently have {} followers.\"".format(tweet_user_name, user_tweet_count, avg_likes, tweet_user_follower_count), tweet_id)
                        
                        print("@[your twitter] tweeted \"@{} out of the past {} tweets, you have had an average of {} likes. You currently have {} followers.\"".format(tweet_user_name, user_tweet_count, avg_likes, tweet_user_follower_count))

                    except tweepy.TweepError as e:
                        print(e.reason)
                else:
                    f_read.close()
                    print("tweet has been replied to")
    else:
        print("no mentions")

        

while True:
    """checks for tweets every 2 minutes"""
    try:
        mentions_reply()
    except tweepy.TweepError as e:
        print(e.reason)
        
    time.sleep(120)