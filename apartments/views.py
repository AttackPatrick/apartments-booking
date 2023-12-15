from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.db.models import Q
from .models import *
from django.shortcuts import redirect
from django.utils import timezone
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.contrib import messages

def apartments_list(request):

    # name = request.GET.get('name')
    # address = request.GET.get('address')
    # status = request.GET.get('status')
    # price_range = request.GET.get('price_range')
    # no_of_person = request.GET.get('no_of_person')
    # bed_type = request.GET.get('bed_type')
    q = Q()
    context = {}

    if request.GET.get('name'):
        name = request.GET.get('name').replace('+', ' ').strip()
        q &= Q(title__icontains=name)
        context['name'] = name

    if request.GET.get('address'):
        address = request.GET.get('address').replace('+', ' ').strip()
        q &= Q(apartmentaddress__city__icontains=address)
        context['address'] = address

    if request.GET.get('price_range'):
        range_price = request.GET.get('price_range')
        price_range = request.GET.get('price_range').split('-')
        min_price, max_price = price_range
        q &= Q(price__gte=min_price) & Q(price__lte=max_price)
        context['price_range'] = range_price

    if request.GET.get('bed_type'):
        bed_type = request.GET.get('bed_type').replace('+', ' ').strip()
        q &= Q(bed__icontains=bed_type)
        context['bed_type'] = bed_type

    if request.GET.get('no_of_person'):
        no_of_person = request.GET.get('no_of_person').replace('+', ' ').strip()
        q &= Q(persons__gte=no_of_person)
        context['no_of_person'] = no_of_person
    if request.GET.get('status'):
        status = request.GET.get('status').replace('+', ' ').strip()
        q &= Q(apartment_status__icontains=status)
        context['status'] = status

    
    # status = request.GET.get('status').replace('+', ' ').strip()

    # query = Q()
    # if name:
    #     query &= Q(title__icontains=name)
    # if address:
    #     query &= Q(apartmentaddress__city__icontains=address)
    # if no_of_person and no_of_person.isdigit():
    #     query &= Q(persons=int(no_of_person))

    # if bed_type:
    #     query &= Q(bed=bed_type)
    # if price_range:
    #     min_price = price_range.split('-')[0]
    #     max_price = price_range.split('-')[1]

    #     query &= Q(price__gte=min_price)
    #     query &= Q(price__gte=max_price)

    # q = Q()
    # if name:
    #     q &= Q(title__icontains=name)
    # if address:
    #     q &= Q(apartmentaddress__city__icontains=address)
    # if bed_type:
    #     q &= Q(bed__icontains=bed_type)
    # if no_of_person:
    #     q &= Q(guests__gte=no_of_person)
    # if price_range:
    #     min_price, max_price = price_range
    #     q &= Q(price__gte=min_price) & Q(price__lte=max_price)
    
    page = request.GET.get('page', 1)
    # apartments = Apartment.objects.filter(query).order_by('price')
    apartments = Apartment.objects.filter(q)
    paginator = Paginator(Apartment.objects.filter(q), 10)
    try:
        apartments = paginator.page(page)
    except PageNotAnInteger:
        apartments = paginator.page(1)
    except EmptyPage:
        apartments = paginator.page(paginator.num_pages)

    # context = {}
    context['apartments'] = apartments
    # context['name'] = name
    # context['address'] = address
    # context['no_of_person'] = no_of_person
    # context['bed_type'] = bed_type
    # context['price_range'] = price_range

    return render(request, 'apartments_list.html', context)



