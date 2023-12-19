from django.urls import path, include
from .views import *

urlpatterns = [
    path('', apartments_list, name='apartments_list'),
    path('apartments_detail/<id>/', apartments_detail, name='apartments_detail'),
    path('apartments_booking_succesful/<id>/',
         apartments_booking_succesful, name='apartments_booking_succesful'),
]
