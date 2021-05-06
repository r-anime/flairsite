from allauth.account.views import LoginView, logout
from django.contrib import auth
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic import View

from .models import FlairsAwarded, FlairType
from .redditflair import *


# Create your views here.
def sort_flairtype_by_order(elem):
    return elem.order


def sort_awarded_flairs_by_order(elem):
    return elem.flair_id.order


def wiki(request):
    wiki_flairs = list(FlairType.objects.filter(wiki_display=True))
    wiki_flairs.sort(key=sort_flairtype_by_order)
    return render(request, 'flair/wiki.html', {
        'wiki_flairs': wiki_flairs,
    })


class FlairLoginView(LoginView):
    template_name = 'account/login.html'


class FlairLogoutView(View):
    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect(request.POST['next'])


@login_required()
def set_flair_url(request):
    if not setup_status:
        setup_reddit_once()

    # username = request.user #Lazyload issue potential
    username = auth.get_user(request).username

    current_flair = get_flair(username).get("flair_text")

    awarded_flairs = list(FlairsAwarded.objects.filter(display_name=username))
    awarded_flairs.sort(key=sort_awarded_flairs_by_order)

    default_flairs = list(FlairType.objects.filter(flair_type="default"))
    default_flairs.sort(key=sort_flairtype_by_order)

    return render(request, 'flair/setflair.html', {
        'username': username,
        'allowed_flairs': awarded_flairs,
        'current_flair': current_flair,
        'default_flairs': default_flairs,
    })


setup_status = False


def setup_reddit_once():
    reddit_setup()
    global setup_status  # for scope
    print('Reddit object initialized')
    setup_status = True


def flair_length_builder(flair_award_emoji_to_set, flair_tracker_emoji_to_set, flair_tracker_text_to_set,
                         flair_tracker_user_to_set):
    """Flair is limited to 64 characters, this method tries and cuts down longer flairs to fit"""
    """It is assumed the longest tracker_text_to_set will be 51 characters. Eg:"""
    """https://anime-planet.com/users/12345678901234567890"""

    # TODO: Validate that flair submitted is a correct link
    # TODO: Filter any emoji out of the user submitted portion

    full_length_string = flair_award_emoji_to_set + flair_tracker_emoji_to_set + flair_tracker_text_to_set + flair_tracker_user_to_set
    if len(full_length_string) <= 64:
        # Great, no problems return it
        return full_length_string

    # Remove the "https://" and see if that fits
    flair_tracker_text_to_set = flair_tracker_text_to_set.replace("https://", "")
    full_length_string = flair_award_emoji_to_set + flair_tracker_emoji_to_set + flair_tracker_text_to_set + flair_tracker_user_to_set
    if len(full_length_string) <= 64:
        return full_length_string

    # Cut the tracker emoji as well and see if that fits
    full_length_string = flair_award_emoji_to_set + flair_tracker_text_to_set + flair_tracker_user_to_set
    if len(full_length_string) <= 64:
        return full_length_string

    # Just have the tracker site emoji and the users username
    full_length_string = flair_award_emoji_to_set + flair_tracker_emoji_to_set + flair_tracker_user_to_set
    if len(full_length_string) <= 64:
        return full_length_string

    #  TODO: Somethings wrong, just give them their award emoji. Is this the best workflow?
    return flair_award_emoji_to_set


@login_required
def submit(request):
    """A view saving a user's response as their flair. Records a log in database, and redirecting them back to the index. Requires the user being logged in."""

    # username = request.user #Lazyload issue potential
    username = auth.get_user(request).username

    #  TODO: Add logging of some kind on each request

    # should reddit be setup here or somewhere else one single time?
    if not setup_status:
        setup_reddit_once()

    if 'flair_reset_request' in request.POST:
        delete_flair(username)
        # TODO: a redirect clears the form, find better or 'correct' way
        return redirect(request.META['HTTP_REFERER'])  # returns user back to /set page

    # Get allowed award flairs from the database and check only those (Server-side validation)
    awarded_flairs = list(FlairsAwarded.objects.filter(display_name=username))
    # Sorts flairs by database flairtype 'order' value
    awarded_flairs.sort(key=sort_awarded_flairs_by_order)

    flair_award_emoji_to_set = ""
    flair_tracker_emoji_to_set = ""
    flair_tracker_text_to_set = ""
    flair_tracker_user_to_set = ""
    flair_template_to_set = ""

    for flair_award in awarded_flairs:
        flair_check_name = "flairtype_" + flair_award.flair_id.display_name
        if flair_check_name in request.POST:
            flair_award_emoji_to_set = flair_award_emoji_to_set + flair_award.flair_id.reddit_flair_emoji  # Get from database what should be set

    # Sort out 'default' flair section
    if "defaultflair" in request.POST:
        if request.POST["defaultflair"] == "notracker":
            print("notracker")

        if "trackerAccountName" in request.POST:
            # TODO: Check if username is set or something
            # print(request.POST)
            # print(request.POST["defaultflair"])
            # print(request.POST["trackerAccountName"])

            default_flairs = list(FlairType.objects.filter(flair_type="default"))
            for flairtype in default_flairs:
                print(flairtype)
                if request.POST["defaultflair"] == flairtype.display_name:
                    #  Set both tracker icon and entered tracker name/id
                    flair_tracker_emoji_to_set = flairtype.reddit_flair_emoji
                    flair_tracker_text_to_set = flairtype.reddit_flair_text
                    flair_tracker_user_to_set = request.POST["trackerAccountName"]
                    flair_template_to_set = flairtype.reddit_flair_template_id
                    break

    # Build the flair text that will then be set
    final_flair_to_set = flair_length_builder(flair_award_emoji_to_set, flair_tracker_emoji_to_set,
                                              flair_tracker_text_to_set, flair_tracker_user_to_set)

    # Finally set the flair on the subreddit, use the template way if one is set
    if flair_template_to_set == "":
        set_flair(username, final_flair_to_set, "")
    else:
        set_flair_with_template(username, final_flair_to_set, flair_template_to_set)

    # TODO: This redirects back to /set, maybe not what is needed
    return redirect(request.META['HTTP_REFERER'])  # returns user back to /set page
