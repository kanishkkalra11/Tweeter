from datetime import datetime
import re

BUFF = 1024 #buffer size
DISPLAY_TWEETS = 10 #Number of tweets to display on CLI

def execute_query(connection, query):
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    return

def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    cursor.execute(query)
    result = cursor.fetchall()
    return result

def register_new_user(db_conn, username, password):
    insert_user = "INSERT INTO users VALUES ('{}', '{}', NULL, NULL, 1, NULL, NULL, NULL)".format(username,password)
    try:
        execute_query(db_conn, insert_user)
        return True
    except:
        return False

def check_user_pass(db_conn, username, password):
    results = read_query(db_conn,"SELECT * FROM users WHERE username = '{}'".format(username))
    a = len(results)
    if a==0:
        return False
    result = list(results[0])
    if result[1]==password:
        return True
    return False

def check_user_exists(db_conn, username):
    results = read_query(db_conn,"SELECT * FROM users WHERE username = '{}'".format(username))
    a = len(results)
    if a==0:
        return False
    return True

def get_trending_hashtags(db_conn):
    retrieve_tags = "SELECT hashtag FROM hashtags ORDER BY count DESC LIMIT 5"
    results = read_query(db_conn, retrieve_tags)
    hashtags = []
    for result in results:
        hashtags.append(result[0])
    return hashtags

def get_tweets_by_hashtag(db_conn, hashtag):
    retr = []
    get_tweet_ids = "SELECT * FROM hashtags WHERE hashtag = '{}'".format(hashtag)
    results = read_query(db_conn, get_tweet_ids)
    if len(results)==0:
        return retr
    result = list(results[0])
    ids = result[1]
    ids = list(map(int, ids.split(',')))
    for id in ids:
        get_tweets = "SELECT * FROM tweets WHERE tweet_id = {}".format(id)
        results = read_query(db_conn, get_tweets)
        result = list(results[0])
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
            m = list(mm[0])
            result = result + m
        retr.append(result)
    retr.sort(key = lambda x:(x[4]),reverse=True)
    if len(retr)>DISPLAY_TWEETS:
        retr = retr[:DISPLAY_TWEETS]
    return retr
    # format => list of tweets, for each tweet => tweet_id, tweet, username, hashtags, timestamp, is_retweet, retweet_id

def logout(db_conn, username):
    change_status = "UPDATE users SET is_online = 0 WHERE username = '{}'".format(username)
    execute_query(db_conn,change_status)
    return

def get_tweets_of_user(db_conn, username):
    retr = []
    get_tweet_ids = "SELECT * FROM users WHERE username = '{}'".format(username)
    results = read_query(db_conn, get_tweet_ids)
    if len(results)==0:
        return retr
    result = list(results[0])
    ids = result[5]
    if ids is None:
        return retr
    ids = list(map(int, ids.split(',')))
    for id in ids:
        results = read_query(db_conn, "SELECT * FROM tweets WHERE tweet_id = {}".format(id))
        result = list(results[0])
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
            m = list(mm[0])
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
    results = read_query(db_conn, "SELECT * FROM users WHERE username = '{}'".format(username1))
    result = list(results[0])
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
    retr = "SELECT followers FROM users WHERE username = '{}'".format(username)
    results = read_query(db_conn, retr)
    result = list(results[0])
    result = str(result[2])
    followers = result.split(',')
    online_followers = []
    offline_followers = []
    for follower in followers:
        results = read_query(db_conn,"SELECT * FROM users WHERE username = '{}'".format(follower))
        result = list(results[0])
        if result[4] == 0:
            offline_followers.append(follower)
        else:
            online_followers.append(follower)
    return online_followers,offline_followers

def get_following_list(db_conn,username):
    retr = "SELECT following FROM users WHERE username = '{}'".format(username)
    results = read_query(db_conn, retr)
    result = list(results[0])
    result = str(results[3])
    following = result.split(',')
    online_following = []
    offline_following = []
    for person in following:
        results = read_query(db_conn,"SELECT * FROM users WHERE username = '{}'".format(username))
        result = list(results[0])
        if result[4] == 0:
            offline_following.append(person)
        else:
            online_following.append(person)
    return online_following,offline_following

def get_pinned_tweets_of_user(db_conn,username):
    retr = []
    get_tweet_ids = "SELECT * FROM users WHERE username = '{}'".format(username)
    results = read_query(db_conn, get_tweet_ids)
    if len(results)==0:
        return retr
    result = list(results[0])
    ids = result[7]
    if ids is None:
        return retr
    ids = list(map(int, ids.split(',')))
    for id in ids:
        results = read_query(db_conn, "SELECT * FROM tweets WHERE tweet_id = {}".format(id))
        result = list(results[0])
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
            m = list(mm[0])
            result = result + m
        retr.append(result)
    retr.sort(key = lambda x:(x[4]),reverse=True)
    return retr
    # format => list of tweets, for each tweet => tweet_id, tweet, username, hashtags, timestamp, is_retweet, retweet_id

