import email
from pyexpat import model
from wsgiref import validate
from attr import field
from matplotlib.pyplot import cla
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Attendant, Student

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=Attendant
        fields="__all__"
    
    
    
class LogOutTokenSerializers(serializers.Serializer):
    refresh = serializers.CharField()

class RefreshTokenSerializers(serializers.Serializer):
    refresh = serializers.CharField()

class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    password1 = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    def validate(self, data):
        if data['password'] != data['password1']:
            raise serializers.ValidationError('passwords does not match')
        if Attendant.objects.filter(email = data['email']).exists():
            raise serializers.ValidationError("Email already Exist")
        return data

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"
