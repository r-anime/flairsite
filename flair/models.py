from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

# DO stuff on logging aka trigger (signal)
User = get_user_model()


class FlairType(models.Model):
    id = models.BigAutoField(primary_key=True)
    display_name = models.CharField("Text displayed on django server for flair", max_length=64)
    reddit_flair_emoji = models.CharField("Emoji that will be added if selected.", max_length=16)
    reddit_flair_text = models.CharField("Text that will be added if selected.", max_length=64, blank=True)
    reddit_flair_template_id = models.CharField("Reddit's Template ID to set if any", max_length=36, blank=True)
    flair_type = models.CharField("Flairs Type", default="default", max_length=255)
    note = models.CharField("An optional note about this flair.", default="", max_length=255, blank=True)
    order = models.IntegerField()  # used to order emojis/flairs when multiple added
    wiki_display = models.BooleanField(default=False)
    wiki_text = models.CharField("Information displayed on the flair wiki page.", default="", max_length=65536, blank=True)
    static_image = models.CharField("Server image path. Used by wiki page.", default="", max_length=255, blank=True)

    def __str__(self):
        return self.display_name


class FlairsAwarded(models.Model):
    flair_id = models.ForeignKey(FlairType, null=True, on_delete=models.SET_NULL)  # Links to what flair, or null if somehow deleted
    display_name = models.CharField("A reddit username", max_length=20)  # Reddit names can be max 20 characters
    date_added = models.DateTimeField(default=timezone.now, blank=True)
    note = models.CharField("An optional note on why this was awarded.", default="", max_length=255, blank=True)

    def __str__(self):
        return "{} : {}".format(self.display_name, self.flair_id)