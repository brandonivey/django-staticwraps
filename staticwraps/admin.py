"""
admin action for staticwraps
"""

from django.contrib import admin

from staticwraps.models import StaticWrap


class StaticWrapAdmin(admin.ModelAdmin):
    """ humble admin for staticwraps """

    list_display = ('title', 'url_path', 'originating_site',)
    list_filter = ('originating_site',)

admin.site.register(StaticWrap, StaticWrapAdmin)
