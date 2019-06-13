from django.db import models

from url_shortener.apps.common.abstract_models import DateCreatable
from url_shortener.services.url import UrlService


class Url(DateCreatable):
    # date_created

    long_url = models.URLField()
    slug = models.CharField(max_length=32, unique=True)

    @property
    def last_visit(self) -> 'Visit':
        return self.visits.last()

    @property
    def num_visit(self) -> int:
        return self.visits.count()

    def add_visit(self, ip_address: str = '') -> None:
        Visit.objects.create(url=self, ip_address=ip_address)

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            length = 3
            url_service = UrlService()

            slug = url_service.generate_slug(length)
            while Url.objects.filter(slug=slug).count() > 0:
                length += 1
                slug = url_service.generate_slug(length)

            self.slug = slug

        return super().save(*args, **kwargs)

    class Meta:
        ordering = ('-date_created',)

    def __unicode__(self) -> str:
        return '{}: {}'.format(self.slug, self.long_url)


class Visit(DateCreatable):
    url = models.ForeignKey(Url, related_name='visits',
                            on_delete=models.CASCADE)
    ip_address = models.CharField(max_length=32, blank=True)

    class Meta:
        ordering = ('-date_created',)
