from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('signup/', views.SignUpView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('logout/', views.LogoutView.as_view()),

    path('movie/', views.MovieListView.as_view()),
    path('movie/<int:pk>/', views.MovieDetailView.as_view()),

    path('review/', views.ReviewListView.as_view()),
    path('review/<int:pk>/', views.ReviewDetailView.as_view()),

    path('movie/<int:pk>/ratings/', views.MovieRatingView.as_view()),

    path('genre/', views.GenreView.as_view()),

    path('user/', views.UserView.as_view()), # testing
]
