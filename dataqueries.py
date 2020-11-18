BUFF = 1024 #buffer size

def register_new_user(db_conn, username, password):
    #TODO add new user to database
    return

def check_user_pass(db_conn, username, password):
    #TODO check username exists and password matches
    # return true if all correct
    return

def check_user_exists(db_conn, username):
    #TODO check if username taken already
    # return true if username taken
    return

def get_trending_hashtags(db_conn):
    #TODO get top 5 trending hashtags as a list
    hashtags = []
    return hashtags

def get_tweets_by_hashtag(db_conn, hashtag):
    #TODO return a list of max 10 recent tweets with input hashtag
    tweets = []
    return tweets

def mark_user_online(db_conn, user):
    return

def mark_user_offline(db_conn, user):
    return