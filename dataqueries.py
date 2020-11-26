BUFF = 1024 #buffer size

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
    #TODO get top 5 trending hashtags as a list
    hashtags = []
    return hashtags

def get_tweets_by_hashtag(db_conn, hashtag):
    #TODO return a list of max 10 recent tweets with input hashtag
    tweets = []
    return tweets

def logout(db_conn, user):
    change_status = "UPDATE users SET is_online = 0 WHERE username = {}".format(user)
    execute_query(db_conn,change_status)
    return





# top 5 trending hashtags
retrieve_tags = "SELECT hashtag FROM hashtags ORDER BY count DESC LIMIT 5"
results = read_query(db_conn, retrieve_tags)
hashtags = []
for result in results:
    hashtags.append(result)

# tweets by hashtag
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
    retr.append(result)
retr.sort(key = lambda x:(x[4]),reverse=True)
tweets = []
if len(retr)>10:
    retr = retr[:10]
# format => list of tweets, for each tweet => tweet_id, tweet, username, hashtags, timestamp, is_retweet, retweet_id

# tweets by username
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
    retr.append(result)
retr.sort(key = lambda x:(x[4]),reverse=True)
if len(retr)>10:
    retr = retr[:10]
# format => list of tweets, for each tweet => tweet_id, tweet, username, hashtags, timestamp, is_retweet, retweet_id

# your pinned tweets
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
    retr.append(result)
retr.sort(key = lambda x:(x[4]),reverse=True)
# format => list of tweets, for each tweet => tweet_id, tweet, username, hashtags, timestamp, is_retweet, retweet_id

# pin tweet using tweet_id and username
results = read_query(db_conn,"SELECT * FROM users WHERE username = {}".format(username))
for result in results:
    result = list(result)
pinned_tweets = result[7]
if pinned_tweets is not NULL:
    pinned_tweets = pinned_tweets + ',' + str(tweet_id)
else:
    pinned_tweets = str(tweet_id)
execute_query(db_conn,"UPDATE users SET pinned_tweets_ids = {} WHERE username = {}".format(pinned_tweets,username))
    

# post tweet using tweet, username
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
insert_tweet = "INSERT INTO tweets VALUES ({}, {}, {}, {}, {}, 0, NULL)".format(tw,tweet,username,hashtags,now)
execute_query(db_conn,insert_tweet)
results = read_query(db_conn, "SELECT * FROM users WHERE username = {}".format(username))
for result in results:
    result = list(result)
if result[5] is not NULL:
    result[5] = result[5]+','+str(tw)
else:
    result[5] = str(tw)
execute_query(db_conn,"UPDATE users SET tweet_ids = {} WHERE username = {}".format(result[5],username)

# followers list by username
retr = "SELECT followers FROM users WHERE username = {}".format(username)
results = read_query(db_conn, retr)
result = str(results)
followers = result.split(',')

# following list by username
retr = "SELECT following FROM users WHERE username = {}".format(username)
results = read_query(db_conn, retr)
result = str(results)
following = result.split(',')

# follow someone using my username1 and his username2
results = read_query(db_conn, "SELECT * FROM users WHERE username = {}".format(username1))
for result in results:
    result = list(result)
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

# delete follower using my username1 and his username2
results = read_query(db_conn, "SELECT * FROM users WHERE username = {}".format(username1))
for result in results:
    result = list(result)
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