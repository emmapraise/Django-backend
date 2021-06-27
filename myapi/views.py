from myapi.serializers import UserSerializer
from myapi.models import User
from django.db import IntegrityError
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows all users to be viewed or edited.

    Available  Endpoint
    register: https://ideathinker-django.herokuapp.com/register
    Login: https://ideathinker-django.herokuapp.com/login
    Logout: https://ideathinker-django.herokuapp.com/logout
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        # try:
        response = super().create(request, args, **kwargs)
        user = User.objects.get(email=response.data['email'])
        response = {
            'data': response.data,
            'message': 'User created successfully.',
            'status': 'success'
        }
        # except IntegrityError:
            # response = {
            #     'data': {},
            #     'message': 'Existing account found with this email.',
            #     'status': 'failure'
            # }
        return Response(data=response, status=status.HTTP_200_OK)

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)