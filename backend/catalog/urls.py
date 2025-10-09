from django.urls import path
from catalog import views

app_name = 'catalog'

urlpatterns = [
    path('signup/', views.SignUpView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('logout/', views.LogoutView.as_view()),

    path('user/', views.UserView.as_view()), # testing
    path('user/<int:pk>/', views.ReviewDetailView.as_view()),  # need view

    path('movie/', views.MovieListView.as_view()),
    path('movie/<int:pk>/', views.MovieDetailView.as_view()),

    path('review/', views.ReviewListView.as_view()),
    path('review/<int:pk>/', views.ReviewDetailView.as_view()),

    path('rating/', views.RatingListView.as_view()),
    path('rating/<int:pk>/', views.RatingDetailView.as_view()),

    path('person/', views.PersonListView.as_view()),
    path('person/<int:pk>/', views.PersonDetailView.as_view()),

    path('profession/', views.ProfessionListView.as_view()),
    path('profession/<int:pk>/', views.ProfessionDetailView.as_view()),

    path('genre/', views.GenreListView.as_view()),
    path('genre/<int:pk>/', views.GenreDetailView.as_view()),

    path('country/', views.CountryListView.as_view()),
    path('country/<int:pk>/', views.CountryDetailView.as_view()),
]
