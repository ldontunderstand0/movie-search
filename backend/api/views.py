from django.contrib.auth import authenticate, login
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView, GenericAPIView
from . import serializers, models


class SignUpView(CreateAPIView):
    serializer_class = serializers.SignUpSerializer


class LoginView(GenericAPIView):
    serializer_class = serializers.LoginSerializer

    def post(self, request):

        username = request.data['username']
        password = request.data['password']

        user = models.User.objects.filter(username=username).first()
        if user is None:
            raise AuthenticationFailed('User not found')
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')
        login(request, user)

        return Response({
            "200": "OK",
        })


class LogoutView(APIView):
    permission_classes = [IsAuthenticated,]

    def post(self, request):
        

        return Response({"success": "User logged out."})


class UserView(ListAPIView):
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all()