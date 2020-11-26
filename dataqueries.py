BUFF = 1024 #buffer size

def register_new_user(db_conn, username, password):
    #TODO add new user to database
    return

def check_user_pass(db_conn, username, password):
    change_status = "UPDATE users SET is_online = 1 WHERE username = {} AND password = {}".format(username,password)
    try:
        execute_query(db_conn,change_status)
        return True
    except:
        return False

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

def logout(db_conn, user):
    return