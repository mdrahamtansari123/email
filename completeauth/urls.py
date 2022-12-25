
from django.contrib import admin
from django.urls import path
from accounts.views import *

urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('register/', RegisterAPI.as_view()),
    path('verify/', VerifyOTP.as_view()),
   
]
