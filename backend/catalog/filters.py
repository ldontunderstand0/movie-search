from django.db.models.functions import ExtractYear
from django_filters import rest_framework as filters
from catalog import models


class UserFilter(filters.FilterSet):

    search = filters.CharFilter(field_name='username', lookup_expr='contains')
    sort = filters.OrderingFilter(
        fields=(
            ('_watches', 'watches'),
            ('_rates', 'rates'),
            ('_reviews', 'reviews'),
        )
    )

    class Meta:
        model = models.User
        fields = ['search', 'sort']



class MovieFilter(filters.FilterSet):

    search = filters.CharFilter(field_name='title', lookup_expr='iregex')

    type = filters.ChoiceFilter(choices=models.Movie.Type.choices)

    year = filters.ModelChoiceFilter(
        queryset=models.Movie.objects
        .annotate(year=ExtractYear('release_date')).values_list('year', flat=True).distinct(),
        to_field_name='year',
        field_name='release_date__year',
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
            ('_rate', 'rate'),
            ('release_date', 'release_date'),
            ('title', 'title'),
        ]
    )

    class Meta:
        model = models.Movie
        fields = ['search', 'type', 'year', 'genre', 'country', 'sort']


class PersonFilter(filters.FilterSet):

    search = filters.CharFilter(field_name='full_name', lookup_expr='iregex')

    class Meta:
        model = models.Person
        fields = ['search']


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

    search = filters.CharFilter(field_name='name', lookup_expr='iсontains')

    class Meta:
        model = models.Genre
        fields = ['search']


class CountryFilter(filters.FilterSet):

    search = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = models.Country
        fields = ['search']
