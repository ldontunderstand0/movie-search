from django.contrib.auth import login, logout
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView, GenericAPIView, ListCreateAPIView, \
    RetrieveUpdateDestroyAPIView
from . import models, serializers, filters, permissions


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
    permission_classes = [permissions.GetAllowAnyOtherAdminPermission]
    serializer_class = serializers.MovieListSerializer
    queryset = models.Movie.objects.all()
    filterset_class = filters.MovieFilter


class MovieDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.GetAllowAnyOtherAdminPermission]
    serializer_class = serializers.MovieDetailSerializer
    queryset = models.Movie.objects.prefetch_related('genres', 'countries').all()


class GenreView(ListCreateAPIView):
    serializer_class = serializers.GenreSerializer
    queryset = models.Genre.objects.all()
