#
# Database access functions for the web forum.
# 

import time
import psycopg2

## Database connection
DB = psycopg2.connect("dbname=forum")
c = DB.cursor()

## Get posts from database.
def GetAllPosts():
    '''Get all the posts from the database, sorted with the newest first.

    Returns:
      A list of dictionaries, where each dictionary has a 'content' key
      pointing to the post content, and 'time' key pointing to the time
      it was posted.
    '''
    # posts = [{'content': str(row[1]), 'time': str(row[0])} for row in DB]
    # posts.sort(key=lambda row: row['time'], reverse=True)
    # return posts
    c.execute("select content, time from posts order by time")
    posts = [{'content': str(row[0]), 'time': str(row[1])} for row in c.fetchall()]
    return posts

## Add a post to the database.
def AddPost(content):
    '''Add a new post to the database.

    Args:
      content: The text content of the new post.
    '''
    # t = time.strftime('%c', time.localtime())
    # DB.append((t, content))
    c.execute("INSERT INTO posts (content) VALUES ('%s')" % content)
    DB.commit()
