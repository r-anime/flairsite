from allauth.account.views import LoginView, logout
from django.contrib import auth
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic import View

from .flairparsing import *
from .models import FlairDisplay
from .redditflair import *


def sort_flairtype_by_order(elem):
    return elem.order


def sort_awarded_flairs_by_order(elem):
    return elem.flair_id.order


def wiki(request):
    wiki_flairs = list(FlairType.objects.filter(wiki_display=True))
    print(wiki_flairs)
    wiki_flairs.sort(key=sort_flairtype_by_order)
    print(wiki_flairs)

    #TODO: CLEANUP AND REMOVE
    # for ft in wiki_flairs:
    #     for s in ft.flair_display.all():
    #         print(s.static_image)

    # wiki_images = list(wiki_flairs.flair_display.static_image)
    # print(wiki_images)
    print("-------")

    return render(request, 'flair/wiki.html', {
        'wiki_flairs': wiki_flairs
    })


class FlairLoginView(LoginView):
    template_name = 'account/login.html'


class FlairLogoutView(View):
    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect(request.POST['next'])


def LogLogin(username, user_agent):
    logItem = ActionLogging(
        action='set_flair_url',
        reddit_name=username,
        user_agent=user_agent
    )
    logItem.save()


@login_required()
def set_flair_url(request):
    if not setup_status:
        setup_reddit_once()

    # username = request.user #Lazyload issue potential
    username = auth.get_user(request).username

    # TODO: Decide if this should be toggleable off by the admin
    LogLogin(username, request.META.get('HTTP_USER_AGENT', ''))

    if check_user_exists(username):

        current_flair = get_flair(username).get("flair_text")
        current_emoji_flair_list = users_current_awarded_flair_icons(current_flair)
        stripped_flair = colon_emoji_strip(current_flair)
        stripped_flair_url = make_url_of_flair_text(stripped_flair)
        tracker_name = tracker_type(current_flair)
        tracker_user_account_name = strip_flair_to_tracker_account_name(current_flair)

        awarded_flairs = list(FlairsAwarded.objects.filter(display_name__iexact=username))  # __iexact to be case insensitive
        awarded_flairs.sort(key=sort_awarded_flairs_by_order)
        awarded_flairs = remove_duplicate_awarded_flairs(awarded_flairs)
        awarded_flairs = find_already_set_flairs(awarded_flairs,
                                                 current_emoji_flair_list)  # Adds 'checked' status to objects

        default_flairs = list(FlairType.objects.filter(flair_type__iexact="default"))
        default_flairs.sort(key=sort_flairtype_by_order)

        return render(request, 'flair/setflair.html', {
            'username': username,
            'allowed_flairs': awarded_flairs,
            'current_flair_text': stripped_flair,
            'current_flair_url': stripped_flair_url,
            'current_emoji_flair_list': current_emoji_flair_list,
            'tracker_name': tracker_name,
            'tracker_user_account_name': tracker_user_account_name,
            'default_flairs': default_flairs,
        })
    else:
        return HttpResponse('No reddit account is attached to this login. (Shadowbanned or Site-Administrator)')


setup_status = False


def setup_reddit_once():
    reddit_setup()
    global setup_status  # for scope
    print('Reddit object initialized')
    setup_status = True


@login_required
def submit(request):
    """A view saving a user's response as their flair. Records a log in database, and redirecting them back to the index. Requires the user being logged in."""

    # username = request.user #Lazyload issue potential
    username = auth.get_user(request).username

    # should reddit be setup here or somewhere else one single time?
    if not setup_status:
        setup_reddit_once()

    if 'flair_reset_request' in request.POST:
        delete_flair(username)
        return redirect('/set')  # returns user back to /set page

    # Get allowed award flairs from the database and check only those (Server-side validation)
    awarded_flairs = list(FlairsAwarded.objects.filter(display_name__iexact=username))  # __iexact to be case insensitive
    # Sorts flairs by database flairtype 'order' value
    awarded_flairs = remove_duplicate_awarded_flairs(awarded_flairs)
    awarded_flairs.sort(key=sort_awarded_flairs_by_order)

    flair_award_emoji_to_set = ""
    flair_tracker_emoji_to_set = ""
    flair_tracker_text_to_set = ""
    flair_tracker_user_account = ""
    flair_template_to_set = ""

    for flair_award in awarded_flairs:
        flair_check_name = "flairtype_" + flair_award.flair_id.display_name
        if flair_check_name in request.POST:
            flair_award_emoji_to_set = flair_award_emoji_to_set + flair_award.flair_id.flair_display.reddit_flair_emoji  # Get from database what should be set

    # Sort out 'default' flair section
    if "defaultflair" in request.POST:
        if request.POST["defaultflair"] == "notracker":
            # print("notracker")
            pass
        elif "trackerAccountName" in request.POST:
            # print(request.POST) # Debugging

            default_flairs = list(FlairType.objects.filter(flair_type__iexact="default"))
            for flairtype in default_flairs:
                # print(flairtype.display_name)
                # Look for through database flairs to find what they have
                if request.POST["defaultflair"] == flairtype.display_name:
                    #  Set both tracker icon and entered tracker name/id
                    flair_tracker_emoji_to_set = flairtype.flair_display.reddit_flair_emoji
                    flair_tracker_text_to_set = flairtype.reddit_flair_text
                    flair_tracker_user_account = request.POST["trackerAccountName"]
                    flair_template_to_set = flairtype.reddit_flair_template_id
                    break

    # Build the flair text that will then be set
    final_flair_to_set = flair_length_builder(flair_award_emoji_to_set, flair_tracker_emoji_to_set,
                                              flair_tracker_text_to_set, flair_tracker_user_account)

    # Finally set the flair on the subreddit, use the template way if one is set
    if flair_template_to_set == "":
        set_flair(username, final_flair_to_set, "")
    else:
        set_flair_with_template(username, final_flair_to_set, flair_template_to_set)

    return redirect('/set')  # returns user back to /set page
