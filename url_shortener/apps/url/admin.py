from django.contrib import admin

from url_shortener.apps.url.models import Url


@admin.register(Url)
class UrlAdmin(admin.ModelAdmin):
    list_display = ('slug', 'long_url', 'num_visit', 'last_visit_date')

    def last_visit_date(self, obj: Url):
        if obj.last_visit is None:
            return 'No visit'

        return obj.last_visit.date_created
