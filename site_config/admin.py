from django.contrib import admin
from .models import *
from django import forms
from django.http import HttpResponseRedirect

# Register your models here.
# @admin.register(SiteMetaData)
# class SiteMetaDataAdmin(admin.ModelAdmin):
#     list_display = ['meta_keywords', 'meta_description']


class ContactInfoAdminForm(forms.ModelForm):
    class Meta:
        model = ContactInfo
        fields = "__all__"

    def clean(self):
        instance = self.instance
        if not instance.pk and ContactInfo.objects.exists():
            raise forms.ValidationError('There can only be one instance of ContactInfo.')
        return super(ContactInfoAdminForm, self).clean()

class ContactInfoAdmin(admin.ModelAdmin):
    form = ContactInfoAdminForm

admin.site.register(ContactInfo, ContactInfoAdmin)


class BusinessInfoAdminForm(forms.ModelForm):
    class Meta:
        model = BusinessInfo
        fields = "__all__"

    def clean(self):
        instance = self.instance
        if not instance.pk and BusinessInfo.objects.exists():
            raise forms.ValidationError('There can only be one instance of BusinessInfo.')
        return super(BusinessInfoAdminForm, self).clean()

class BusinessInfoAdmin(admin.ModelAdmin):
    form = BusinessInfoAdminForm

admin.site.register(BusinessInfo, BusinessInfoAdmin)


class SiteMetaDataAdminForm(forms.ModelForm):
    class Meta:
        model = SiteMetaData
        fields = "__all__"

    def clean(self):
        instance = self.instance
        if not instance.pk and SiteMetaData.objects.exists():
            raise forms.ValidationError('There can only be one instance of SiteMetaData.')
        return super(SiteMetaDataAdminForm, self).clean()

class SiteMetaDataAdmin(admin.ModelAdmin):
    form = SiteMetaDataAdminForm

admin.site.register(SiteMetaData, SiteMetaDataAdmin)


class SocialLinksAdminForm(forms.ModelForm):
    class Meta:
        model = SocialLinks
        fields = "__all__"

    def clean(self):
        instance = self.instance
        if not instance.pk and SocialLinks.objects.exists():
            raise forms.ValidationError('There can only be one instance of SocialLinks.')
        return super(SocialLinksAdminForm, self).clean()

class SocialLinksAdmin(admin.ModelAdmin):
    form = SocialLinksAdminForm

admin.site.register(SocialLinks, SocialLinksAdmin)



class TermsOfUseAdminForm(forms.ModelForm):
    class Meta:
        model = TermsOfUse
        fields = "__all__"

    def clean(self):
        instance = self.instance
        if not instance.pk and TermsOfUse.objects.exists():
            raise forms.ValidationError('There can only be one instance of TermsOfUse.')
        return super(TermsOfUseAdminForm, self).clean()

class TermsOfUseAdmin(admin.ModelAdmin):
    form = TermsOfUseAdminForm

admin.site.register(TermsOfUse, TermsOfUseAdmin)

class PrivacyPolicyAdminForm(forms.ModelForm):
    class Meta:
        model = PrivacyPolicy
        fields = "__all__"

    def clean(self):
        instance = self.instance
        if not instance.pk and PrivacyPolicy.objects.exists():
            raise forms.ValidationError('There can only be one instance of PrivacyPolicy.')
        return super(PrivacyPolicyAdminForm, self).clean()

class PrivacyPolicyAdmin(admin.ModelAdmin):
    form = PrivacyPolicyAdminForm

admin.site.register(PrivacyPolicy, PrivacyPolicyAdmin)

class EnvironmentalPolicyAdminForm(forms.ModelForm):
    class Meta:
        model = EnvironmentalPolicy
        fields = "__all__"

    def clean(self):
        instance = self.instance
        if not instance.pk and EnvironmentalPolicy.objects.exists():
            raise forms.ValidationError('There can only be one instance of EnvironmentalPolicy.')
        return super(EnvironmentalPolicyAdminForm, self).clean()

class EnvironmentalPolicyAdmin(admin.ModelAdmin):
    form = EnvironmentalPolicyAdminForm

admin.site.register(EnvironmentalPolicy, EnvironmentalPolicyAdmin)