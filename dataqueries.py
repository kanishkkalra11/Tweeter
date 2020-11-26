from datetime import datetime
import re

BUFF = 1024 #buffer size
DISPLAY_TWEETS = 10 #Number of tweets to display on CLI

def execute_query(connection, query):
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    # print("Query successful")
    # except Error as err:
    #     print(f"Error: '{err}'")
    return

def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    # try:
    cursor.execute(query)
    result = cursor.fetchall()
    return result
    # except Error as err:
        # print(f"Error: '{err}'")

def register_new_user(db_conn, username, password):
    insert_user = "INSERT INTO users VALUES ({}, {}, NULL, NULL, 1, NULL, NULL, NULL)".format(username,password)
    try:
        execute_query(db_conn, insert_user)
        return True
    except:
        return False

def check_user_pass(db_conn, username, password):
    change_status = "UPDATE users SET is_online = 1 WHERE username = {} AND password = {}".format(username,password)
    try:
        execute_query(db_conn,change_status)
        return True
    except:
        return False

def check_user_exists(db_conn, username):
    check_query = "SELECT * FROM users WHERE username = {}".format(username)
    results = read_query(db_conn, check_query)
    a = len(results)
    if a==0:
        return False
    else:
        return True

def get_trending_hashtags(db_conn):
    retrieve_tags = "SELECT hashtag FROM hashtags ORDER BY count DESC LIMIT 5"
    results = read_query(db_conn, retrieve_tags)
    hashtags = []
    for result in results:
        hashtags.append(result[0])
    return hashtags

def get_tweets_by_hashtag(db_conn, hashtag):
    get_tweet_ids = "SELECT tweet_ids FROM hashtags WHERE hashtag = {}".format(hashtag)
    results = read_query(db_conn, get_tweet_ids)
    for result in results:
        result = list(result)
    ids = result[1]
    ids = list(map(int, ids.split(',')))
    get_tweets = "SELECT * FROM tweets WHERE tweet_id IN {}".format(ids)
    results = read_query(db_conn, get_tweets)
    retr = []
    for result in results:
        result = list(result)
        a = result[4]
        b = list(a.split())
        c = list(map(int,b[0].split('-')))
        d = list(b[1].split('.'))
        c = c + list(map(int,d[0].split(':')))
        c.append(int(d[1]))
        e = datetime(c[0],c[1],c[2],c[3],c[4],c[5],c[6])
        result[4] = e
        if result[5]==1:
            mm = read_query(db_conn,"SELECT * FROM tweets WHERE tweet_id = {}".format(result[6]))
            for m in mm:
                m = list(m)
                break
            result = result + m
        retr.append(result)
    retr.sort(key = lambda x:(x[4]),reverse=True)
    if len(retr)>DISPLAY_TWEETS:
        retr = retr[:DISPLAY_TWEETS]
    return retr
    # format => list of tweets, for each tweet => tweet_id, tweet, username, hashtags, timestamp, is_retweet, retweet_id

def logout(db_conn, username):
    change_status = "UPDATE users SET is_online = 0 WHERE username = {}".format(username)
    execute_query(db_conn,change_status)
    return

def get_tweets_of_user(db_conn, username):
    get_tweet_ids = "SELECT * FROM users WHERE username = {}".format(username)
    results = read_query(db_conn, get_tweet_ids)
    for result in results:
        result = list(result)
    ids = result[5]
    ids = list(map(int, ids.split(',')))
    get_tweets = "SELECT * FROM tweets WHERE tweet_id IN {}".format(ids)
    results = read_query(db_conn, get_tweets)
    retr = []
    for result in results:
        result = list(result)
        a = result[4]
        b = list(a.split())
        c = list(map(int,b[0].split('-')))
        d = list(b[1].split('.'))
        c = c + list(map(int,d[0].split(':')))
        c.append(int(d[1]))
        e = datetime(c[0],c[1],c[2],c[3],c[4],c[5],c[6])
        result[4] = e
        if result[5] == 1:
            mm = read_query(db_conn,"SELECT * FROM tweets WHERE tweet_id = {}".format(result[6]))
            for m in mm:
                m = list(m)
                break
            result = result + m
        retr.append(result)
    retr.sort(key = lambda x:(x[4]),reverse=True)
    if len(retr)>DISPLAY_TWEETS:
        retr = retr[:DISPLAY_TWEETS]
    return retr
    # format => list of tweets, for each tweet => tweet_id, tweet, username, hashtags, timestamp, is_retweet, retweet_id

