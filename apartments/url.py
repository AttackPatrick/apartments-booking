from django.urls import path, include
from .views import *

urlpatterns = [
    path('', apartments_list, name='apartments_list'),
    
]
