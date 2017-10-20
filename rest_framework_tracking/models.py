from django.db import models
from django.conf import settings
from django.utils.six import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _l

from rest_framework_tracking.managers import PrefetchUserManager


@python_2_unicode_compatible
class BaseAPIRequestLog(models.Model):
    """Logs API requests by time, user, etc"""

    ALL_DATA_FROM_CACHE = 100
    PART_OF_DATA_FROM_CACHE = 50
    NOTHING_FROM_CACHE = 0
    KIND_OF_CACHE_USING = (
        (ALL_DATA_FROM_CACHE, _l('All data was given from cache')),
        (PART_OF_DATA_FROM_CACHE, _l('Part of data was given from cache')),
        (NOTHING_FROM_CACHE, _l('Nothing was given from cache')),
    )

    # user or None for anon
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)

    # id of request
    request_id = models.CharField(max_length=100, db_index=True, null=True, blank=True)

    # timestamp of request
    requested_at = models.DateTimeField(db_index=True)

    # number of milliseconds to respond
    response_ms = models.PositiveIntegerField(default=0)

    # request path
    path = models.CharField(max_length=200, db_index=True)

    # view called by the path
    view = models.CharField(max_length=200, db_index=True)

    # method of the view
    view_method = models.CharField(max_length=200, db_index=True)

    # remote IP address of request
    remote_addr = models.GenericIPAddressField()

    # originating host of request
    host = models.URLField()

    # HTTP method (GET, etc)
    method = models.CharField(max_length=10)

    # query params
    query_params = models.TextField(null=True, blank=True)

    # POST body data
    data = models.TextField(null=True, blank=True)

    # response
    response = models.TextField(null=True, blank=True)

    # Shows degree of using cache (all data was given from cache or partially or nothing).
    kind_of_cache_using = models.PositiveSmallIntegerField(choices=KIND_OF_CACHE_USING, null=True, blank=True)

    # error traceback
    errors = models.TextField(null=True, blank=True)

    # status code
    status_code = models.PositiveIntegerField(null=True, blank=True)

    # custom manager
    objects = PrefetchUserManager()

    class Meta:
        abstract = True
        verbose_name = 'API Request Log'

    def __str__(self):
        return '{} {}'.format(self.method, self.path)


class APIRequestLog(BaseAPIRequestLog):
    pass
