import os
import socket
import praw
from dotenv import load_dotenv
from prawcore import NotFound

from flair.models import ActionLogging


def LogAction(action, action_info, username):
    logItem = ActionLogging(
        action=action,
        action_info=action_info,
        reddit_name=username
    )
    logItem.save()


def LogError(action, action_info, username, error):
    LogError = ActionLogging(
        action=action,
        action_info=action_info,
        reddit_name=username,
        error=error
    )
    LogError.save()


def receive_connection():
    """
    Wait for and then return a connected socket..
    Opens a TCP connection on port 8080, and waits for a single client.
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('localhost', 8080))
    server.listen(1)
    client = server.accept()[0]
    server.close()
    return client


def send_message(client, message):
    """
    Send message to client and close the connection.
    """
    client.send('HTTP/1.1 200 OK\r\n\r\n{}'.format(message).encode('utf-8'))
    client.close()


def reddit_setup():
    global reddit
    global subreddit_name
    load_dotenv()

    # SCRIPT FORMAT
    reddit = praw.Reddit(
        client_id=os.environ.get('REDDIT_CLIENT_ID'),
        client_secret=os.environ.get('REDDIT_SECRET'),
        username=os.environ.get('REDDIT_USERNAME'),
        user_agent=os.environ.get('REDDIT_USER_AGENT'),
        password=os.environ.get('REDDIT_USER_PASSWORD'),
        redirect_uri=os.environ.get('REDIRECT_URI'),
    )

    subreddit_name = os.environ.get('SUBREDDIT_NAME_TO_ACT_ON')

    # print('DEBUG: ' + os.environ.get('REDDIT_CLIENT_ID'))
    # print('DEBUG: ' + os.environ.get('REDDIT_SECRET'))
    # print('DEBUG: ' + os.environ.get('REDDIT_USERNAME'))
    # print('DEBUG: ' + os.environ.get('REDDIT_USER_AGENT'))
    # print('DEBUG: ' + os.environ.get('REDDIT_USER_PASSWORD'))

    try:
        reddit.user.me()
    except Exception as err:
        if str(err) != 'invalid_grant error processing request':
            print('SERVER REDDIT LOGIN FAILURE')


def check_flair_length(flair_to_set, username):
    if len(flair_to_set) <= 64:
        return True
    else:
        LogError("check_flair_length", flair_to_set, username, 'Flair longer than 64 characters.')
        return False


def check_user_exists(username):
    try:
        reddit.redditor(username).id
    except NotFound:
        LogError("check_user_exists", '', username, 'Username Not Found')
        return False
    return True


def set_flair(username, flair_to_set, flair_CSS_to_set):
    if check_user_exists(username):
        if check_flair_length(flair_to_set, username):
            LogAction("set_flair", flair_to_set, username)
            reddit.subreddit(subreddit_name).flair.set(username, flair_to_set, flair_CSS_to_set)


def set_flair_with_template(username, flair_to_set, template):
    if check_user_exists(username):
        if check_flair_length(flair_to_set, username):
            LogAction("set_flair_with_template", flair_to_set, username)
            reddit.subreddit(subreddit_name).flair.set(username, flair_to_set, flair_template_id=template)


def delete_flair(username):
    if check_user_exists(username):
        LogAction("delete_flair", '', username)
        reddit.subreddit(subreddit_name).flair.delete(username)


def get_flair(username):
    if check_user_exists(username):
        return next(reddit.subreddit(subreddit_name).flair(username))
    return ""


def get_user_karma(username):
    if check_user_exists(username):
        return reddit.redditor(username).comment_karma + reddit.redditor(username).link_karma
    return 0
