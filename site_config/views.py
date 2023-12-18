
# Create your views here.

from django.shortcuts import render
from .models import *

def global_context(request):
    try:
        metadata = SiteMetaData.objects.first()
    except SiteMetaData.DoesNotExist:
        metadata = None

    try:
        contact_info = ContactInfo.objects.first()
    except ContactInfo.DoesNotExist:
        contact_info = None

    try:
        business_info = BusinessInfo.objects.first()
    except BusinessInfo.DoesNotExist:
        business_info = None
    try:
        social_links = SocialLinks.objects.first()
    except BusinessInfo.DoesNotExist:
        social_links = None

    return {
        'metadata': metadata,
        'contact_info': contact_info,
        'business_info': business_info,
        'social_links': social_links
    }


def terms_of_use_view(request):
    try:
        terms = TermsOfUse.objects.first()
    except TermsOfUse.DoesNotExist:
        terms = None
    return render(request, 'terms_of_use.html', {'terms_of_use': terms})

def privacy_policy_view(request):
    try:
        privacy = PrivacyPolicy.objects.first()
    except PrivacyPolicy.DoesNotExist:
        privacy = None
    return render(request, 'privacy_policy.html', {'privacy_policy': privacy})

def environmental_policy_view(request):
    try:
        policy = EnvironmentalPolicy.objects.first()
    except EnvironmentalPolicy.DoesNotExist:
        policy = None
    return render(request, 'environmental_policy.html', {'environmental_policy': policy})
