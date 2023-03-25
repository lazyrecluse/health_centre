from datetime import datetime
from os import access 
from django.conf import settings
import jwt
from rest_framework.authentication import BaseAuthentication
from .models import Attendant, Jwt, BlackListedToken

class Authentication(BaseAuthentication):

    def authenticate(self, request):
       
        data = self.validate_request(request.headers)
        
        if not data:
            return None, None
        


        return self.get_user(data["user_id"]), None
        # return super().authenticate(request)
    def get_user(self, user_id):
        try:
            user = Attendant.objects.get(id=user_id)
            return user
        except Exception:
            return None
    def validate_request(self, headers):
        authorization = headers.get("Authorization", None)
        # print(authorization[7:])
        
        if not authorization:
            return None
        token = headers["Authorization"][7:]
        
        decoded_data = self.verify_access_token(token)
        if not decoded_data:
            return None
        return decoded_data


    @staticmethod
    def verify_token(token):
        try:
            decoded_data = jwt.decode(
                token, 
                settings.SECRET_KEY, 
                algorithms="HS256")
        except Exception:
            return None

        print(token)
        if BlackListedToken.objects.filter(refreshtoken = token).exists():
            return None

        exp = decoded_data["exp"]
        if datetime.now().timestamp() > exp:
            return None
        return decoded_data

    def verify_access_token(self, token):
        try:
            decoded_data = jwt.decode(
                token, 
                settings.SECRET_KEY, 
                algorithms="HS256")
        except Exception:
            return None
            
        try:
            Jwt.objects.get(access=token)
        except Exception:
            return None

        exp = decoded_data["exp"]
        if datetime.now().timestamp() > exp:
            return None
        return decoded_data
    
    
    
