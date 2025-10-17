from django.contrib.auth.password_validation import validate_password
from rest_framework.serializers import (
    ModelSerializer,
    CharField,
    ValidationError,
    SerializerMethodField,
)

from utils.serializers import BaseModelSerializer
from catalog import models


class UserSerializer(ModelSerializer):
    class Meta:
        model = models.User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}


class SignUpSerializer(UserSerializer):
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

    class Meta(UserSerializer.Meta):
        fields = ['username', 'email', 'password1', 'password2']

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


class LoginSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = ['username', 'password']


class UserListSerializer(UserSerializer):
    watches = SerializerMethodField()
    rates = SerializerMethodField()
    reviews = SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = ['id', 'username', 'watches', 'rates', 'reviews']

    @staticmethod
    def get_watches(obj):
        return getattr(obj, '_watches')

    @staticmethod
    def get_rates(obj):
        return getattr(obj, '_rates')

    @staticmethod
    def get_reviews(obj):
        return getattr(obj, '_reviews')


class PersonSerializer(BaseModelSerializer):
    class Meta:
        model = models.Person
        exclude = []


class ProfessionSerializer(BaseModelSerializer):
    class Meta:
        model = models.Profession
        exclude = []


class GenreSerializer(ModelSerializer):
    class Meta:
        model = models.Genre
        fields = '__all__'


class GenreListSerializer(GenreSerializer):
    movies_count = SerializerMethodField()

    @staticmethod
    def get_movies_count(obj):
        return obj.movies.count()


class CountrySerializer(ModelSerializer):
    class Meta:
        model = models.Country
        exclude = []


class CountryListSerializer(CountrySerializer):
    movies_count = SerializerMethodField()

    @staticmethod
    def get_movies_count(obj):
        return obj.movies.count()


class RatingSerializer(BaseModelSerializer):
    class Meta:
        model = models.Rating
        exclude = []


class ReviewSerializer(ModelSerializer):
    class Meta:
        model = models.Review
        exclude = []
        extra_kwargs = {'status': {'read_only': True}}


class MovieSerializer(BaseModelSerializer):
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
        return getattr(obj, '_rate')

    def get_user_actions(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            rating = obj.ratings.filter(user=request.user)
            return RatingSerializer(
                rating.first(),
                exclude_fields=['movie', 'user', 'created_at', 'updated_at']
            ).data if rating.exists() else None
        return None


class MovieListSerializer(MovieInfoSerializer):
    release_year = SerializerMethodField()
    url = SerializerMethodField()

    class Meta(MovieInfoSerializer.Meta):
        fields = MovieInfoSerializer.Meta.fields + ['release_year', 'url']
        extra_kwargs = {
            'release_date': {'write_only': True},
            'description':  {'write_only': True},
            'genres':       {'write_only': True},
            'countries':    {'write_only': True},
        }

    @staticmethod
    def get_release_year(obj):
        return obj.release_date.year

    @staticmethod
    def get_url(obj):
        return obj.get_absolute_url()


class MovieDetailSerializer(MovieInfoSerializer):

    genres = GenreSerializer(many=True, read_only=True)
    countries = CountrySerializer(many=True, read_only=True)
    rates_count = SerializerMethodField()
    actors = SerializerMethodField()
    directors = SerializerMethodField()

    class Meta(MovieInfoSerializer.Meta):
        fields = MovieInfoSerializer.Meta.fields + ['trailer_url', 'rates_count', 'directors', 'actors']

    @staticmethod
    def get_rates_count(obj):
        return obj.ratings.count()

    @staticmethod
    def get_actors(obj):
        actors = obj.professions.exclude(name=models.Profession.Type.DIRECTOR).select_related('person')
        return PersonSerializer(
            [actor.person for actor in actors],
            many=True,
            exclude_fields=['birth_date', 'sex', 'movies', 'biography']
        ).data

    @staticmethod
    def get_directors(obj):
        directors = obj.professions.filter(name=models.Profession.Type.DIRECTOR).select_related('person')
        return PersonSerializer(
            [director.person for director in directors],
            many=True,
            exclude_fields=['birth_date', 'sex', 'movies', 'biography'],
        ).data


class ProfessionDetailSerializer(ProfessionSerializer):
    movie = MovieListSerializer(read_only=True, exclude_fields=['user_actions'])


class PersonListSerializer(PersonSerializer):
    class Meta(PersonSerializer.Meta):
        exclude = PersonSerializer.Meta.exclude + ['movies']
        extra_kwargs = {'biography': {'write_only': True}}


class PersonDetailSerializer(PersonSerializer):
    professions = ProfessionDetailSerializer(many=True, read_only=True, exclude_fields=['id', 'person'])
    movies_count = SerializerMethodField()

    @staticmethod
    def get_movies_count(obj):
        return obj.movies.count()

    class Meta(PersonSerializer.Meta):
        exclude = PersonSerializer.Meta.exclude + ['movies']
