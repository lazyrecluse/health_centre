from django.shortcuts import render
import jwt
from .models import Student, Jwt
from rest_framework.views import APIView
from rest_framework import generics
import random
import string
from datetime import datetime, timedelta
from django.contrib.auth import authenticate
from django.conf import settings
from rest_framework.response import Response
from .serializer import LoginSerializer, UserSerializer, LogOutTokenSerializers, RefreshTokenSerializers, RegisterSerializer
from .authentication import Authentication
from Account import serializer

from rest_framework.status import HTTP_200_OK
from rest_framework import permissions
from .models import BlackListedToken,Attendant

def get_random(length):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
def get_access_token(payload):
    return jwt.encode(
        {"exp":datetime.now() + timedelta(days=2), **payload}, 
        settings.SECRET_KEY,
         algorithm="HS256"
         )

def get_refresh_token():
    return jwt.encode(
        {"exp": datetime.now() + timedelta(days=365), "data":get_random(10)},
         settings.SECRET_KEY, algorithm="HS256"
    )

class LoginView(APIView):
    serializer_class = LoginSerializer
    def post(self, request):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(username = serializer.validated_data['email'], password = serializer.validated_data['password'])
        if not user:
            return Response(
                data = {
                    "error": "Invalid email or password"
                }, status=400
            )
        Jwt.objects.filter(user_id=user.id).delete()
        access = get_access_token({"user_id": user.id, "username": user.get_username()})
        exp = jwt.decode(access, settings.SECRET_KEY, algorithms="HS256" )['exp']
        refresh = get_refresh_token()
        serializedUser = UserSerializer(user)
        Jwt.objects.create(
            user_id = user.id, access=access, refresh=refresh
        )
        return Response({'access': access, 'refresh': refresh, 'user': serializedUser.data, 'exp': exp}, status = 200)
    
    
    
class LogoutView(APIView):
    serializer_class = LogOutTokenSerializers
    # permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data['refresh']
        try:
            Jwt.objects.get(refresh = serializer.validated_data['refresh'])
        except Jwt.DoesNotExist:
            return Response({"data": "invalid token"})
        else:
            refresh_token = BlackListedToken(refreshtoken = serializer.validated_data['refresh'])
            refresh_token.save()
            Jwt.objects.get(refresh=serializer.validated_data["refresh"]).delete()
            return Response({"logged out successfully"}, status=HTTP_200_OK)


class UserApi(generics.RetrieveAPIView):
    authentication_classes = [Authentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
    def get_object(self):
        return self.request.user


class RefreshTokenView(APIView):
    serializer_class = RefreshTokenSerializers
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data['refresh'])
        try:
            active_jwt = Jwt.objects.get(refresh=serializer.validated_data["refresh"])
        except Jwt.DoesNotExist:
            return Response({"error": "refresh does not exist"}, status='404')
        if not Authentication.verify_token(serializer.validated_data['refresh']):
            return Response({"error": "Token is invalid"})
        refresh_token = BlackListedToken(refreshtoken = serializer.validated_data['refresh'])
        refresh_token.save()
        access = get_access_token({"user_id": active_jwt.user.id})
        refresh = get_refresh_token()
        exp = jwt.decode(access, settings.SECRET_KEY, algorithms="HS256" )['exp']
        active_jwt.access = access
        active_jwt.refresh = refresh
        active_jwt.save()
        PersonSerializer = UserSerializer(active_jwt.user)
        return Response({
            'access': access, 'refresh': refresh, 'user': PersonSerializer.data, 'exp': exp 
        })

class RegisterView(APIView):
    serializer_class = RegisterSerializer
    def post(self, request):
        serilizer = self.serializer_class(data=request.data)
        serilizer.is_valid(raise_exception=True)
        Attendant.objects._create_(email = serilizer.validated_data['email'], password = serilizer.validated_data['password'],
                                    first_name = serilizer.validated_data['first_name'],
                                    last_name = serilizer.validated_data['last_name'])
        
        authenticated_user = authenticate(username = serilizer.validated_data['email'], password = serilizer.validated_data['password'])
        Jwt.objects.filter(user_id=authenticated_user.id).delete()
        access = get_access_token({"user_id": authenticated_user.id, "username": authenticated_user.get_username()})
        exp = jwt.decode(access, settings.SECRET_KEY, algorithms="HS256" )['exp']
        refresh = get_refresh_token()
        serializedUser = UserSerializer(authenticated_user)
        Jwt.objects.create(
            user_id = authenticated_user.id, access=access, refresh=refresh
        )
        return Response({"message": "user succesfully created", 'access': access, 'refresh': refresh, 'user': serializedUser.data, 'exp': exp}, status=HTTP_200_OK)