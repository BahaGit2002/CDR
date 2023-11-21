# from django_filters import rest_framework
# from CDR.models import CDR
#
#
# class CRDFilter(rest_framework.FilterSet):
#     start_time = rest_framework.DateTimeFilter(field_name='start_time', lookup_expr='gte')
#     end_time = rest_framework.DateTimeFilter(field_name='end_time', lookup_expr='lte')
#
#     class Meta:
#         model = CDR
#         fields = ('start_time', 'end_time')
