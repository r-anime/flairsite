from django import forms
from django.contrib import admin, messages
from django.contrib.admin.helpers import ActionForm
from django.db.models import Count
from django.utils.html import format_html


from .models import Anime, FlairType, FlairsAwarded, FlairAssigned, ActionLogging


class AnimeAdmin(admin.ModelAdmin):
    list_display = ('title_jp', 'title_en', 'alias')
    search_fields = ['title_jp', 'title_en', 'alias']


class FlairsAwardedAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'flair_id', 'date_added', 'note', 'override', 'override_flair')
    list_filter = ['date_added']
    search_fields = ['display_name', 'flair_id__display_name']


class FlairsAssignedAdmin(admin.ModelAdmin):
    list_display = ('reddit_username', 'flair_id', 'date_added')
    list_filter = ['date_added']
    search_fields = ['reddit_username', 'flair_id__display_name']


class UpdateFlairTypeActionForm(ActionForm):
    flair_type = forms.ChoiceField(choices=FlairType.FLAIR_TYPE_CHOICES, required=False)


def update_flair_type(modeladmin, request, queryset):
    flair_type = request.POST['flair_type']
    queryset.update(flair_type=flair_type)
    modeladmin.message_user(request, f"Successfully changed flair type for {queryset.count()} rows", messages.SUCCESS)


update_flair_type.short_description = "Update flair type of selected rows"


class FlairTypeAdmin(admin.ModelAdmin):
    action_form = UpdateFlairTypeActionForm
    actions = [update_flair_type]
    search_fields = ['display_name', 'flair_type', 'note']
    list_display = (
        'display_name',
        'image_tag',
        'flair_type',
        'currently_set_count',
        'note',
        'anime',
        'wiki_display',
        'order',
        'reddit_flair_emoji',
        'reddit_flair_text',
        'reddit_flair_template_id',
        )

    def image_tag(self, obj):
        if not obj.display_image:
            return
        return format_html('<img src="{0}" style="height:16px;" />'.format(obj.display_image.url))

    def currently_set_count(self, obj):
        return obj.currently_set_count

    currently_set_count.admin_order_field = 'currently_set_count'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(currently_set_count=Count("flairassigned__flair_id"))
        return queryset


class ActionLoggingAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'action',
        'action_info',
        'reddit_name',
        'error',
        'user_agent',
        'timestamp'
        )
    search_fields = ['reddit_name']


admin.site.register(Anime, AnimeAdmin)
admin.site.register(FlairType, FlairTypeAdmin)
admin.site.register(FlairsAwarded, FlairsAwardedAdmin)
admin.site.register(FlairAssigned, FlairsAssignedAdmin)
admin.site.register(ActionLogging, ActionLoggingAdmin)
