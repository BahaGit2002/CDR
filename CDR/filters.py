import django_filters
from CDR.models import CDR, CallStatus


class CRDFilter(django_filters.FilterSet):
    start_time = django_filters.DateTimeFilter(field_name='start_time', lookup_expr='gte')
    end_time = django_filters.DateTimeFilter(field_name='start_time', lookup_expr='lte')
    call_status = django_filters.ChoiceFilter(field_name='call_status', choices=CallStatus.choices)

    class Meta:
        model = CDR
        fields = ('start_time', 'end_time', 'call_status', 'calling_number')
