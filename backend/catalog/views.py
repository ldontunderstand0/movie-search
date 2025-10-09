from django.contrib.auth import login, logout
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView, ListAPIView, GenericAPIView, ListCreateAPIView, \
    RetrieveUpdateDestroyAPIView
from catalog import models, serializers, filters, permissions, pagination


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

        return Response({
            "success": "User logged in.",
        })


class LogoutView(APIView):
    permission_classes = [IsAuthenticated,]

    @staticmethod
    def post(request):
        logout(request)
        return Response({"success": "User logged out."})


class UserListView(ListCreateAPIView): # need to custom
    permission_classes = [permissions.IsAdminUserOrReadOnly]
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all()
    # filterset_class = filters.UserFilter
    pagination_class = pagination.APIListPagination


class UserDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsUserOrAdminOrReadOnly]
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all()


class MovieListView(ListCreateAPIView):
    permission_classes = [permissions.IsAdminUserOrReadOnly]
    serializer_class = serializers.MovieListSerializer
    queryset = models.Movie.objects.all()
    filterset_class = filters.MovieFilter
    pagination_class = pagination.APIListPagination


class MovieDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAdminUserOrReadOnly]
    serializer_class = serializers.MovieDetailSerializer
    queryset = models.Movie.objects.prefetch_related('genres', 'countries').all()


class ReviewListView(ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = serializers.ReviewSerializer
    queryset = models.Review.objects.select_related('user', 'movie').all()
    filterset_class = filters.ReviewFilter
    pagination_class = pagination.APIListPagination


class ReviewDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsCreatorOrAdminOrReadOnly]
    serializer_class = serializers.ReviewSerializer
    queryset = models.Review.objects.select_related('user', 'movie').all()


class RatingListView(ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = serializers.RatingSerializer
    queryset = models.Rating.objects.select_related('user', 'movie').all()
    filterset_class = filters.RatingFilter
    pagination_class = pagination.APIListPagination


class RatingDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsCreatorOrAdminOrReadOnly]
    serializer_class = serializers.RatingSerializer
    queryset = models.Rating.objects.select_related('user', 'movie').all()


# class PersonListView(ListCreateAPIView): # need to custom
#     permission_classes = [permissions.IsAdminUserOrReadOnly]
#     serializer_class = serializers.PersonSerializer
#     queryset = models.Person.objects.prefetch_related('movies').all()
#     # filterset_class = filters.PersonFilter
#     pagination_class = pagination.APIListPagination
#
#
# class PersonDetailView(RetrieveUpdateDestroyAPIView): # need to custom
#     permission_classes = [permissions.IsAdminUserOrReadOnly]
#     serializer_class = serializers.PersonSerializer
#     queryset = models.Person.objects.prefetch_related('movies').all()

class PersonViewSet(ModelViewSet):
    permission_classes = [permissions.IsAdminUserOrReadOnly]
    serializer_class = serializers.PersonSerializer
    queryset = models.Person.objects.prefetch_related('movies').all()
    # filterset_class = filters.PersonFilter
    pagination_class = pagination.APIListPagination


class ProfessionViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = serializers.ProfessionSerializer
    queryset = models.Profession.objects.select_related('person', 'movie').all()
    filterset_class = filters.ProfessionFilter
    pagination_class = pagination.APIListPagination


class GenreListView(ListCreateAPIView): # need to custom
    permission_classes = [permissions.IsAdminUserOrReadOnly]
    serializer_class = serializers.GenreSerializer
    queryset = models.Genre.objects.all()
    filterset_class = filters.GenreFilter
    pagination_class = pagination.APIListPagination


class GenreDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = serializers.GenreSerializer
    queryset = models.Genre.objects.all()


class CountryListView(ListCreateAPIView): # need to custom
    permission_classes = [permissions.IsAdminUserOrReadOnly]
    serializer_class = serializers.CountrySerializer
    queryset = models.Country.objects.all()
    filterset_class = filters.CountryFilter
    pagination_class = pagination.APIListPagination


class CountryDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = serializers.CountrySerializer
    queryset = models.Country.objects.all()
