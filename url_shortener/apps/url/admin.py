from django.contrib import admin

from url_shortener.apps.url.models import Url


@admin.register(Url)
class UrlAdmin(admin.ModelAdmin):
    fields = ('slug', 'long_url', 'num_visit', 'last_visit')
