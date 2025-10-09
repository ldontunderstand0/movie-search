from django.db.models.functions import ExtractYear
from django_filters import rest_framework as filters
from catalog import models


class MovieFilter(filters.FilterSet):

    search = filters.CharFilter(method='filter_by_search')

    type = filters.ChoiceFilter(choices=models.Movie.Type.choices)

    year = filters.ModelChoiceFilter(
        queryset=models.Movie.objects
        .annotate(year=ExtractYear('release_date')).values_list('year', flat=True).distinct(),
        to_field_name='year',
        field_name='release_date__year'
    )

    genre = filters.ModelChoiceFilter(
        queryset=models.Genre.objects,
        field_name='genres',
        to_field_name='name'
    )

    country = filters.ModelChoiceFilter(
        queryset=models.Country.objects,
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
        model = models.Movie
        fields = ['search', 'type', 'year', 'genre', 'country', 'sort']


class ReviewFilter(filters.FilterSet):

    movie = filters.ModelChoiceFilter(
        queryset=models.Movie.objects,
        field_name='movie',
        to_field_name='id'
    )

    user = filters.ModelChoiceFilter(
        queryset=models.User.objects,
        field_name='user',
        to_field_name='id'
    )

    type = filters.ChoiceFilter(choices=models.Review.Type.choices)

    sort = filters.OrderingFilter(
        fields=[
            ('created_at', 'created_at'),
            ('updated_at', 'updated_at'),
        ]
    )

    class Meta:
        model = models.Review
        fields = ['movie', 'user', 'type', 'sort']


class RatingFilter(filters.FilterSet):

    movie = filters.ModelChoiceFilter(
        queryset=models.Movie.objects,
        field_name='movie',
        to_field_name='id'
    )

    user = filters.ModelChoiceFilter(
        queryset=models.User.objects,
        field_name='user',
        to_field_name='id'
    )

    sort = filters.OrderingFilter(
        fields=[
            ('created_at', 'created_at'),
            ('updated_at', 'updated_at'),
        ]
    )

    class Meta:
        model = models.Rating
        fields = ['movie', 'user', 'sort']


class ProfessionFilter(filters.FilterSet):

    name = filters.ChoiceFilter(choices=models.Profession.Type.choices)

    movie = filters.ModelChoiceFilter(
        queryset=models.Movie.objects,
        field_name='movie',
        to_field_name='id'
    )

    person = filters.ModelChoiceFilter(
        queryset=models.Person.objects,
        field_name='person',
        to_field_name='id'
    )

    class Meta:
        model = models.Profession
        fields = ['name', 'movie', 'person']


class GenreFilter(filters.FilterSet):

    search = filters.CharFilter(method='filter_by_search')

    @staticmethod
    def filter_by_search(queryset, name, value):
        if value:
            return queryset.filter(name__iregex=value)
        return queryset

    class Meta:
        model = models.Genre
        fields = ['search']


class CountryFilter(filters.FilterSet):

    search = filters.CharFilter(method='filter_by_search')

    @staticmethod
    def filter_by_search(queryset, name, value):
        if value:
            return queryset.filter(name__iregex=value)
        return queryset

    class Meta:
        model = models.Country
        fields = ['search']
