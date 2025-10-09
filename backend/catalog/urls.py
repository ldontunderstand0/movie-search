from django.urls import path
from rest_framework.routers import SimpleRouter
from catalog import views

app_name = 'catalog'

router = SimpleRouter()
router.register(r'user', views.UserViewSet)
router.register(r'movie', views.MovieViewSet)
router.register(r'person', views.PersonViewSet)
router.register(r'profession', views.ProfessionViewSet)
router.register(r'genre', views.GenreViewSet)
router.register(r'country', views.CountryViewSet)
router.register(r'review', views.ReviewViewSet)
router.register(r'rating', views.RatingViewSet)

urlpatterns = [
    path('signup/', views.SignUpView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('logout/', views.LogoutView.as_view()),
] + router.urls
# сортировка по рейтингу фильмов, сортировка по новым полям пользователя, персоны
# баг permissions
# баг регистрации