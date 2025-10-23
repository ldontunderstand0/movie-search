from django.db.models import Count, Q, Avg, Case, When, ExpressionWrapper, F, IntegerField, Value
from django.db.models.functions import ExtractMonth, ExtractDay
from datetime import datetime
from zoneinfo import ZoneInfo


def annotate_user_queryset(queryset):
    return queryset.annotate(
        _watches=Count('ratings', filter=Q(ratings__is_watched=True)),
        _rates=Count('ratings', filter=Q(ratings__rate__isnull=False)),
        _reviews=Count('reviews'),
    ).order_by('username')


def annotate_movie_queryset(queryset):
    return queryset.annotate(
        _rate=Avg('ratings__rate', filter=Q(ratings__rate__isnull=False)),
    ).order_by('-_rate')

def annotate_genre_queryset(queryset):
    return queryset.annotate(
        _movies_count=Count('movies'),
    ).order_by('name')

def annotate_person_queryset(queryset):
    tz = ZoneInfo("Europe/Moscow")  # например Москва
    today = datetime.now(tz).date()
    return queryset.exclude(birth_date__isnull=True).annotate(
        month=ExtractMonth("birth_date"),
        day=ExtractDay("birth_date"),
        ).annotate(
            has_had_birthday=Case(
                When(Q(month__lt=today.month)| Q(month=today.month, day__lt=today.day),
                     then=Value(1)),
                default=Value(0),
                output_field=IntegerField(),),
        ).annotate(
            month_offset=Case(
                When(has_had_birthday=1,
                     then=F("month") + Value(12)),
                default=F("month"),
                output_field=IntegerField(),
            )
        ).annotate(
            _days_to_birthday=ExpressionWrapper(
                ((F("month_offset") * 31 + F("day")) - (today.month * 31 + today.day)),
                output_field=IntegerField(),
            )
    ).order_by("month_offset", "day")
