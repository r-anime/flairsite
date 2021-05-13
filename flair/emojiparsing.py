import re

from flair.models import FlairsAwarded, FlairType

"""A set of functions for turning strings to recognised flair emoji"""


def colon_emoji_strip(string):
    """Takes string and removes ALL :emoji: from the front in ':' text ':' format."""
    if string is None:
        return ''  # If empty or None return empty string
    return re.sub(':.+?:', '', string)


def colon_emoji_strip_single(string):
    """Takes string and removes ONE :emoji: from the front in ':' text ':' format."""
    return re.sub(':.+?:', '', string, count=1)


def get_all_colon_emoji(string):
    """Takes string and returns a list of stings in (:emoji:) ':' text ':' format."""
    if string is None:
        return ''  # If empty or None return empty string
    reg_exp_obj = re.compile(':.+?:')
    return reg_exp_obj.findall(string)


def flair_icon_builder(flair_string):
    """Builds a list of static/images to display instead of the text emoji in a flair. No validation on a user."""
    file_list = []

    if flair_string is None:
        return file_list  # If empty or None return nothing

    ls = get_all_colon_emoji(flair_string)
    database = FlairType.objects.all()

    for emoji in ls:
        for flair_type in database:
            if emoji == flair_type.reddit_flair_emoji:
                file_list.append(flair_type.static_image)

    return file_list


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

    # This covers for when the account doesn't have a tracker emoji (space or policy) or is a legacy flair and matches on URL's instead

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
                         flair_tracker_user_to_set):
    """Flair is limited to 64 characters, this method tries and cuts down longer flairs to fit"""
    """It is assumed the longest tracker_text_to_set will be 51 characters. Eg:"""
    """https://anime-planet.com/users/12345678901234567890"""
    """This leaves the remaining space for award emoji"""

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

