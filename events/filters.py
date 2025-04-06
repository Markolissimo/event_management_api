import django_filters
from django.utils import timezone
from .models import Event
from django.db import models
from typing import QuerySet

class EventFilter(django_filters.FilterSet):
    """
    Filter for events.
    """
    title = django_filters.CharFilter(lookup_expr='icontains')
    location = django_filters.CharFilter(lookup_expr='icontains')
    min_date = django_filters.DateTimeFilter(field_name='date', lookup_expr='gte')
    max_date = django_filters.DateTimeFilter(field_name='date', lookup_expr='lte')
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    is_active = django_filters.BooleanFilter()
    has_available_seats = django_filters.BooleanFilter(method='filter_available_seats')
    upcoming = django_filters.BooleanFilter(method='filter_upcoming')

    class Meta:
        """
        Meta class for the EventFilter.
        """
        model = Event
        fields = [
            'title', 'location', 'min_date', 'max_date',
            'min_price', 'max_price', 'is_active',
            'has_available_seats', 'upcoming'
        ]

    def filter_available_seats(self, queryset: QuerySet[Event], name: str, value: bool) -> QuerySet[Event]:
        """
        Filter events with available seats.
        """
        if value:
            return queryset.filter(registrations__isnull=True) | queryset.annotate(
                registration_count=models.Count('registrations')
            ).filter(registration_count__lt=models.F('capacity'))
        return queryset

    def filter_upcoming(self, queryset: QuerySet[Event], name: str, value: bool) -> QuerySet[Event]:
        """
        Filter upcoming events.
        """
        if value:
            return queryset.filter(date__gt=timezone.now())
        return queryset.filter(date__lte=timezone.now()) 