from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from rest_framework.generics import ListCreateAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from url_shortener.apps.url.models import Url
from url_shortener.apps.url.serializers import UrlSerializer, BatchUrlSerializer
from url_shortener.services.ip_address import IpAddressService


class UrlView(ListCreateAPIView):
    queryset = Url.objects.all()
    serializer_class = UrlSerializer
    permission_classes = ()

    def get_serializer_context(self):
        return {'request': self.request}


class BatchUrlCreateView(APIView):
    permission_classes = ()

    def get_serializer_context(self):
        return {'request': self.request}

    def post(self, request: Request, *args, **kwargs) -> HttpResponse:
        serializer = BatchUrlSerializer(data=request.data, context=self.get_serializer_context())

        if not serializer.is_valid(raise_exception=True):
            return Response({'message': 'Not a valid batch url create query.'}, status=HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data)


class ResolveUrlView(View):
    permission_classes = ()

    def get(self, request: Request, slug: str) -> HttpResponse:
        url: Url = get_object_or_404(Url, slug=slug)
        url.add_visit(IpAddressService(request).get_ip_address())
        return redirect(url.long_url)
