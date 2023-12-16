from django.shortcuts import render
from apartments.models import *


def index(request):
    context = {}
    apartments = Apartment.objects.filter()
    context['apartments'] = apartments
    # return render(request,'index.html',context)
    return render('apartments_list')