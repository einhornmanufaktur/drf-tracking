from django.shortcuts import get_list_or_404
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers, viewsets, mixins
from rest_framework.exceptions import APIException
from rest_framework_tracking.mixins import LoggingErrorsMixin, LoggingMixin
from rest_framework_tracking.models import APIRequestLog
from tests.test_serializers import ApiRequestLogSerializer
import time


class MockNoLoggingView(APIView):
    def get(self, request):
        return Response('no logging')


class MockLoggingView(LoggingMixin, APIView):
    def get(self, request):
        self.kind_of_cache_using = APIRequestLog.PART_OF_DATA_FROM_CACHE
        return Response('with logging')


class MockSlowLoggingView(LoggingMixin, APIView):
    def get(self, request):
        time.sleep(1)
        return Response('with logging')


class MockExplicitLoggingView(LoggingMixin, APIView):
    logging_methods = ['POST']

    def get(self, request):
        return Response('no logging')

    def post(self, request):
        return Response('with logging')


class MockSensitiveFieldsLoggingView(LoggingMixin, APIView):
    sensitive_fields = {'mY_fiEld'}

    def get(self, request):
        return Response('with logging')


class MockCustomCheckLoggingView(LoggingMixin, APIView):
    def _should_log(self, request, response):
        """
        Log only if response contains 'log'
        """
        return 'log' in response.data

    def get(self, request):
        return Response('with logging')

    def post(self, request):
        return Response('no recording')


class MockLoggingErrorsView(LoggingErrorsMixin, APIView):
    def get(self, request):
        raise APIException('with logging')

    def post(self, request):
        return Response('no logging')


class MockSessionAuthLoggingView(LoggingMixin, APIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response('with session auth logging')


class MockTokenAuthLoggingView(LoggingMixin, APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response('with token auth logging')


class MockJSONLoggingView(LoggingMixin, APIView):
    def get(self, request):
        return Response({'get': 'response'})

    def post(self, request):
        return Response({'post': 'response'})


class MockValidationErrorLoggingView(LoggingMixin, APIView):
    def get(self, request):
        raise serializers.ValidationError('bad input')


class Mock404ErrorLoggingView(LoggingMixin, APIView):
    def get(self, request):
        empty_qs = APIRequestLog.objects.none()
        return get_list_or_404(empty_qs)


class Mock500ErrorLoggingView(LoggingMixin, APIView):
    def get(self, request):
        raise APIException('response')


class Mock415ErrorLoggingView(LoggingMixin, APIView):
    def post(self, request):
        return request.data


class MockNameAPIView(LoggingMixin, APIView):
    def get(self, _):
        return Response('with logging')


class MockNameViewSet(LoggingMixin, viewsets.GenericViewSet, mixins.ListModelMixin):
    authentication_classes = ()
    permission_classes = []

    queryset = APIRequestLog.objects.all()
    serializer_class = ApiRequestLogSerializer


class Mock400BodyParseErrorLoggingView(LoggingMixin, APIView):
    def post(self, request):
        # raise ParseError for request with mismatched Content-Type and body:
        # (though only if it's the first access to request.data)
        request.data
        return Response('Data processed')
