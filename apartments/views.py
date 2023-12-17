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


def apartments_detail(request, id):

    if request.method == 'POST':

        email = request.POST.get('email')
        apartment = request.POST.get('apartment')
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        check_in = request.POST.get('check_in')
        check_in_time = request.POST.get('check_in_time')
        check_out = request.POST.get('check_out')
        check_out_time = request.POST.get('check_out_time')
        guest = request.POST.get('guest')

        customer, created = Customer.objects.get_or_create(
            name=full_name,
            phone=phone,
            email=email
        )
        print(customer)
        existing_booking = Booking.objects.filter(
                apartment_id=apartment,
                check_in_date__lte=check_out,
                check_out_date__gte=check_in
            )
            
        if existing_booking:
                messages.error(request,"No booking available for selected dates")
                # Raise a validation error if a booking already exists
        else:
                # Create a new booking object
                Booking.objects.create(
                    email=email,
                    phone=phone,
                    check_in_date=check_in,
                    check_in_time=check_in_time,
                    check_out_date=check_out,
                    check_out_time=check_out_time,
                    guest=guest,
                    apartment=Apartment.objects.get(id=apartment),
                    customer=customer,
                    full_name=full_name
                )


                # Booking.objects.create(
                #     email=email,
                #     phone=phone,
                #     check_in_date=check_in,
                #     check_in_time=check_in_time,
                #     check_out_date=check_out,
                #     check_out_time=check_out_time,
                #     guest=guest,
                #     apartment=Apartment.objects.get(id=apartment),
                #     customer=customer,
                #     full_name=full_name
                # )

                email_body = """\
                        <table class="body-wrap" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; width: 100%; background-color: #f6f6f6; margin: 0;" bgcolor="#f6f6f6">
                            <tbody>
                                <tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
                                    <td style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; vertical-align: top; margin: 0;" valign="top"></td>
                                    <td class="container" width="600" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; vertical-align: top; display: block !important; max-width: 600px !important; clear: both !important; margin: 0 auto;"
                                        valign="top">
                                        <div class="content" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; max-width: 600px; display: block; margin: 0 auto; padding: 20px;">
                                            <table class="main" width="100%" cellpadding="0" cellspacing="0" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; border-radius: 3px; background-color: #fff; margin: 0; border: 1px solid #e9e9e9;"
                                                bgcolor="#fff">
                                                <tbody>
                                                    <tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
                                                        <td class="" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 16px; vertical-align: top; color: #fff; font-weight: 500; text-align: center; border-radius: 3px 3px 0 0; background-color: #38414a; margin: 0; padding: 20px;"
                                                            align="center" bgcolor="#71b6f9" valign="top">
                                                            <a href="#" style="font-size:32px;color:#fff;">Booking Confirmation</a> <br>
                                                            <span style="margin-top: 10px;display: block; color:yellow">Hi ,your Booking was successfull<b></b>.</span>
                                                        </td>
                                                    </tr>
                                                    <tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
                                                        <td class="content-wrap" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; vertical-align: top; margin: 0; padding: 20px;" valign="top">
                                                            <table width="100%" cellpadding="0" cellspacing="0" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
                                                                <tbody>
                                                                    <tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
                                                                        <td class="content-block" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; vertical-align: top; margin: 0; padding: 0 0 20px;" valign="top">

                                                                        </td>
                                                                    </tr>
                                                                    <tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
                                                                        <td class="content-block" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; vertical-align: top; margin: 0; padding: 0 0 20px;" valign="top">
                                                                        <!-- Please click on the link below to Join. -->
                                                                        </td>
                                                                    </tr>
                                                                    <tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
                                                                        <td class="content-block" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; vertical-align: top; margin: 0; padding: 0 0 20px;" valign="top">
                                                                            <a href="" class="btn-primary" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; color: #FFF; text-decoration: none; line-height: 2em; font-weight: bold; text-align: center; cursor: pointer; display: inline-block; border-radius: 5px; text-transform: capitalize; background-color: #f1556c; margin: 0; border-color: #f1556c; border-style: solid; border-width: 8px 16px;">
                                                            Check here</a> </td>
                                                            </tr>
                                                            <tr>
                    
                                                                    </tr>
                                                                    <tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
                                                                        <td class="content-block" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; vertical-align: top; margin: 0; padding: 0 0 20px;" valign="top">
                                                                            Thanks for choosing us<b> </b> .
                                                                        </td>
                                                                    </tr>
                                                                </tbody>
                                                            </table>
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                            <div class="footer" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; width: 100%; clear: both; color: #999; margin: 0; padding: 20px;">
                                                <table width="100%" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
                                                    <tbody>
                                                        <tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
                                                            <td class="" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 16px; vertical-align: top; color: #fff; font-weight: 500; text-align: center; border-radius: 3px 3px 0 0; background-color: #38414a; margin: 0; padding: 20px;"
                                                                align="center" bgcolor="#71b6f9" valign="top">
                                                                <a href="#" style="font-size:32px;color:#fff;">Booking Confirmation</a> <br>
                                                                <span style="margin-top: 10px;display: block; color:yellow">Hi ,your Booking was successfull<b></b>.</span>
                                                            </td>
                                                        </tr>
                                                        <tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
                                                            <td class="content-wrap" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; vertical-align: top; margin: 0; padding: 20px;" valign="top">
                                                                <table width="100%" cellpadding="0" cellspacing="0" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
                                                                    <tbody>
                                                                        <tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
                                                                            <td class="content-block" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; vertical-align: top; margin: 0; padding: 0 0 20px;" valign="top">

                                                                            </td>
                                                                        </tr>
                                                                        <tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
                                                                            <td class="content-block" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; vertical-align: top; margin: 0; padding: 0 0 20px;" valign="top">
                                                                            <!-- Please click on the link below to Join. -->
                                                                            </td>
                                                                        </tr>
                                                                        <tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
                                                                            <td class="content-block" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; vertical-align: top; margin: 0; padding: 0 0 20px;" valign="top">
                                                                                <a href="" class="btn-primary" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; color: #FFF; text-decoration: none; line-height: 2em; font-weight: bold; text-align: center; cursor: pointer; display: inline-block; border-radius: 5px; text-transform: capitalize; background-color: #f1556c; margin: 0; border-color: #f1556c; border-style: solid; border-width: 8px 16px;">
                                                                Check here</a> </td>
                                                                </tr>
                                                                <tr>
                        
                                                                        </tr>
                                                                        <tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
                                                                            <td class="content-block" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; vertical-align: top; margin: 0; padding: 0 0 20px;" valign="top">
                                                                                Thanks for choosing us<b> </b> .
                                                                            </td>
                                                                        </tr>
                                                                    </tbody>
                                                                </table>
                                                            </td>
                                                        </tr>
                                                    </tbody>
                                                </table>
                                                <div class="footer" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; width: 100%; clear: both; color: #999; margin: 0; padding: 20px;">
                                                    <table width="100%" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
                                                        <tbody>
                                                            <tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">

                                                                </td>
                                                            </tr>
                                                        </tbody>
                                                    </table>
                                                </div>
                                            </div>
                                        </td>
                                        <td style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; vertical-align: top; margin: 0;" valign="top"></td>
                                    </tr>
                                </tbody>
                            </table>
                            """

                # email_body = email_body.replace('{{applicant.name}}',applicant.name).replace('{{job.title}}',job.title)
                # o=request.session["orgname"]
                # subject=f'Application  to Job'

                from_email = 'dowelllogintest@gmail.com'
                # from_email='stay@capitalapartment.co.uk'

                to_email = email
                # send_mail(subject, "lav", from_email, [to_email], fail_silently=False,html_message=email_body)
                email1 = EmailMessage("Booking Confimration",
                                    email_body, from_email, [to_email])
                email1.content_subtype = "html"  # this is the crucial part
                # email1.attach_file(applicant.resume.path, 'application/pdf')
                email1.send()

                return redirect('apartments_booking_succesful', apartment)

    context = {}
    apartment = Apartment.objects.get(id=id)
    context['apartment'] = apartment

    return render(request, 'apartment_detail.html', context)


def apartments_booking_succesful(request, id):

    context = {}
    context['apartment'] = Apartment.objects.get(id=id)

    return render(request, 'apartment_booking_succesful.html', context)

