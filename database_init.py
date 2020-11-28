import mysql.connector
from mysql.connector import Error

MySQL_hostname = 'localhost'
MySQL_username = 'root'
MySQL_password = 'mysqlpwd'

def create_server_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection
connection = create_server_connection(MySQL_hostname, MySQL_username, MySQL_password)

def create_database(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Database created successfully")
    except Error as err:
        print(f"Error: '{err}'")
create_database(connection, "CREATE DATABASE Tweeter")

def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection
connection = create_db_connection(MySQL_hostname, MySQL_username, MySQL_password, "Tweeter")

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")

create_user_table = """
CREATE TABLE users (
  username VARCHAR(256) PRIMARY KEY,
  password VARCHAR(256) NOT NULL,
  followers TEXT,
  following TEXT,
  is_online BIT,
  tweet_ids TEXT,
  active_chats_ids TEXT,
  pinned_tweets_ids TEXT
  );
 """
execute_query(connection, create_user_table)

create_curids_table = """
CREATE TABLE current_ids (
  tweets INT NOT NULL,
  chats INT NOT NULL
  );
 """
execute_query(connection, create_curids_table)

create_tweets_table = """
CREATE TABLE tweets (
  tweet_id INT PRIMARY KEY,
  tweet TEXT,
  username VARCHAR(256),
  hashtags TEXT,
  timestamp VARCHAR(256),
  is_retweet BIT,
  retweet_id INT
  );
 """
execute_query(connection, create_tweets_table)

create_hashtags_table = """
CREATE TABLE hashtags (
  hashtag VARCHAR(256) PRIMARY KEY,
  tweet_ids TEXT,
  count INT
  );
 """
execute_query(connection, create_hashtags_table)

create_chats_table = """
CREATE TABLE chats (
  chat_id INT PRIMARY KEY,
  user1 VARCHAR(256),
  user2 VARCHAR(256),
  chat TEXT
  );
 """
execute_query(connection, create_chats_table)

insert_user = """
INSERT INTO users VALUES
('undertaker', 'paulheyman', 'kane', NULL, 0, '1', '1', '1'),
('kane', 'hell', NULL, 'undertaker', 0, NULL, '1', NULL);
"""
execute_query(connection, insert_user)

insert_hashtag = """
INSERT INTO hashtags VALUES
('deadman', '1', 2),
('wrestling', '1', 1),
('gorgoyle' ,'1', 1),
('strawman' ,'1', 1),
('unagi', '1', 1);
"""
execute_query(connection, insert_hashtag)

insert_tweet = """
INSERT INTO tweets VALUES
(1, 'Hello twitter! #deadman #wrestling #deadman #gorgoyle #strawman #unagi', 'undertaker', 'deadman,wrestling,deadman,gorgoyle,strawman,unagi', '2020-11-18 21:57:31.755873', 0, NULL);
"""
execute_query(connection, insert_tweet)

insert_chat = """
INSERT INTO chats VALUES
(1, 'undertaker', 'kane', "@undertaker: Hello my brother kane@kane: i will find you and kill you");
"""
execute_query(connection, insert_chat)

insert_curids = """
INSERT INTO current_ids VALUES
(1, 1);
"""
execute_query(connection, insert_curids)