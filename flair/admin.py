from django.contrib import admin

from .models import FlairType, FlairsAwarded, ActionLogging


class FlairsAwardedAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'flair_id', 'date_added', 'note', 'override', 'override_flair')
    list_filter = ['date_added']
    search_fields = ['display_name']


class FlairTypeAdmin(admin.ModelAdmin):
    list_display = (
        'display_name',
        'id',
        'display_image',
        'order',
        'reddit_flair_emoji',
        'reddit_flair_text',
        'reddit_flair_template_id',
        'flair_type',
        'note',
        'wiki_display',
        'wiki_title',
        'wiki_text',
        'static_image'
        )


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


admin.site.register(FlairType, FlairTypeAdmin)
admin.site.register(FlairsAwarded, FlairsAwardedAdmin)
admin.site.register(ActionLogging, ActionLoggingAdmin)
