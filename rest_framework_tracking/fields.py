# from django.db.models.fields import PositiveSmallIntegerField
# from django.utils.translation import ugettext_lazy as _l
#
#
# class KindOfCacheUsingField(PositiveSmallIntegerField):
#     ALL_DATA_FROM_CACHE = 100
#     PART_OF_DATA_FROM_CACHE = 50
#     NOTHING_FROM_CACHE = 0
#     KIND_OF_CACHE_USING = (
#         (ALL_DATA_FROM_CACHE, _l('All data was given from cache')),
#         (PART_OF_DATA_FROM_CACHE, _l('Part of data was given from cache')),
#         (NOTHING_FROM_CACHE, _l('Nothing was given from cache')),
#     )
#
#     class KindOfCacheUsing(object):
#         def __init__(self, value):
#             self.__value
#
#         @property
#         def value(self):
#             return self.__value
#
#         def set_as_all_data_from_cache(self):
#             self.__value = self.ALL_DATA_FROM_CACHE
#
#         def set_as_all_data_from_cache(self):
#             self.__value = self.ALL_DATA_FROM_CACHE
#
#
#
#     def __init__(self, **kwargs):
#         kwargs['choices'] = KIND_OF_CACHE_USING
#         super(KindOfCacheUsingField, self).__init__(**kwargs)
#
#     def to_python(self, value):

