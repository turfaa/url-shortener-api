from django.apps import apps
from django.urls import reverse
from rest_framework import serializers
from rest_framework.request import Request

Url = apps.get_model('url', 'Url')
UrlVisit = apps.get_model('url', 'Visit')


class UrlVisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = UrlVisit
        fields = ('date_created',)
        read_only_fields = ('date_created',)


class UrlSerializer(serializers.ModelSerializer):
    short_url = serializers.SerializerMethodField()

    def get_short_url(self, url: Url) -> str:
        request: Request = self.context.get('request')
        return request.build_absolute_uri(reverse('url-resolve', kwargs={'slug': url.slug}))

    class Meta:
        model = Url
        fields = ('date_created', 'long_url', 'short_url', 'num_visit')
        read_only_fields = ('date_created',)


class BatchUrlSerializer(serializers.Serializer):
    urls = UrlSerializer(many=True)

    def create(self, validated_data):
        urls = list(map(lambda data: Url(**data), validated_data.get('urls')))

        for url in urls:
            url.save()

        return {'urls': urls}