def pin_new_tweet(db_conn,username,tweet_id):
    try:
        results = read_query(db_conn,"SELECT * FROM users WHERE username = '{}'".format(username))
        result = list(results[0])
        pinned_tweets = result[7]
        if pinned_tweets is not None:
            pinned_tweets = pinned_tweets + ',' + str(tweet_id)
        else:
            pinned_tweets = str(tweet_id)
        execute_query(db_conn,"UPDATE users SET pinned_tweets_ids = '{}' WHERE username = '{}'".format(pinned_tweets,username))
        return True
    except:
        return False

def post_new_tweet(db_conn,username,tweet,retweet_id):
    try:
        now = str(datetime.now())
        h = re.findall(r"#(\w+)", tweet)
        results = read_query(db_conn, "SELECT * FROM current_ids")
        curids = list(results[0])
        tw = curids[0] + 1
        ch = curids[1]
        execute_query(db_conn,"DELETE FROM current_ids")
        execute_query(db_conn,"INSERT INTO current_ids VALUES ({},{})".format(tw,ch))
        for item in h:
            results = read_query(db_conn, "SELECT * FROM hashtags WHERE hashtag = '{}'".format(item))
            if len(results)!=0:
                result = list(results[0])
                result[1] = result[1]+','+str(tw)
                result[2] = result[2]+1
                execute_query(db_conn,"DELETE FROM hashtags WHERE hashtag = '{}'".format(item))
                execute_query(db_conn,"INSERT INTO hashtags VALUES ('{}','{}',{})".format(result[0],result[1],result[2]))
            else:
                execute_query(db_conn,"INSERT INTO hashtags VALUES ('{}','{}',{})".format(item,str(tw),1))
        hashtags = ','.join(h)
        if not retweet_id: 
            insert_tweet = "INSERT INTO tweets VALUES ({}, '{}', '{}', '{}', '{}', 0, NULL)".format(tw,tweet,username,hashtags,now)
        else:
            insert_tweet = "INSERT INTO tweets VALUES ({}, '{}', '{}', '{}', '{}', 1, {})".format(tw,tweet,username,hashtags,now,retweet_id)
        execute_query(db_conn,insert_tweet)
        results = read_query(db_conn, "SELECT * FROM users WHERE username = '{}'".format(username))
        result = list(results[0])
        if result[5] is not None:
            result[5] = result[5]+','+str(tw)
        else:
            result[5] = str(tw)
        execute_query(db_conn,"UPDATE users SET tweet_ids = '{}' WHERE username = '{}'".format(result[5],username))
        return True
    except:
        return False

def get_tweet_by_id(db_conn,tweet_id):
    results = read_query(db_conn,"SELECT * FROM tweets WHERE tweet_id = {}".format(tweet_id))
    result = list(results[0])
    return result

# follow someone using my username1 and his username2
def add_user_to_following(db_conn,username1,username2):
    try:
        results = read_query(db_conn, "SELECT * FROM users WHERE username = '{}'".format(username2))
        if len(results)==0:
            return False
        result = list(results[0])
        followers = result[2]
        if followers is not None:
            followers = followers + ',' + username1
        else:
            followers = username1
        execute_query(db_conn,"UPDATE users SET followers = '{}' WHERE username = '{}'".format(followers,username2))
        results = read_query(db_conn, "SELECT * FROM users WHERE username = '{}'".format(username1))
        result = list(results[0])
        following = result[3]
        if following is not None:
            following = following + ',' + username2
        else:
            following = username2
        execute_query(db_conn,"UPDATE users SET following = '{}' WHERE username = '{}'".format(following,username1))
        return True
    except:
        return False

def rem_user_from_following(db_conn, username1, username2):
    try:
        results = read_query(db_conn, "SELECT * FROM users WHERE username = '{}'".format(username2))
        if len(results)==0:
            return False
        result = list(results[0])
        followers = result[2]
        try:
            l = len(username1)
            m = len(followers)
            for i in range(m):
                if followers[i:i+l] == username1:
                    if i==0 and i+l==m:
                        followers = None
                    elif i==0:
                        followers = followers[l+1:]
                    elif i+l==m:
                        followers = followers[:i-1]
                    else:
                        followers = followers[:i] + followers[l+1:]
                    execute_query(db_conn,"UPDATE users SET followers = '{}' WHERE username = '{}'".format(followers,username2))
                    break
        except:
            garbage = 9 #do nothing
        results = read_query(db_conn, "SELECT * FROM users WHERE username = '{}'".format(username1))
        result = list(results[0])
        following = result[3]
        try:
            l = len(username2)
            m = len(following)
            for i in range(m):
                if following[i:i+l] == username2:
                    if i==0 and i+l==m:
                        following = None
                    elif i==0:
                        following = following[l+1:]
                    elif i+l==m:
                        following = following[:i-1]
                    else:
                        following = following[:i] + following[l+1:]
                    execute_query(db_conn,"UPDATE users SET following = '{}' WHERE username = '{}'".format(following,username1))
                    break
        except:
            garbage = 9 #do nothing
        return True
    except:
        return False

