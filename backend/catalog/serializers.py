from django.contrib.auth.password_validation import validate_password
from django.db.models import Avg
from django.db.models.functions import ExtractYear
from rest_framework.serializers import (
    ModelSerializer,
    CharField,
    ValidationError,
    SerializerMethodField,
)
from . import models


class SignUpSerializer(ModelSerializer):
    password1 = CharField(
        write_only=True,
        required=True,
        max_length=100,
        validators=[validate_password])
    password2 = CharField(
        write_only=True,
        required=True,
        max_length=100,
        validators=[validate_password])

    class Meta:
        model = models.User
        fields = ['id', 'username', 'email', 'password1', 'password2']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise ValidationError('Passwords do not match.')
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password1')
        validated_data.pop('password2')

        validated_data['password'] = password
        instance = self.Meta.model(**validated_data)

        instance.set_password(password)
        instance.save()
        return instance


class LoginSerializer(ModelSerializer):
    class Meta:
        model = models.User
        fields = ['username', 'password']


class UserSerializer(ModelSerializer): # testing
    class Meta:
        model = models.User
        fields = ['id', 'username', 'email', 'password']


class GenreSerializer(ModelSerializer):
    class Meta:
        model = models.Genre
        fields = ['id', 'name']


class CountrySerializer(ModelSerializer):
    class Meta:
        model = models.Country
        fields = ['id', 'name']


class MoviePersonSerializer(ModelSerializer):
    class Meta:
        model = models.Person
        fields = ['id', 'full_name']


class MovieSerializer(ModelSerializer):
    rate = SerializerMethodField()

    class Meta:
        model = models.Movie
        fields = ['id', 'type', 'title', 'release_date', 'description', 'genres', 'countries', 'poster', 'rate']
        extra_kwargs = {
            'id': {'read_only': True},
        }

    def validate(self, attrs):
        title = attrs['title']
        release_date = attrs['release_date']
        movie = models.Movie.objects.filter(title=title, release_date=release_date).first()
        if movie:
            raise ValidationError('Movie already exists.')
        return attrs

    @staticmethod
    def get_rate(obj):
        rates = models.Rating.objects.filter(movie=obj)
        avg_rate = rates.aggregate(avg=Avg('rate'))
        return avg_rate['avg'] or 0.0


class MovieListSerializer(MovieSerializer):
    release_year = SerializerMethodField()

    class Meta(MovieSerializer.Meta):
        fields = MovieSerializer.Meta.fields + ['release_year']
        extra_kwargs = {
            **MovieSerializer.Meta.extra_kwargs,
            'release_date': {'write_only': True},
            'description':  {'write_only': True},
            'genres':       {'write_only': True},
            'countries':    {'write_only': True},
        }

    @staticmethod
    def get_release_year(obj):
        return obj.release_date.year


class MovieDetailSerializer(MovieSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    countries = CountrySerializer(many=True, read_only=True)
    rates_count = SerializerMethodField()
    actors = SerializerMethodField()
    directors = SerializerMethodField()

    class Meta(MovieSerializer.Meta):
        fields = MovieSerializer.Meta.fields + ['rates_count', 'directors', 'actors']

    @staticmethod
    def get_rates_count(obj):
        return models.Rating.objects.filter(movie=obj).count()

    @staticmethod
    def get_actors(obj):
        actors = models.Profession.actors.filter(movie=obj).select_related('person')
        return MoviePersonSerializer([actor.person for actor in actors], many=True).data

    @staticmethod
    def get_directors(obj):
        directors = models.Profession.directors.filter(movie=obj)
        return MoviePersonSerializer([director.person for director in directors], many=True).data
