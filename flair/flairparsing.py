import re

from flair.models import FlairsAwarded, FlairType

"""A set of functions for turning strings to recognised flair emoji"""


def colon_emoji_strip(string):
    """Takes string and removes ALL :emoji: from the front in ':' text ':' format."""
    if string is None:
        return ''  # If empty or None return empty string
    return re.sub(':.+?:', '', string)


def make_url_of_flair_text(string):
    """Takes string that MAY not start with http://, if it doesn't it prepends that elsewise returns"""
    if string is None:
        return ''  # If empty or None return empty string

    if string.startswith('https://'):
        return string
    else:
        string = "https://" + string

    return string


def colon_emoji_strip_single(string):
    """Takes string and removes ONE :emoji: from the front in ':' text ':' format."""
    return re.sub(':.+?:', '', string, count=1)


def get_all_colon_emoji(string):
    """Takes string and returns a list of stings in (:emoji:) ':' text ':' format."""
    if string is None:
        return ''  # If empty or None return empty string
    reg_exp_obj = re.compile(':.+?:')
    return reg_exp_obj.findall(string)


def users_current_awarded_flair_icons(flair_string):
    """Builds a list of FlairType flair's the user is currently using. No validation on a user, just shows what they have already."""
    awarded_flairs = []

    if flair_string is None:
        return awarded_flairs  # If empty or None return nothing

    ls = get_all_colon_emoji(flair_string)
    database = FlairType.objects.all()

    for emoji in ls:
        for flair_type in database:
            if emoji == flair_type.reddit_flair_emoji:
                awarded_flairs.append(flair_type)

    return awarded_flairs


def tracker_type(flair_string):
    """Reads a flair and returns the tracker's name from the database."""

    ls = get_all_colon_emoji(flair_string)

    if not ls:  # Does the current flair have emoji?
        pass  # Now skip over for legacy flairs to be checked below
        # return "notracker"  # No emoji found
    else:
        database = FlairType.objects.all()
        for emoji in ls:
            for flair_type in database:
                if emoji == flair_type.reddit_flair_emoji:
                    if flair_type.flair_type == 'default':
                        return flair_type.display_name

    # This covers for when the account doesn't have a tracker emoji (ie: no space or if we allow as a policy) or is a legacy flair and is matching on URL's instead

    if not flair_string:
        return "notracker"
    if "anidb.net" in flair_string:
        return "Anidb"
    if "anilist.co" in flair_string:
        return "Anilist"
    if "anime-planet.com" in flair_string:
        return "animeplanet"
    if "kitsu.io" in flair_string:
        return "Kitsu"
    if "myanimelist.net" in flair_string:
        return "MAL"

    # Flair must either be; be an old legacy flair without a correct website. Or award-emoji only, with no tracker info.
    return "notracker"


def flair_length_builder(flair_award_emoji_to_set, flair_tracker_emoji_to_set, flair_tracker_text_to_set,
                         flair_tracker_user_account):
    """Flair is limited to 64 characters, this function runs filters on the entered text and tries and cuts down longer flairs to fit"""
    """It is assumed the longest tracker_text_to_set will be 51 characters. Eg:"""
    """https://anime-planet.com/users/12345678901234567890"""
    """This leaves the remaining space for award emoji"""

    # Run text validation on the tracker-account they entered:
    validated_tracker_user_account = tracker_account_name_validation(flair_tracker_user_account)

    full_length_string = flair_award_emoji_to_set + flair_tracker_emoji_to_set + flair_tracker_text_to_set + validated_tracker_user_account
    if len(full_length_string) <= 64:
        # Great, no problems return it
        return full_length_string

    # Remove the "https://" and see if that fits
    flair_tracker_text_to_set = flair_tracker_text_to_set.replace("https://", "")
    full_length_string = flair_award_emoji_to_set + flair_tracker_emoji_to_set + flair_tracker_text_to_set + validated_tracker_user_account
    if len(full_length_string) <= 64:
        return full_length_string

    # Cut the tracker emoji as well and see if that fits
    full_length_string = flair_award_emoji_to_set + flair_tracker_text_to_set + validated_tracker_user_account
    if len(full_length_string) <= 64:
        return full_length_string

    # Just have the tracker site emoji and the users username
    full_length_string = flair_award_emoji_to_set + flair_tracker_emoji_to_set + validated_tracker_user_account
    if len(full_length_string) <= 64:
        return full_length_string

    #  TODO: Somethings wrong, just give them their award emoji. Is this the best workflow?
    return flair_award_emoji_to_set


