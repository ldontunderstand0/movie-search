from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView
from . import serializers, models


class SignUpView(CreateAPIView):
    serializer_class = serializers.SignUpSerializer


class UserView(ListAPIView):
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all()