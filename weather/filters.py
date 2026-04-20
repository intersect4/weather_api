import django_filters

from .models import WeatherRecord


class WeatherRecordFilter(django_filters.FilterSet):
    timestamp = django_filters.DateFilter(
        field_name='timestamp',
        lookup_expr='date',
    )

    class Meta:
        model = WeatherRecord
        fields = ['city', 'timestamp']
