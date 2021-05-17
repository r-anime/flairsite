from django.test import TestCase
from .redditflair import *
from dotenv import load_dotenv
from flair.models import FlairType, FlairsAwarded, ActionLogging
from .flairparsing import *


def setup_db():
    q = FlairType(id=1, display_name="Cake", reddit_flair_emoji=":cake:", order=1,
                  static_image='/static/flairs/bot.png')
    q.save()
    q = FlairType(id=2, display_name="Upvote", reddit_flair_emoji=":upvote:", order=2,
                  static_image='/static/flairs/upvote.png')
    q.save()
    q = FlairType(id=3, display_name="Star", reddit_flair_emoji=":star:", order=3,
                  static_image='/static/flairs/star.png')
    q.save()
    q = FlairType(id=7, display_name="Anilist", reddit_flair_emoji=":ANI:", order=96,
                  static_image='/static/flairs/Anilist.png')
    q.save()

    f = FlairsAwarded(flair_id=FlairType.objects.get(id=1), display_name="spez")
    f.save()
    f = FlairsAwarded(flair_id=FlairType.objects.get(id=2), display_name="spez")
    f.save()
    f = FlairsAwarded(flair_id=FlairType.objects.get(id=1), display_name="forth")
    f.save()
    f = FlairsAwarded(flair_id=FlairType.objects.get(id=3), display_name="forth")
    f.save()


class ActionLoggingTests(TestCase):
    reddit_setup()

    def test_direct_insert_to_log(self):
        global username
        username = "spez"
        example_flair = ':cake::star::ANI:https://anilist.co/user/spez'
        q = ActionLogging(
            action="set_flair",
            action_info=example_flair,
            reddit_name="spez",
            error="",
        )
        q.save()
        self.assertIs(ActionLogging.objects.get(pk=1).reddit_name == "spez", True)
        self.assertIs(ActionLogging.objects.get(pk=1).action == "set_flair", True)
        self.assertIs(ActionLogging.objects.get(pk=1).action_info == example_flair, True)

    def test_flairset_creates_log(self):
        example_flair = ':cake::cake:'
        set_flair("spez", example_flair, "")
        all_log = ActionLogging.objects.filter(reddit_name=username)
        self.assertIs(ActionLogging.objects.get(pk=1).reddit_name == "spez", True)
        self.assertIs(ActionLogging.objects.get(pk=1).action == "set_flair", True)
        self.assertIs(ActionLogging.objects.get(pk=1).action_info == example_flair, True)

    def test_deleteflair_creates_log(self):
        delete_flair(username)
        all_log = ActionLogging.objects.filter(reddit_name=username)
        self.assertIs(ActionLogging.objects.get(pk=1).reddit_name == "spez", True)
        self.assertIs(ActionLogging.objects.get(pk=1).action == "delete_flair", True)


