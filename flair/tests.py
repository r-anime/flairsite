from django.test import TestCase
from .redditflair import *
from dotenv import load_dotenv
from flair.models import FlairType, FlairsAwarded


def setup_db():
    q = FlairType(id=1, display_name="Cake", reddit_flair_emoji=":cake:", order=1)
    q.save()
    q = FlairType(id=2, display_name="Upvote", reddit_flair_emoji=":upvote:", order=2)
    q.save()
    q = FlairType(id=3, display_name="Doge", reddit_flair_emoji=":doge:", order=3)
    q.save()

    f = FlairsAwarded(flair_id=FlairType.objects.get(id=1), display_name="spez")
    f.save()
    f = FlairsAwarded(flair_id=FlairType.objects.get(id=2), display_name="spez")
    f.save()
    f = FlairsAwarded(flair_id=FlairType.objects.get(id=1), display_name="forth")
    f.save()
    f = FlairsAwarded(flair_id=FlairType.objects.get(id=3), display_name="forth")
    f.save()


class FlairModelTests(TestCase):
    def test_setup_db(self):
        setup_db()
        self.assertIs(FlairType.objects.get(pk=1).display_name == "Cake", True)
        self.assertIs(FlairType.objects.get(pk=2).display_name == "Upvote", True)
        self.assertIs(FlairsAwarded.objects.get(pk=1).display_name == "spez", True)
        self.assertIs(FlairsAwarded.objects.get(pk=1).flair_id == FlairType.objects.get(pk=1), True)


    def test_user_get_all_FlairsAwarded(self):
        username = "spez"
        setup_db()

        awarded_flairs = FlairsAwarded.objects.filter(display_name=username)
        # awardedFlairs = FlairsAwarded.objects.filter(flair_id=FlairType.objects.get(pk=1))
        print(awarded_flairs)

    # def test_get_data(self):
    #     self.assertIs(FlairType.objects.get(pk=1).display_name == "Cake", True)



class RedditFlairTests(TestCase):
    reddit_setup()  # TODO: make this into a test
    # TODO: Make 'subreddit' and input (KobayashiCoderbus)
    global username
    username = "spez"  # TODO: Pull this from settings file or something - this is the user to test setting on

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

    def test_set_flair(self):
        delete_flair(username)
        set_flair(username, ":cake::cake:", "")
        # print(get_flair(username))
        self.assertIs(get_flair(username).get('flair_text') == ":cake::cake:", True)
        # self.assertIs(get_flair(username).get('flair_css_class') == "", True) #TODO: flair_template_id - requires templates setup?
        delete_flair(username)

    def test_set_flair_then_delete(self):
        delete_flair(username)
        set_flair(username, ":cake::cake:", "")
        # print(get_flair(username).get('flair_text'))
        delete_flair(username)
        self.assertIs(get_flair(username).get('flair_text') == "", True)

    def test_check_karma_value(self):
        karma = get_user_karma(username)
        self.assertIs(karma > 0, True)



# TODO: make this
# def test_set_flair_user_doesnt_exist(self):
#     set_flair("xgauyshxijkoasx28)@(*", ":cake::cake:", "css")

# test setting flair on user that doesn't exist.


# setflair
# getflair()
#

#
# class QuestionModelTests(TestCase):
#     def test_was_published_recently_with_future_question(self):
#         """
#         was_published_recently() returns False for questions whose pub_date
#         is in the future.
#         """
#         time = timezone.now() + datetime.timedelta(days=30)
#         future_question = Question(pub_date=time)
#         self.assertIs(future_question.was_published_recently(), False)
#
#     def test_was_published_recently_with_old_question(self):
#         """
#         was_published_recently() returns False for questions whose pub_date
#         is older than 1 day.
#         """
#         time = timezone.now() - datetime.timedelta(days=1, seconds=1)
#         old_question = Question(pub_date=time)
#         self.assertIs(old_question.was_published_recently(), False)
#
#     def test_was_published_recently_with_recent_question(self):
#         """
#         was_published_recently() returns True for questions whose pub_date
#         is within the last day.
#         """
#         time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
#         recent_question = Question(pub_date=time)
#         self.assertIs(recent_question.was_published_recently(), True)
#
# def create_question(question_text, days):
#     """
#     Create a question with the given `question_text` and published the
#     given number of `days` offset to now (negative for questions published
#     in the past, positive for questions that have yet to be published).
#     """
#     time = timezone.now() + datetime.timedelta(days=days)
#     return Question.objects.create(question_text=question_text, pub_date=time)
#
#
# class QuestionIndexViewTests(TestCase):
#     def test_no_questions(self):
#         """
#         If no questions exist, an appropriate message is displayed.
#         """
#         response = self.client.get(reverse('flair:index'))
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, "No flair are available.")
#         self.assertQuerysetEqual(response.context['latest_question_list'], [])
#
#     def test_past_question(self):
#         """
#         Questions with a pub_date in the past are displayed on the
#         index page.
#         """
#         create_question(question_text="Past question.", days=-30)
#         response = self.client.get(reverse('flair:index'))
#         self.assertQuerysetEqual(
#             response.context['latest_question_list'],
#             ['<Question: Past question.>']
#         )
#
#     def test_future_question(self):
#         """
#         Questions with a pub_date in the future aren't displayed on
#         the index page.
#         """
#         create_question(question_text="Future question.", days=30)
#         response = self.client.get(reverse('flair:index'))
#         self.assertContains(response, "No flair are available.")
#         self.assertQuerysetEqual(response.context['latest_question_list'], [])
#
#     def test_future_question_and_past_question(self):
#         """
#         Even if both past and future questions exist, only past questions
#         are displayed.
#         """
#         create_question(question_text="Past question.", days=-30)
#         create_question(question_text="Future question.", days=30)
#         response = self.client.get(reverse('flair:index'))
#         self.assertQuerysetEqual(
#             response.context['latest_question_list'],
#             ['<Question: Past question.>']
#         )
#
#     def test_two_past_questions(self):
#         """
#         The questions index page may display multiple questions.
#         """
#         create_question(question_text="Past question 1.", days=-30)
#         create_question(question_text="Past question 2.", days=-5)
#         response = self.client.get(reverse('flair:index'))
#         self.assertQuerysetEqual(
#             response.context['latest_question_list'],
#             ['<Question: Past question 2.>', '<Question: Past question 1.>']
#         )
#
# class QuestionDetailViewTests(TestCase):
#     def test_future_question(self):
#         """
#         The detail view of a question with a pub_date in the future
#         returns a 404 not found.
#         """
#         future_question = create_question(question_text='Future question.', days=5)
#         url = reverse('flair:detail', args=(future_question.id,))
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 404)
#
#     def test_past_question(self):
#         """
#         The detail view of a question with a pub_date in the past
#         displays the question's text.
#         """
#         past_question = create_question(question_text='Past Question.', days=-5)
#         url = reverse('flair:detail', args=(past_question.id,))
#         response = self.client.get(url)
#         self.assertContains(response, past_question.question_text)
