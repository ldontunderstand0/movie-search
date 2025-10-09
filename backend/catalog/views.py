from django.contrib.auth import login, logout
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView
from catalog import models, serializers, filters, permissions


class SignUpView(CreateAPIView):
    serializer_class = serializers.SignUpSerializer


class LoginView(APIView):
    serializer_class = serializers.LoginSerializer

    @staticmethod
    def post(request):

        username = request.data['username']
        password = request.data['password']

        user = models.User.objects.filter(username=username).first()
        if user is None:
            raise AuthenticationFailed('User not found.')
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password.')
        login(request, user)

        return Response({"success": "User logged in.",})


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        logout(request)
        return Response({"success": "User logged out."})


class UserViewSet(ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    filterset_class = filters.UserFilter

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsUserOrAdminOrReadOnly()]
        return [permissions.IsAdminUserOrReadOnly()]

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.UserListSerializer
        return serializers.UserSerializer


class MovieViewSet(ModelViewSet):
    permission_classes = [permissions.IsAdminUserOrReadOnly]
    queryset = models.Movie.objects.prefetch_related('genres', 'countries').all()
    filterset_class = filters.MovieFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.MovieListSerializer
        return serializers.MovieDetailSerializer


class ReviewViewSet(ModelViewSet):
    queryset = models.Review.objects.select_related('user', 'movie').all()
    serializer_class = serializers.ReviewSerializer
    filterset_class = filters.ReviewFilter

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsCreatorOrAdminOrReadOnly()]
        return [IsAuthenticatedOrReadOnly()]


class RatingViewSet(ModelViewSet):
    queryset = models.Rating.objects.select_related('user', 'movie').all()
    serializer_class = serializers.RatingSerializer
    filterset_class = filters.RatingFilter

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsCreatorOrAdminOrReadOnly()]
        return [IsAuthenticatedOrReadOnly()]


class PersonViewSet(ModelViewSet):
    permission_classes = [permissions.IsAdminUserOrReadOnly]
    queryset = models.Person.objects.prefetch_related('movies').all()
    filterset_class = filters.PersonFilter

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.PersonDetailSerializer
        return serializers.PersonListSerializer


class ProfessionViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = serializers.ProfessionSerializer
    queryset = models.Profession.objects.select_related('person', 'movie').all()
    filterset_class = filters.ProfessionFilter


class GenreViewSet(ModelViewSet):
    permission_classes = [permissions.IsAdminUserOrReadOnly]
    queryset = models.Genre.objects.all()
    filterset_class = filters.GenreFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.GenreListSerializer
        return serializers.GenreSerializer


class CountryViewSet(ModelViewSet):
    permission_classes = [permissions.IsAdminUserOrReadOnly]
    queryset = models.Country.objects.all()
    filterset_class = filters.CountryFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.CountryListSerializer
        return serializers.CountrySerializer
