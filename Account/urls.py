from django.urls import path
from .views import LoginView, LogoutView, RegisterView, UserApi, RefreshTokenView
from .api import StudentView, StudentDetailsView
urlpatterns = [
    path('login', LoginView.as_view()),
    path('logout', LogoutView.as_view()),
    path('register', RegisterView.as_view()),
    path('get_user', UserApi.as_view()),
    path('get_new_token', RefreshTokenView.as_view()),
    path('student/', StudentView.as_view()),
    path('student/<pk>', StudentDetailsView.as_view()) 
]