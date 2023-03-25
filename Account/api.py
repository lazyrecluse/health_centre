import imp
from .models import Student
from rest_framework import generics
from .authentication import Authentication
from rest_framework.permissions import IsAuthenticated
from .serializer import StudentSerializer

class StudentView(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    # authentication_classes = [Authentication]
    # permission_classes = [IsAuthenticated]
    

class StudentDetailsView(generics.RetrieveAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    # authentication_classes = [Authentication]
    # permission_classes = [IsAuthenticated]