# delete follower using my username1 and his username2
def rem_user_from_followers(db_conn,username1,username2):
    try:
        results = read_query(db_conn, "SELECT * FROM users WHERE username = '{}'".format(username2))
        if len(results)==0:
            return False
        result = list(results[0])
        following = result[3]
        try:
            l = len(username1)
            m = len(following)
            for i in range(m):
                if following[i:i+l] == username1:
                    if i==0 and i+l==m:
                        following = None
                    elif i==0:
                        following = following[l+1:]
                    elif i+l==m:
                        following = following[:i-1]
                    else:
                        following = following[:i] + following[l+1:]
                    execute_query(db_conn,"UPDATE users SET following = '{}' WHERE username = '{}'".format(following,username2))
                    break
        except:
            garbage = 7 # do nothing
        results = read_query(db_conn, "SELECT * FROM users WHERE username = '{}'".format(username1))
        result = list(results[0])
        followers = result[2]
        try:
            l = len(username2)
            m = len(followers)
            for i in range(m):
                if followers[i:i+l] == username2:
                    if i==0 and i+l==m:
                        followers = None
                    elif i==0:
                        followers = followers[l+1:]
                    elif i+l==m:
                        followers = followers[:i-1]
                    else:
                        followers = followers[:i] + followers[l+1:]
                    execute_query(db_conn,"UPDATE users SET followers = '{}' WHERE username = '{}'".format(followers,username1))
                    break
        except:
            garbage = 9 # do nothing
        return True
    except:
        return False

def get_news_feed(db_conn,username):
    tweets = []
    results = read_query(db_conn,"SELECT * FROM users WHERE username = '{}'".format(username))
    result = list(results[0])
    followers = result[2]
    if followers is None:
        return tweets
    followers = followers.split(',')
    ids = []
    for follower in followers:
        mm = read_query(db_conn,"SELECT * FROM users WHERE username = '{}'".format(follower))
        m = list(mm[0])
        id = m[5]
        if id is not None:
            id = list(map(int, id.split(',')))
            ids = ids + id
    if len(ids)==0:
        return tweets
    for id in ids:
        results = read_query(db_conn, "SELECT * FROM tweets WHERE tweet_id = {}".format(id))
        result = list(results[0])
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
            m = list(mm[0])
            result = result + m
        tweets.append(result)
    tweets.sort(key = lambda x:(x[4]),reverse=True)
    try:
        return tweets[:DISPLAY_TWEETS]
    except:
        return tweets

def check_tweet_of_user(db_conn,username,tweet_id):
    results = read_query(db_conn,"SELECT * FROM users WHERE username = '{}'".format(username))
    result = list(results[0])
    ids = result[5]
    if ids is None:
        return False
    ids = set(map(int,ids.split(',')))
    if tweet_id in ids:
        return True
    return False

def get_user_profile(db_conn,username):
    results = read_query(db_conn,"SELECT * FROM users WHERE username = '{}'".format(username))
    result = list(results[0])
    followers = result[2]
    following = result[3]
    if followers is not None:
        followers = followers.split(',')
        no_of_followers = len(followers)
    else:
        no_of_followers = 0
    if following is not None:
        following = following.split(',')
        no_of_following = len(following)
    else:
        no_of_following = 0
    ids = result[5]
    pin_tweets = []
    other_tweets = []
    if ids is None:
        no_of_tweets = 0
        return no_of_followers,no_of_following,no_of_tweets,pin_tweets,other_tweets    
    ids = list(map(int, ids.split(',')))
    no_of_tweets = len(ids)
    pin_ids = result[7]
    if pin_ids is None:
        other_ids = ids
        for id in other_ids:
            results = read_query(db_conn, "SELECT * FROM tweets WHERE tweet_id = {}".format(id))
            result = list(results[0])
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
                m = list(mm[0])
                result = result + m
            other_tweets.append(result)
        other_tweets.sort(key = lambda x:(x[4]),reverse=True)
        if len(other_tweets)>DISPLAY_TWEETS:
            other_tweets = other_tweets[:DISPLAY_TWEETS]
        return no_of_followers,no_of_following,no_of_tweets,pin_tweets,other_tweets
    pin_ids = list(map(int, pin_ids.split(',')))
    other_ids = list(set(ids)-set(pin_ids))
    for id in pin_ids:
        results = read_query(db_conn, "SELECT * FROM tweets WHERE tweet_id = {}".format(id))
        result = list(results[0])
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
            m = list(mm[0])
            result = result + m
        pin_tweets.append(result)
    pin_tweets.sort(key = lambda x:(x[4]),reverse=True)
    if len(other_ids)==0:
        return no_of_followers,no_of_following,no_of_tweets,pin_tweets,other_tweets
    for id in other_ids:
        results = read_query(db_conn, "SELECT * FROM tweets WHERE tweet_id = {}".format(id))
        result = list(results[0])
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
            m = list(mm[0])
            result = result + m
        other_tweets.append(result)
    other_tweets.sort(key = lambda x:(x[4]),reverse=True)
    if len(other_tweets)>DISPLAY_TWEETS:
        other_tweets = other_tweets[:DISPLAY_TWEETS]
    return no_of_followers,no_of_following,no_of_tweets,pin_tweets,other_tweets