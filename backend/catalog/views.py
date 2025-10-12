from django.contrib.auth import login, logout
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.db.models import Prefetch
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView
import weasyprint
from urllib.parse import quote
from utils import querysets
from catalog import models, serializers, filters, permissions


@staff_member_required
def admin_review_pdf(request, review_id):
    review = get_object_or_404(models.Review, id=review_id)
    print(len(review.text))
    html = render_to_string('review_pdf.html', {'review': review})
    filename = f"review_{review.user.username}_{review.movie.title}.pdf"
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f"filename*=UTF-8''{quote(filename)}"
    # response['Content-Disposition'] = f"attachment; filename*=UTF-8''{quote(filename)}"
    weasyprint.HTML(string=html).write_pdf(response,)
                                           #stylesheets=[weasyprint.CSS(
                                               #settings.STATIC_URL / 'css/pdf.css')])
    return response


class SignUpView(CreateAPIView):
    permission_classes = [permissions.IsUnauthenticated]
    serializer_class = serializers.SignUpSerializer


class LoginView(APIView):
    permission_classes = [permissions.IsUnauthenticated]
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
    filterset_class = filters.UserFilter

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsUserOrAdminOrReadOnly()]
        return [permissions.IsAdminUserOrReadOnly()]

    def get_queryset(self):
        qs = super().get_queryset()
        return querysets.annotate_user_queryset(qs)

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

    def get_queryset(self):
        qs = super().get_queryset()
        return querysets.annotate_movie_queryset(qs)


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
    queryset = models.Person.objects.all()
    filterset_class = filters.PersonFilter

    def get_queryset(self):
        qs = super().get_queryset()
        annotated_movies = querysets.annotate_movie_queryset(models.Movie.objects.all())
        return qs.prefetch_related(Prefetch('professions__movie', queryset=annotated_movies))

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