def get_follow_update(db_conn,username1,username2):
#username1 - me
#username2 - other person
#return format - bool(i follow him), bool(he follows me)
    ret1 = True
    ret2 = True
    results = read_query(db_conn, "SELECT * FROM users WHERE username = {}".format(username1))
    for result in results:
        result = list(result)
        break
    followers = result[2]
    following = result[3]
    try:
        l = len(username2)
        m = len(followers)
        for i in range(m):
            if followers[i:i+l] == username2:
                break
    except:
        ret2 = False
    try:
        l = len(username2)
        m = len(following)
        for i in range(m):
            if following[i:i+l] == username2:
                break
    except:
        ret1 = False
    return ret1,ret2

def get_followers_list(db_conn,username):
    retr = "SELECT followers FROM users WHERE username = {}".format(username)
    results = read_query(db_conn, retr)
    for result in results:
        result = list(result)
        break
    result = str(result[2])
    followers = result.split(',')
    online_followers = []
    offline_followers = []
    for follower in followers:
        results = read_query(db_conn,"SELECT * FROM users WHERE username = {}".format(follower))
        for result in results:
            result = list(result)
            if result[4] == 0:
                offline_followers.append(follower)
            else:
                online_followers.append(follower)
            break
    return online_followers,offline_followers

def get_following_list(db_conn,username):
    retr = "SELECT following FROM users WHERE username = {}".format(username)
    results = read_query(db_conn, retr)
    for result in results:
        result = list(result)
        break
    result = str(results[3])
    following = result.split(',')
    online_following = []
    offline_following = []
    for person in following:
        results = read_query(db_conn,"SELECT * FROM users WHERE username = {}".format(username))
        for result in results:
            result = list(result)
            if result[4] == 0:
                offline_following.append(person)
            else:
                online_following.append(person)
            break
    return online_following,offline_following

def get_pinned_tweets_of_user(db_conn,username):
    get_tweet_ids = "SELECT * FROM users WHERE username = {}".format(username)
    results = read_query(db_conn, get_tweet_ids)
    for result in results:
        result = list(result)
    ids = result[7]
    ids = list(map(int, ids.split(',')))
    get_tweets = "SELECT * FROM tweets WHERE tweet_id IN {}".format(ids)
    results = read_query(db_conn, get_tweets)
    retr = []
    for result in results:
        result = list(result)
        a = result[4]
        b = list(a.split())
        c = list(map(int,b[0].split('-')))
        d = list(b[1].split('.'))
        c = c + list(map(int,d[0].split(':')))
        c.append(int(d[1]))
        e = datetime(c[0],c[1],c[2],c[3],c[4],c[5],c[6])
        result[4] = e
        if result[5] == 1:
            mm = read_query(db_conn,"SELECT * FROM tweets WHERE tweet_id = {}".format(result[6]))
            for m in mm:
                m = list(m)
                break
            result = result + m
        retr.append(result)
    retr.sort(key = lambda x:(x[4]),reverse=True)
    return retr
    # format => list of tweets, for each tweet => tweet_id, tweet, username, hashtags, timestamp, is_retweet, retweet_id

def pin_new_tweet(db_conn,username,tweet_id):
    results = read_query(db_conn,"SELECT * FROM users WHERE username = {}".format(username))
    for result in results:
        result = list(result)
    pinned_tweets = result[7]
    if pinned_tweets is not NULL:
        pinned_tweets = pinned_tweets + ',' + str(tweet_id)
    else:
        pinned_tweets = str(tweet_id)
    execute_query(db_conn,"UPDATE users SET pinned_tweets_ids = {} WHERE username = {}".format(pinned_tweets,username))
    return

