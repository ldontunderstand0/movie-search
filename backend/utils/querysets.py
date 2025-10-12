from django.db.models import Count, Q, Avg


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
