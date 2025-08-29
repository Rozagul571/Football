from django_filters import FilterSet, DateTimeFilter
from .models import Booking

class BookingFilter(FilterSet):
    start_time = DateTimeFilter(field_name='start_time', lookup_expr='gte')
    end_time = DateTimeFilter(field_name='end_time', lookup_expr='lte')

    class Meta:
        model = Booking
        fields = ['start_time', 'end_time']