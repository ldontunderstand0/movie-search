from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('signup/', views.SignUpView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('logout/', views.LogoutView.as_view()),

    path('movie/', views.MovieListView.as_view()), # testing
    path('movie/<int:pk>/', views.MovieDetailView.as_view()), # testing
    path('genre/', views.GenreView.as_view()), # testing

    path('user/', views.UserView.as_view()), # testing
]
