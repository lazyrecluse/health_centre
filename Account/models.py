from django.db import models

from django.db import models
from typing import final
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager



class CustomUserManager(BaseUserManager):
    def _create_(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email field is requeired')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('first_name', "admin")

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True")

        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True")
        return self._create_(email, password, **extra_fields)


class Attendant(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255,blank=True,null=True)
    last_name = models.CharField(max_length=255,null=True,blank=True)
    created_At = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    USERNAME_FIELD = "email"
    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Jwt(models.Model):
    user = models.OneToOneField(Attendant, related_name='login_user', on_delete=models.CASCADE)
    access = models.TextField()
    refresh = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class BlackListedToken(models.Model):
    refreshtoken = models.TextField()

    
class Student(models.Model):
    Sex = (("Male", "M"),
           ("Female", "F"))
    email=models.EmailField(blank=True, null=True)
    age = models.IntegerField(default=18)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    matric_no =  models.CharField(max_length=50)
    sex=models.CharField(choices=Sex , null=True,blank=True,   max_length=50)
    phone_no = models.IntegerField(null=True,blank=True)
    address = models.CharField(null=True, blank=True, max_length=50)
    blood_group = models.CharField(null=True, blank=True,  max_length=50)
    blood_type = models.CharField(null=True,blank=True,  max_length=50)
    previous_health_condition = models.CharField(null=True, blank=True,  max_length=50)
    matric_no =  models.CharField(max_length=12, blank=True, null=True)
    
    
    
