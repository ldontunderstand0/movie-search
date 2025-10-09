from django.contrib.auth.password_validation import validate_password
from django.db.models import Avg
from rest_framework.serializers import (
    Serializer,
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


class MovieSerializer(ModelSerializer):
    class Meta:
        model = models.Movie
        fields = ['id', 'type', 'title', 'release_date', 'description', 'genres', 'countries', 'poster']

    def validate(self, attrs):
        title = attrs['title']
        release_date = attrs['release_date']
        movie = models.Movie.objects.filter(title=title, release_date=release_date).first()
        if movie:
            raise ValidationError('Movie already exists.')
        return attrs


class MovieInfoSerializer(MovieSerializer):
    rate = SerializerMethodField()
    user_actions = SerializerMethodField()

    class Meta(MovieSerializer.Meta):
        fields = MovieSerializer.Meta.fields + [ 'rate', 'user_actions']

    @staticmethod
    def get_rate(obj):
        rates = models.Rating.objects.filter(movie=obj)
        avg_rate = rates.aggregate(avg=Avg('rate'))
        return avg_rate['avg'] or 0.0

    def get_user_actions(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            rating = models.Rating.objects.filter(movie=obj, user=request.user).first()
            return MovieRatingSerializer(rating).data if rating else None
        return None


class MovieListSerializer(MovieInfoSerializer):
    release_year = SerializerMethodField()

    class Meta(MovieInfoSerializer.Meta):
        fields = MovieInfoSerializer.Meta.fields + ['release_year']
        extra_kwargs = {
            'release_date': {'write_only': True},
            'description':  {'write_only': True},
            'genres':       {'write_only': True},
            'countries':    {'write_only': True},
        }

    @staticmethod
    def get_release_year(obj):
        return obj.release_date.year


class MovieDetailSerializer(MovieInfoSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    countries = CountrySerializer(many=True, read_only=True)
    rates_count = SerializerMethodField()
    actors = SerializerMethodField()
    directors = SerializerMethodField()

    class Meta(MovieInfoSerializer.Meta):
        fields = MovieInfoSerializer.Meta.fields + ['rates_count', 'directors', 'actors']

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


class PersonSerializer(ModelSerializer):
    class Meta:
        model = models.Person
        exclude = []


class MoviePersonSerializer(PersonSerializer):
    class Meta(PersonSerializer.Meta):
        exclude = PersonSerializer.Meta.exclude + ['birth_date', 'sex', 'movies']


class RatingSerializer(ModelSerializer):
    class Meta:
        model = models.Rating
        fields = ['id', 'movie', 'user', 'rate', 'date', 'is_watched']


class MovieRatingSerializer(RatingSerializer):
    class Meta(RatingSerializer.Meta):
        extra_kwargs = {
            'movie': {'write_only': True},
            'user': {'write_only': True},
            'date': {'write_only': True},
        }


class ReviewSerializer(ModelSerializer):
    class Meta:
        model = models.Review
        exclude = []
