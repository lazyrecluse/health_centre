from django.contrib import admin
from .models import Attendant, Student
# Register your models here.
admin.site.register((Attendant, ))
admin.site.register((Student,))