def strip_flair_to_tracker_account_name(string):
    """Takes a subreddit set flair and attempts to remove everything but the tracker's account name. Returns a blank string if it can't."""

    if string is None:
        return ''

    # Remove :emoji:
    string = colon_emoji_strip(string)

    # Remove https://
    https_filter = re.compile(re.escape('https://'), re.IGNORECASE)
    http_filter = re.compile(re.escape('http://'), re.IGNORECASE)
    string = https_filter.sub('', string)
    string = http_filter.sub('', string)

    # Remove tracker's
    MAL1_filter = re.compile(re.escape('myanimelist.net/profile/'), re.IGNORECASE)
    MAL2_filter = re.compile(re.escape('myanimelist.net/animelist/'), re.IGNORECASE)
    Anilist_filter = re.compile(re.escape('anilist.co/user/'), re.IGNORECASE)
    Kitsu_filter = re.compile(re.escape('kitsu.io/users/'), re.IGNORECASE)
    Anidb_filter = re.compile(re.escape('anidb.net/user/'), re.IGNORECASE)
    animeplanet_filter = re.compile(re.escape('anime-planet.com/users/'), re.IGNORECASE)

    string = MAL1_filter.sub('', string)
    string = MAL2_filter.sub('', string)
    string = Anilist_filter.sub('', string)
    string = Kitsu_filter.sub('', string)
    string = Anidb_filter.sub('', string)
    string = animeplanet_filter.sub('', string)

    # All flairs set by the flair server will now be good. Legacy set flairs maybe not.

    if len(string) <= 20:
        if '/' not in string:
            # All flairs set by the flair-server get here. Legacy flairs that were formatted well do to.
            return string
        else:
            # Has '/animelist' or something additional, lets not risk dealing with it
            return ''
    else:
        # Flair too long, must be something legacy we can't handle
        return ''


def tracker_account_name_validation(string):
    # MAL: letters, numbers, underscores and dashes only
    # Anilist: The user name may only contain letters and numbers.
    # anime planet:  Only letters or numbers (min 3, max 20)
    # kitsu name can be anything, but 'slug' (url) is only letters numbers and underscores
    # Allows use of '/' so that you can add /animelist to end of your tracker name (and thus URL) if there is room available.

    # Allow only alphanumeric characters, also underscore and dash
    string = re.sub(r'[^a-zA-Z0-9_\-/]+', '', string)

    return string


def find_already_set_flairs(all_awarded_flairs, current_selected_flair_list):
    """Edits the all_awarded_flairs list to set if a flair is 'checked' and in the users flair already."""
    ls = []

    for awarded_flair in all_awarded_flairs:

        matched = False
        for currently_selected_flair in current_selected_flair_list:
            if awarded_flair.flair_id == currently_selected_flair:
                matched = True
        if matched:
            awarded_flair.flair_id.checked = True
        else:
            awarded_flair.flair_id.checked = False
        ls.append(awarded_flair)

    return ls


def remove_duplicate_awarded_flairs(all_awarded_flairs):
    """Edit find all award flairs that have the same type (duplicates) and remove one, putting information of there being more into a field"""

    ls = []
    flair_id_ls = []

    for awarded_flair in all_awarded_flairs:
        if awarded_flair.flair_id in flair_id_ls:
            continue  # Done this ID already

        count = 0
        for flair in all_awarded_flairs:
            if awarded_flair.flair_id == flair.flair_id:
                count = count+1
        if count > 1:
            awarded_flair.awarded_count = count
            print(awarded_flair)
        flair_id_ls.append(awarded_flair.flair_id)  # Used to avoid duplicates by ID instead of object
        ls.append(awarded_flair)

    return ls
