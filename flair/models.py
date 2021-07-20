from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q, UniqueConstraint
from django.utils import timezone

# DO stuff on logging aka trigger (signal)
User = get_user_model()


class FlairDisplay(models.Model):
    id = models.BigAutoField(primary_key=True)
    is_tierd = models.BooleanField(default=False)
    reddit_flair_emoji = models.CharField("Emoji that will be added if selected.", max_length=16)
    static_image = models.CharField("Server image path. Used by wiki page.", default="", max_length=255, blank=True)
    rank = models.IntegerField(default=0)  # used to indicate set's rank

    def __str__(self):
        return self.reddit_flair_emoji


class FlairType(models.Model):
    id = models.BigAutoField(primary_key=True)
    display_name = models.CharField("Text displayed on django server for flair", max_length=64)
    # reddit_flair_emoji = models.CharField("Emoji that will be added if selected.", max_length=16)
    reddit_flair_text = models.CharField("Text that will be added if selected.", max_length=64, blank=True)
    reddit_flair_template_id = models.CharField("Reddit's Template ID to set if any", max_length=36, blank=True)
    FLAIR_TYPE_CHOICES = [('default', 'Default'), ('award', 'Award'), ('tiered-award', 'Tiered-Award'), ('temporary', 'Temporary')]
    flair_type = models.CharField("Flairs Type", default="default", choices=FLAIR_TYPE_CHOICES, max_length=255)
    note = models.CharField("An optional note about this flair.", default="", max_length=255, blank=True)
    order = models.IntegerField()  # used to order emojis/flairs when multiple added
    wiki_display = models.BooleanField(default=True)
    wiki_title = models.CharField("Title of the flair displayed on the wiki.", default="", max_length=255, blank=True)
    wiki_text = models.CharField("Information displayed on the flair wiki page.", default="", max_length=65536, blank=True)
    # static_image = models.CharField("Server image path. Used by wiki page.", default="", max_length=255, blank=True)
    flair_display = models.ManyToManyField(FlairDisplay)

    def __str__(self):
        return self.display_name

    def emoji_display(self):
        return " | ".join([str(p) for p in self.flair_display.all()])



class FlairsAwarded(models.Model):
    flair_id = models.ForeignKey(FlairType, limit_choices_to=Q(flair_type='award') | Q(flair_type='tiered-award'), null=True, on_delete=models.SET_NULL)  # Links to what flair, or null if somehow deleted
    display_name = models.CharField("A reddit username", max_length=20)  # Reddit names can be max 20 characters
    date_added = models.DateTimeField(default=timezone.now, blank=True)
    note = models.CharField("An optional note on why this was awarded.", default="", max_length=255, blank=True)

    def __str__(self):
        return "{} : {}".format(self.display_name, self.flair_id)


class ActionLogging(models.Model):
    id = models.BigAutoField(primary_key=True)
    action = models.CharField("Action attempted.", max_length=256)
    action_info = models.CharField("Info related to the action.", max_length=256)
    reddit_name = models.CharField("Redditor name.", max_length=20)
    error = models.CharField("Error message.", max_length=256)
    timestamp = models.DateTimeField('Timestamp of event.', default=timezone.now)
    user_agent = models.CharField("The user-agent string from the user.", max_length=65536, null=True)

    def __str__(self):
        return "id=({}) action=({}) action_info=({}) reddit_name=({}) timestamp=({})".format(self.id, self.action, self.action_info, self.reddit_name, self.timestamp)
