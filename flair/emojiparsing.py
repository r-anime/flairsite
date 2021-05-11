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
        return "notracker"  # No emoji found
    else:
        database = FlairType.objects.all()
        for emoji in ls:
            for flair_type in database:
                if emoji == flair_type.reddit_flair_emoji:
                    if flair_type.flair_type == 'default':
                        return flair_type.display_name
    return "notracker"  # has emoji but no tracker
