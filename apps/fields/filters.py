from django_filters import FilterSet, DateTimeFilter

from apps.booking.models import Booking
from apps.fields.models import Field


class FieldFilter(FilterSet):
    start_time = DateTimeFilter(method='filter_by_time')
    end_time = DateTimeFilter(method='filter_by_time')

    def filter_queryset(self, queryset):
        start_time = self.form.cleaned_data.get('start_time')
        end_time = self.form.cleaned_data.get('end_time')
        if start_time and end_time:
            booked_fields = Booking.objects.filter(
                start_time__lt=end_time,
                end_time__gt=start_time,
                is_active=True
            ).values_list('field_id', flat=True)
            queryset = queryset.exclude(id__in=booked_fields)
        return queryset

    class Meta:
        model = Field
        fields = ['start_time', 'end_time']