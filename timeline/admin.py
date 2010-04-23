from django.contrib import admin
from timeline.models import Timeline


class TimelineAdmin(admin.ModelAdmin):
    list_display = ('user', 'object', 'content_type', 'time')

admin.site.register(Timeline, TimelineAdmin)
