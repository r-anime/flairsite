# [/r/anime User Flair Website](https://flair.r-anime.moe/)

Website for letting users set their own flair on [/r/anime](https://www.reddit.com/r/anime/). Built with [Django](https://www.djangoproject.com/) as the backend and [BootstrapVue](https://bootstrap-vue.org/) (Bootstrap and embedded Vue.js) on the frontend.

## Features

* Reddit authentication.
* Admin page for editing the database.
* Default flairs available to all.
* Award flairs can be granted to specific users.
* Makes use of [Reddit's emoji](https://mods.reddithelp.com/hc/en-us/articles/360010560371-Emojis) which works on both old/new reddit.
* Makes use of [Reddit's flair templates.](https://mods.reddithelp.com/hc/en-us/articles/360010541651-User-Flair) which also works on old/new reddit.

## Requirements

Python 3.6+

## Setup

Setup Reddit authorised applications. This projects makes use of an 'web app' application for reading other users accounts (Set 'redirect uri' as https://example.com/accounts/reddit/login/callback/). 

It also uses a separate 'personal use script' for an individual account that will be responsible for setting the flairs on the target subreddit. 
Ensure that account has subreddot permissions to set flairs on the target subreddit (moderator permissions). 


You can make apps on Reddit [here](https://www.reddit.com/prefs/apps) for a logged in account.

* Copy template.env to .env and set the environment variables:
    * `DJANGO_SECRET_KEY` should be a strong, secure [secret key](https://docs.djangoproject.com/en/3.1/ref/settings/#secret-key) for Django.
    * `REDDIT_CLIENT_ID` Reddit Script Credentials.
    * `REDDIT_SECRET` Reddit Script Credentials.
    * `REDDIT_USERNAME` Reddit Script Credentials.
    * `REDDIT_USER_PASSWORD` Reddit Script Credentials.
    * `SUBREDDIT_NAME_TO_ACT_ON` The subreddit that the project will edit flairs on.
    * `WEBSITE_REDDIT_OAUTH_CLIENT_ID` OAuth Web App Credentials.
    * `WEBSITE_REDDIT_OAUTH_SECRET` OAuth Web App Credentials.
    * `DEBUG` Sets the website in debug mode or not.

* Create the website's database: `python manage.py migrate`.
* Create a superuser for the website: `python manage.py createsuperuser`.
* Run the server with: `manage.py runserver`
* Connect to admin interface server at: `http://127.0.0.1:8000/admin/`
* Add your host/domain name(s) to `Sites` on the admin page (`.../admin/sites/site/`).
* Configure a Social application on the admin page (`.../admin/socialaccount/socialapp/`) for Reddit. Get that URI right http/https matters.
* Start setting up flairs in the website's database:
  * [Setup emoji on your subreddit.](https://mods.reddithelp.com/hc/en-us/articles/360010560371-Emojis)
  * [Setup flair templates on your subreddit](https://mods.reddithelp.com/hc/en-us/articles/360010541651-User-Flair)
  * Use the admin page to setup a `Flair type` you will use your setup emoji and template from the above two steps. [Example](https://i.imgur.com/XAvboSA.png)
  * Setup a `Flair type` with an `award` `Flair Type` and then award that flair in `Flairs awardeds`, note the reddit username is case sensitive 
* Go to the flair site and login as a reddit user, test the set (`.../flair/set`) and wiki pages (`.../wiki`)
* You should now be able to see the loaded flairs and set them.
