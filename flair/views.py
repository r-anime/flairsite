import random

from allauth.account.views import LoginView, logout
from django.contrib import auth
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic import View

from .flairparsing import *
from .models import FlairsAwarded, FlairType
from .redditflair import *


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
        current_emoji_flair_list = parse_flair_types(current_flair)
        set_current_assigned_flairs(username, current_emoji_flair_list)

        stripped_flair = colon_emoji_strip(current_flair)
        stripped_flair_url = make_url_of_flair_text(stripped_flair)
        tracker_name = tracker_type(current_flair)
        tracker_user_account_name = strip_flair_to_tracker_account_name(current_flair)

        # Include dummy None flair if they want to clear their general choice
        none_type = FlairType()
        none_type.id = 0
        none_type.display_name = "None"
        general_flairs = list(FlairType.objects.filter(flair_type__exact="general"))
        custom_flairs = list(FlairsAwarded.objects.filter(display_name__iexact=username).filter(flair_id__flair_type="custom"))
        # Temporary: pick a present flair if they exist.
        _pick_present_flair(username, custom_flairs)
        general_flairs = [none_type] + [custom_flair.flair_id for custom_flair in custom_flairs] + general_flairs
        find_already_set_general_flairs(general_flairs, current_emoji_flair_list)  # Adds 'checked' status to objects

        awarded_flairs = list(FlairsAwarded.objects.filter(display_name__iexact=username).filter(flair_id__flair_type="achievement"))  # __iexact to be case insensitive
        awarded_flairs.sort(key=sort_awarded_flairs_by_order)
        awarded_flairs = check_awarded_flairs_overrides(awarded_flairs)  # Applies any overrides
        awarded_flairs = remove_duplicate_awarded_flairs(awarded_flairs)
        find_already_set_award_flairs(awarded_flairs, current_emoji_flair_list)  # Adds 'checked' status to objects

        # Fix up 'Flair Preview' section with overrides, also if a user has multiple wins (x2,x3,x4...):
        current_emoji_flair_list = apply_awarded_flairs_overrides(awarded_flairs, current_emoji_flair_list)

        tracker_flairs = list(FlairType.objects.filter(flair_type__exact="list"))
        tracker_flairs.sort(key=sort_flairtype_by_order)

        return render(request, 'flair/setflair.html', {
            'username': username,
            'general_flairs': general_flairs,
            'allowed_flairs': awarded_flairs,
            'current_flair_text': stripped_flair,
            'current_flair_url': stripped_flair_url,
            'current_emoji_flair_list': current_emoji_flair_list,
            'tracker_name': tracker_name,
            'tracker_user_account_name': tracker_user_account_name,
            'tracker_flairs': tracker_flairs,
        })
    else:
        return HttpResponse('No reddit account is attached to this login. (Shadowbanned or Site-Administrator)')


def _pick_present_flair(username, custom_flairs):
    present_flair_name = "??????"
    # Don't do anything if they already have one assigned.
    for flair_type in custom_flairs:
        if flair_type.flair_id.display_name == present_flair_name:
            return
    present_flairs = list(FlairType.objects.filter(flair_type__exact="custom").filter(display_name__exact=present_flair_name))
    if not present_flairs:
        return
    # Select one at random, award it, and add it to their custom flair list.
    selected_flair = random.choice(present_flairs)
    awarded = FlairsAwarded.objects.create(flair_id=selected_flair, display_name=username)
    custom_flairs.append(awarded)


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
    awarded_flairs = check_awarded_flairs_overrides(awarded_flairs)
    awarded_flairs = remove_duplicate_awarded_flairs(awarded_flairs)
    awarded_flairs.sort(key=sort_awarded_flairs_by_order)

    flair_general_emoji_to_set = ""
    flair_award_emoji_to_set = ""
    flair_tracker_emoji_to_set = ""
    flair_tracker_text_to_set = ""
    flair_tracker_user_account = ""
    flair_template_to_set = ""

    # Backend check to enforce that no more than X (hardcoded currently as 2) award_flairs are set
    flaircap = 2

    for flair_award in awarded_flairs:
        flair_check_name = "flairtype_" + flair_award.flair_id.display_name
        if flair_check_name in request.POST:
            if flaircap > 0:
                flaircap -= 1
                flair_award_emoji_to_set = flair_award_emoji_to_set + get_award_flair_emoji_text(flair_award)

    # General/custom flairs
    custom_flairs_available = [awarded.flair_id for awarded in awarded_flairs if awarded.flair_id.flair_type == "custom"]
    general_flairs = list(FlairType.objects.filter(flair_type="general"))
    requested_flair_id = None
    if "generalflair" in request.POST:
        try:
            requested_flair_id = int(request.POST["generalflair"])
        except (ValueError, TypeError):
            pass
    if requested_flair_id:
        for flair_type in custom_flairs_available:
            if flair_type.id == requested_flair_id:
                flair_general_emoji_to_set = flair_type.reddit_flair_emoji
                break
        else:  # Didn't find their selection in custom flair so check general flairs next.
            for flair_type in general_flairs:
                if flair_type.id == requested_flair_id:
                    flair_general_emoji_to_set = flair_type.reddit_flair_emoji
                    break

    # Sort out 'list' flair section
    if "trackerflair" in request.POST:
        if request.POST["trackerflair"] == "notracker":
            # print("notracker")
            pass
        elif "trackerAccountName" in request.POST:
            # print(request.POST) # Debugging

            tracker_flairs = list(FlairType.objects.filter(flair_type__iexact="list"))
            for flairtype in tracker_flairs:
                # print(flairtype.display_name)
                # Look for through database flairs to find what they have
                if request.POST["trackerflair"] == flairtype.display_name:
                    #  Set both tracker icon and entered tracker name/id
                    flair_tracker_emoji_to_set = flairtype.reddit_flair_emoji
                    flair_tracker_text_to_set = flairtype.reddit_flair_text
                    flair_tracker_user_account = request.POST["trackerAccountName"]
                    flair_template_to_set = flairtype.reddit_flair_template_id
                    break

    # Build the flair text that will then be set
    final_flair_to_set = flair_length_builder(flair_general_emoji_to_set, flair_award_emoji_to_set, flair_tracker_emoji_to_set,
                                              flair_tracker_text_to_set, flair_tracker_user_account)

    final_flair_list = parse_flair_types(final_flair_to_set)
    set_current_assigned_flairs(username, final_flair_list)

    # Finally set the flair on the subreddit, use the template way if one is set
    if flair_template_to_set == "":
        set_flair(username, final_flair_to_set, "")
    else:
        set_flair_with_template(username, final_flair_to_set, flair_template_to_set)

    return redirect('/set')  # returns user back to /set page