def post_new_tweet(db_conn,username,tweet,retweet_id):
    now = str(datetime.now())
    h = re.findall(r"#(\w+)", tweet)
    results = read_query(db_conn, "SELECT * FROM current_ids")
    for result in results:
        curids = list(result)
        break
    tw = curids[0] + 1
    ch = curids[1]
    execute_query(db_conn,"DELETE FROM current_ids")
    execute_query(db_conn,"INSERT INTO current_ids VALUES ({},{})".format(tw,ch))
    for item in h:
        try:
            results = read_query(db_conn, "SELECT * FROM hashtags WHERE hashtag = {}".format(item))
            for result in results:
                result = list(result)
            result[1] = result[1]+','+str(tw)
            result[1] = result[2]+1
            execute_query(db_conn,"DELETE FROM hashtags WHERE hashtag = {}".format(item))
            execute_query(db_connm,"INSERT INTO hashtags VALUES ({},{},{})".format(result[0],result[1],result[2]))
        except:
            execute_query(db_conn,"INSERT INTO hashtags VALUES ({},{},{})".format(item,str(tw),1))
    hashtags = ''
    for item in h:
        hashtags = hashtags + item + ','
    hashatags = hashtags[:-1]
    if not retweet_id: 
        insert_tweet = "INSERT INTO tweets VALUES ({}, {}, {}, {}, {}, 0, NULL)".format(tw,tweet,username,hashtags,now)
    else:
        insert_tweet = "INSERT INTO tweets VALUES ({}, {}, {}, {}, {}, 1, {})".format(tw,tweet,username,hashtags,now,retweet_id)
    execute_query(db_conn,insert_tweet)
    results = read_query(db_conn, "SELECT * FROM users WHERE username = {}".format(username))
    for result in results:
        result = list(result)
    if result[5] is not NULL:
        result[5] = result[5]+','+str(tw)
    else:
        result[5] = str(tw)
    execute_query(db_conn,"UPDATE users SET tweet_ids = {} WHERE username = {}".format(result[5],username)
    return

def get_tweet_by_id(db_conn,tweet_id):
    results = read_query(db_conn,"SELECT * FROM tweets WHERE tweet_id = {}".format(tweet_id))
    for result in results:
        result = list(result)
        break
    return result

# follow someone using my username1 and his username2
def add_user_to_following(db_conn,username1,username2):
    try:
        results = read_query(db_conn, "SELECT * FROM users WHERE username = {}".format(username1))
        for result in results:
            result = list(result)
            break
        following = result[3]
        if following is not NULL:
            following = following + ',' + username2
        else:
            following = username2
        execute_query(db_conn,"UPDATE users SET following = {} WHERE username = {}".format(following,username1))
        results = read_query(db_conn, "SELECT * FROM users WHERE username = {}".format(username2))
        for result in results:
            result = list(result)
        followers = result[2]
        if followers is not NULL:
            followers = followers + ',' + username1
        else:
            followers = username1
        execute_query(db_conn,"UPDATE users SET followers = {} WHERE username = {}".format(followers,username2))
        return True
    except:
        return False

def rem_user_from_following(db_conn, username1, username2):
    try:
        results = read_query(db_conn, "SELECT * FROM users WHERE username = {}".format(username1))
        for result in results:
            result = list(result)
            break
        following = result[3]
        try:
            l = len(username2)
            m = len(following)
            for i in range(m):
                if following[i:i+l] == username2:
                    if i==0 and i+l==m:
                        following = NULL
                    elif i==0:
                        following = following[l+1:]
                    elif i+l==m:
                        following = following[:i-1]
                    else:
                        following = following[:i] + following[l+1:]
                    execute_query(db_conn,"UPDATE users SET following = {} WHERE username = {}".format(following,username1))
                    break
        except:
            # do nothing
        return True
    except:
        return False

# delete follower using my username1 and his username2
def rem_user_from_followers(db_conn,username1,username2):
    try:
        results = read_query(db_conn, "SELECT * FROM users WHERE username = {}".format(username1))
        for result in results:
            result = list(result)
            break
        followers = result[2]
        try:
            l = len(username2)
            m = len(followers)
            for i in range(m):
                if followers[i:i+l] == username2:
                    if i==0 and i+l==m:
                        followers = NULL
                    elif i==0:
                        followers = followers[l+1:]
                    elif i+l==m:
                        followers = followers[:i-1]
                    else:
                        followers = followers[:i] + followers[l+1:]
                    execute_query(db_conn,"UPDATE users SET followers = {} WHERE username = {}".format(followers,username1))
                    break
        except:
            # do nothing
        results = read_query(db_conn, "SELECT * FROM users WHERE username = {}".format(username2))
        for result in results:
            result = list(result)
            break
        following = result[3]
        try:
            l = len(username1)
            m = len(following)
            for i in range(m):
                if following[i:i+l] == username1:
                    if i==0 and i+l==m:
                        following = NULL
                    elif i==0:
                        following = following[l+1:]
                    elif i+l==m:
                        following = following[:i-1]
                    else:
                        following = following[:i] + following[l+1:]
                    execute_query(db_conn,"UPDATE users SET following = {} WHERE username = {}".format(following,username2))
                    break
        except:
            # do nothing
        return True
    except:
        return False

def get_news_feed(db_conn,username):
    tweets = []
    results = read_query(db_conn,"SELECT * FROM users WHERE username = {}".format(username))
    for result in results:
        result = list(result)
        followers = result[2]
        break
    followers = followers.split(',')
    ids = []
    for follower in followers:
        mm = read_query(db_conn,"SELECT * FROM users WHERE username = {}".format(follower))
        for m in mm:
            m = list(m)
            break
        id = m[5]
        id = list(map(int, id.split(',')))
        ids = ids + id
    get_tweets = "SELECT * FROM tweets WHERE tweet_if IN {}".format(ids)
    results = read_query(db_conn,get_tweets)
    for result in results:
        a = result[4]
        b = list(a.split())
        c = list(map(int,b[0].split('-')))
        d = list(b[1].split('.'))
        c = c + list(map(int,d[0].split(':')))
        c.append(int(d[1]))
        e = datetime(c[0],c[1],c[2],c[3],c[4],c[5],c[6])
        result[4] = e
        if result[5] == 1:
            mm = read_query(db_conn,"SELECT * FROM tweets WHERE tweet_id = {}".format(result[6]))
            for m in mm:
                m = list(m)
                break
            result = result + m
        tweets.append(result)
    tweets.sort(key = lambda x:(x[4]),reverse=True)
    try:
        return tweets[:DISPLAY_TWEETS]
    except:
        return tweets

def check_tweet_user(db_conn,username,tweet_id):
    results = read_query(db_conn,"SELECT * FROM users WHERE username = {}".format(username))
    for result in results:
        result = list(result)
        break
    ids = result[5]
    ids = set(map(int,ids.split(',')))
    if tweet_id in ids:
        return True
    return False

def my_profile(db_conn,username):
    results = read_query(db_conn,"SELECT * FROM users WHERE username = {}".format(username))
    for result in results:
        result = list(result)
        break
    followers = result[2]
    following = result[3]
    followers = followers.split(',')
    following = following.split(',')
    no_of_followers = len(followers)
    no_of_following = len(following)
    ids = result[5]
    ids = list(map(int, ids.split(',')))
    no_of_tweets = len(ids)
    pin_ids = result[7]
    pin_ids = list(map(int, ids.split(',')))
    other_ids = list(set(ids)-set(pin_ids))
    get_pin_tweets = "SELECT * FROM tweets WHERE tweet_id IN {}".format(pin_ids)
    get_other_tweets = "SELECT * FROM tweets WHERE tweet_id IN {}".format(other_ids)
    pin_tweets = []
    other_tweets = []
    results = read_query(db_conn,get_pin_tweets)
    for result in results:
        result = list(result)
        a = result[4]
        b = list(a.split())
        c = list(map(int,b[0].split('-')))
        d = list(b[1].split('.'))
        c = c + list(map(int,d[0].split(':')))
        c.append(int(d[1]))
        e = datetime(c[0],c[1],c[2],c[3],c[4],c[5],c[6])
        result[4] = e
        if result[5] == 1:
            mm = read_query(db_conn,"SELECT * FROM tweets WHERE tweet_id = {}".format(result[6]))
            for m in mm:
                m = list(m)
                break
            result = result + m
        pin_tweets.append(result)
    pin_tweets.sort(key = lambda x:(x[4]),reverse=True)
    results = read_query(db_conn,get_other_tweets)
    for result in results:
        result = list(result)
        a = result[4]
        b = list(a.split())
        c = list(map(int,b[0].split('-')))
        d = list(b[1].split('.'))
        c = c + list(map(int,d[0].split(':')))
        c.append(int(d[1]))
        e = datetime(c[0],c[1],c[2],c[3],c[4],c[5],c[6])
        result[4] = e
        if result[5] == 1:
            mm = read_query(db_conn,"SELECT * FROM tweets WHERE tweet_id = {}".format(result[6]))
            for m in mm:
                m = list(m)
                break
            result = result + m
        other_tweets.append(result)
    other_tweets.sort(key = lambda x:(x[4]),reverse=True)
    if len(other_tweets)>DISPLAY_TWEETS:
        other_tweets = other_tweets[:DISPLAY_TWEETS]
    return no_of_followers,no_of_following,no_of_tweets,pin_tweets,other_tweets