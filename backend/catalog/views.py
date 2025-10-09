from django.contrib.auth import login, logout
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView, GenericAPIView, ListCreateAPIView, \
    RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from . import models, serializers, filters, permissions, pagination


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


class UserView(ListAPIView): # testing
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


class ReviewListView(ListAPIView):
    permission_classes = [permissions.IsAdminUserOrReadOnly]
    serializer_class = serializers.ReviewSerializer
    queryset = models.Review.objects.select_related('user', 'movie').all()
    filterset_class = filters.ReviewFilter
    pagination_class = pagination.APIListPagination

    # def get_queryset(self):
    #     pk = self.kwargs['pk']
    #     queryset = models.Review.objects.filter(movie_id=pk)
    #     return queryset
    #
    # def get(self, request, pk):
    #     reviews = self.get_queryset()
    #
    #     user_review_serializer = serializers.ReviewSerializer()
    #     other_reviews_serializer = serializers.ReviewSerializer(reviews).data
    #     if request.user.is_authenticated:
    #         user_review = reviews.filter(user=request.user).first()
    #         user_review_serializer = serializers.ReviewSerializer(user_review).data
    #         other_reviews = reviews.exclude(user=request.user)
    #         other_reviews_serializer = serializers.ReviewSerializer(other_reviews).data
    #
    #     print(user_review_serializer, other_reviews_serializer)
    #     reviews_serializer = self.get_serializer(data={
    #         'user_review': user_review_serializer,
    #         'other_reviews': other_reviews_serializer,
    #     })
    #     reviews_serializer.is_valid(raise_exception=True)
    #
    #     return Response(reviews_serializer.data)


class ReviewDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsCreatorOrReadOnly]
    serializer_class = serializers.ReviewSerializer
    queryset = models.Review.objects.select_related('user', 'movie').all()


class GenreView(ListCreateAPIView):
    serializer_class = serializers.GenreSerializer
    queryset = models.Genre.objects.all()


class MovieRatingView(ListAPIView):
    permission_classes = [permissions.IsAdminUserOrReadOnly]
    serializer_class = serializers.MovieRatingSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        queryset = models.Rating.objects.filter(movie_id=pk)
        return queryset
