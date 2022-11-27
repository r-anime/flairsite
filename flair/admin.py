from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html

from .models import FlairType, FlairsAwarded, FlairAssigned, ActionLogging


class FlairsAwardedAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'flair_id', 'date_added', 'note', 'override', 'override_flair')
    list_filter = ['date_added']
    search_fields = ['display_name']


class FlairsAssignedAdmin(admin.ModelAdmin):
    list_display = ('reddit_username', 'flair_id', 'date_added')
    list_filter = ['date_added']
    search_fields = ['reddit_username']


class FlairTypeAdmin(admin.ModelAdmin):
    list_display = (
        'display_name',
        'image_tag',
        'flair_type',
        'assigned_count',
        'note',
        'wiki_display',
        'order',
        'reddit_flair_emoji',
        'reddit_flair_text',
        'reddit_flair_template_id',
        )

    def image_tag(self, obj):
        if obj.static_image:
            return format_html('<img src="{0}" style="height:16px;" />'.format(obj.static_image))
        elif not obj.display_image:
            return
        return format_html('<img src="{0}" style="height:16px;" />'.format(obj.display_image.url))

    def assigned_count(self, obj):
        return obj.assigned_count

    assigned_count.admin_order_field = 'assigned_count'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(assigned_count=Count("flairassigned__flair_id"))
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


admin.site.register(FlairType, FlairTypeAdmin)
admin.site.register(FlairsAwarded, FlairsAwardedAdmin)
admin.site.register(FlairAssigned, FlairsAssignedAdmin)
admin.site.register(ActionLogging, ActionLoggingAdmin)
