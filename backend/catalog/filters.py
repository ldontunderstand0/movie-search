from django.db.models.functions import ExtractYear
from django_filters import rest_framework as filters
from .models import Movie, Genre, Country, User, Review


class MovieFilter(filters.FilterSet):

    search = filters.CharFilter(method='filter_by_search')

    type = filters.ChoiceFilter(choices=Movie.Type.choices)

    year = filters.ModelChoiceFilter(
        queryset=Movie.objects.annotate(year=ExtractYear('release_date')).values_list('year', flat=True).distinct(),
        to_field_name='year',
        field_name='release_date__year'
    )

    genre = filters.ModelChoiceFilter(
        queryset=Genre.objects,
        field_name='genres',
        to_field_name='name'
    )

    country = filters.ModelChoiceFilter(
        queryset=Country.objects,
        field_name='countries',
        to_field_name='name'
    )

    sort = filters.OrderingFilter(
        fields=[
            ('rate', 'rate'),
            ('release_date', 'release_date'),
            ('title', 'title'),
        ]
    )

    @staticmethod
    def filter_by_search(queryset, name, value):
        if value:
            return queryset.filter(title__iregex=value)
        return queryset

    class Meta:
        model = Movie
        fields = ['search', 'type', 'year', 'genre', 'country', 'sort']


class ReviewFilter(filters.FilterSet):

    movie = filters.ModelChoiceFilter(
        queryset=Movie.objects,
        field_name='movie',
        to_field_name='id'
    )

    user = filters.ModelChoiceFilter(
        queryset=User.objects,
        field_name='user',
        to_field_name='id'
    )

    type = filters.ChoiceFilter(choices=Review.Type.choices)

    sort = filters.OrderingFilter(
        fields=[
            ('created_at', 'created_at'),
            ('updated_at', 'updated_at'),
        ]
    )

    class Meta:
        model = Review
        fields = ['movie', 'user', 'type', 'sort']
