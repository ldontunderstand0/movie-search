from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('signup/', views.SignUpView.as_view()),
    path('login/', views.LoginView.as_view()),

    path('user/', views.UserView.as_view()),
]
