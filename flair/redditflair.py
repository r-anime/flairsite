import praw
import random
import webbrowser
import socket
import os
from dotenv import load_dotenv
from prawcore import NotFound


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
        # redirect_uri="http://localhost:8080",
        username=os.environ.get('REDDIT_USERNAME'),
        user_agent=os.environ.get('REDDIT_USER_AGENT'),
        password=os.environ.get('REDDIT_USER_PASSWORD'),
        redirect_uri='http://localhost:8080'
    )

    subreddit_name = os.environ.get('SUBREDDIT_NAME_TO_ACT_ON')


    # print('DEBUG: ' + os.environ.get('REDDIT_CLIENT_ID'))
    # print('DEBUG: ' + os.environ.get('REDDIT_SECRET'))
    # print('DEBUG: ' + os.environ.get('REDDIT_USERNAME'))
    # print('DEBUG: ' + os.environ.get('REDDIT_USER_AGENT'))
    # print('DEBUG: ' + os.environ.get('REDDIT_USER_PASSWORD'))

    try:
        reddit.user.me()
        # print('PRAW Reddit loaded with user: ' + reddit.user.me())
        # print(reddit.user.me())
    except Exception as err:
        if (str(err) != 'invalid_grant error processing request'):
            print('SERVER REDDIT LOGIN FAILURE')
        else:
            # TODO: Remove - this is all for multi-factor login and can't be run without user input
            state = str(random.randint(0, 65000))
            scopes = ['identity', 'history', 'read', 'edit']
            url = reddit.auth.url(scopes, state, 'permanent')
            print('We will now open a window in your browser to complete the login process to reddit.')
            webbrowser.open(url)

            client = receive_connection()
            data = client.recv(1024).decode('utf-8')
            param_tokens = data.split(' ', 2)[1].split('?', 1)[1].split('&')
            params = {key: value for (key, value) in [token.split('=')
                                                      for token in param_tokens]}

            if state != params['state']:
                send_message(client, 'State mismatch. Expected: {} Received: {}'
                             .format(state, params['state']))
                return 1
            elif 'error' in params:
                send_message(client, params['error'])
                return 1

            refresh_token = reddit.auth.authorize(params["code"])
            send_message(client, "Refresh token: {}".format(refresh_token))

            print(refresh_token)
            return 0


def check_flair_length(flair_to_set):
    # TODO: Log a warning or something
    return len(flair_to_set) <= 64


def check_user_exists(username):
    try:
        reddit.redditor(username).id
    except NotFound:
        print("Aborting flair action, Reddit Username not found for: ")
        print(username)
        # TODO: Log an error or something
        return False
    return True


def set_flair(username, flair_to_set, flair_CSS_to_set):
    if check_user_exists(username):
        if check_flair_length(flair_to_set):
            #  TODO: Add logging of some kind on each request
            reddit.subreddit(subreddit_name).flair.set(username, flair_to_set, flair_CSS_to_set)


def set_flair_with_template(username, flair_to_set, template):
    if check_user_exists(username):
        if check_flair_length(flair_to_set):
            #  TODO: Add logging of some kind on each request
            reddit.subreddit(subreddit_name).flair.set(username, flair_to_set, flair_template_id=template)


def delete_flair(username):
    if check_user_exists(username):
        #  TODO: Add logging of some kind on each request
        reddit.subreddit(subreddit_name).flair.delete(username)


def get_flair(username):
    if check_user_exists(username):
        return next(reddit.subreddit(subreddit_name).flair(username))
    return ""


def get_user_karma(username):
    if check_user_exists(username):
        return reddit.redditor(username).comment_karma + reddit.redditor(username).link_karma
    return 0