class FlairParsingTests(TestCase):
    def test_strip_all(self):
        example_flair = ':cake::star::ANI:https://anilist.co/user/spez'
        colon_emoji_stripper_flair = colon_emoji_strip(example_flair)
        self.assertIs('https://anilist.co/user/spez' == colon_emoji_stripper_flair, True)

    def test_strip_single(self):
        example_flair = ':cake::star::ANI:https://anilist.co/user/spez'
        colon_emoji_stripper_flair = colon_emoji_strip_single(example_flair)
        self.assertIs(':star::ANI:https://anilist.co/user/spez' == colon_emoji_stripper_flair, True)

    def test_get_all_enoji(self):
        example_flair = ':cake::star::ANI:https://anilist.co/user/spez'
        all_colon_emoji = get_all_colon_emoji(example_flair)
        ls = [':cake:', ':star:', ':ANI:']
        self.assertIs(ls == all_colon_emoji, True)

    def test_get_all_enoji_none(self):
        example_flair = ''
        all_colon_emoji = get_all_colon_emoji(example_flair)
        ls = []
        self.assertIs(ls == all_colon_emoji, True)

    def test_get_all_enoji_with_database(self):
        setup_db()
        example_flair = ':cake::upvote::ANI:https://anilist.co/user/spez'
        ls = [FlairType.objects.get(id=1), FlairType.objects.get(id=2), FlairType.objects.get(id=7)]
        awarded_flairs_list = users_current_awarded_flair_icons(example_flair)
        self.assertIs(ls == awarded_flairs_list, True)

    def test_strip_to_tracker_name(self):
        MAL = ':MAL:https://myanimelist.net/profile/spez'
        Anilist = ':star::ANI:HTTPS://anilist.co/user/spez'
        Kitsu = ':Kitsu:http://kitsu.io/users/spez'
        Anidb = ':star::anidb:https://anidb.net/user/spez'
        animeplanet = ':star::AP:https://anime-planet.com/users/spez'
        longname = ':cake::upvote::star:anime-planet.com/users/spezspezspezspezspez'
        empty = ''
        existing1 = 'https://anilist.co/user/badspler/animelist'
        existing2 = 'https://www.imdb.com/list/ls123123123/'

        self.assertIs(strip_flair_to_tracker_account_name(MAL) == 'spez', True)
        self.assertIs(strip_flair_to_tracker_account_name(Anilist) == 'spez', True)
        self.assertIs(strip_flair_to_tracker_account_name(Kitsu) == 'spez', True)
        self.assertIs(strip_flair_to_tracker_account_name(Anidb) == 'spez', True)
        self.assertIs(strip_flair_to_tracker_account_name(animeplanet) == 'spez', True)
        self.assertIs(strip_flair_to_tracker_account_name(longname) == 'spezspezspezspezspez', True)
        self.assertIs(strip_flair_to_tracker_account_name(empty) == '', True)
        self.assertIs(strip_flair_to_tracker_account_name(existing1) == '', True)
        self.assertIs(strip_flair_to_tracker_account_name(existing2) == '', True)


class FlairModelTests(TestCase):
    def test_setup_db(self):
        setup_db()
        self.assertIs(FlairType.objects.get(pk=1).display_name == "Cake", True)
        self.assertIs(FlairType.objects.get(pk=2).display_name == "Upvote", True)
        self.assertIs(FlairsAwarded.objects.get(pk=1).display_name == "spez", True)
        self.assertIs(FlairsAwarded.objects.get(pk=1).flair_id == FlairType.objects.get(pk=1), True)

    def test_user_get_FlairsAwarded(self):
        setup_db()
        username = "spez"
        awarded_flairs = FlairsAwarded.objects.filter(display_name=username)
        self.assertIs(awarded_flairs.first().flair_id.display_name == 'Cake', True)



class RedditFlairTests(TestCase):
    reddit_setup()  # TODO: make this into a test
    global username
    username = "spez"

    def test_get_environ(self):
        load_dotenv()
        print('DEBUG: ' + os.environ.get('DEBUG'))

    def test_check_user_exists(self):
        self.assertIs(check_user_exists(username), True)

    def test_ensure_clear_flair_start(self):
        delete_flair(username)
        # print(get_flair(username))
        self.assertIs(get_flair(username).get('flair_text') == "", True)
        # self.assertIs(get_flair(username).get('flair_css_class') == "", True)

    # def test_set_flair(self):
    #     set_flair(username, ":cake:", "")
    #     # print(get_flair(username))
    #     #  TODO: Sometimes this test fails, cache maybe returning old value because of speed?
    #     print('flair print:')
    #     print(get_flair(username).get('flair_text'))
    #     self.assertIs(get_flair(username).get('flair_text') == ":cake:", True)
    #     delete_flair(username)

    def test_set_flair_then_delete(self):
        delete_flair(username)
        set_flair(username, ":cake::cake:", "")
        # print(get_flair(username).get('flair_text'))
        delete_flair(username)
        self.assertIs(get_flair(username).get('flair_text') == "", True)

    def test_check_karma_value(self):
        karma = get_user_karma(username)
        self.assertIs(karma > 0, True)
