from django.db import models
from django.core.exceptions import ValidationError
from ckeditor.fields import RichTextField

class SiteMetaData(models.Model):
    meta_keywords = models.TextField(blank=True, help_text="SEO meta keywords for the site.")
    meta_description = models.TextField(blank=True, help_text="SEO meta description for the site.")
    logo = models.ImageField(upload_to="logos/")
    def __str__(self):
        return "Site Meta Data"
    def clean(self):
            if not self.pk and SiteMetaData.objects.exists():
                raise ValidationError('There can only be one instance of SiteMetaData.')

    def save(self, *args, **kwargs):
        if not self.pk and SiteMetaData.objects.exists():
            # if the object is new and another instance already exists in the database, raise an exception
            raise ValidationError('There can only be one instance of SiteMetaData.')
        return super(SiteMetaData, self).save(*args, **kwargs)
class ContactInfo(models.Model):
    phone_number = models.CharField(max_length=15, blank=True, help_text="Contact phone number.")
    email = models.EmailField(blank=True, help_text="Contact email address.")
    address = models.TextField(blank=True, help_text="Physical address.")

    def __str__(self):
        return "Contact Information"
    def clean(self):
        if not self.pk and ContactInfo.objects.exists():
            raise ValidationError('There can only be one instance of ContactInfo.')

class BusinessInfo(models.Model):
    name = models.CharField(max_length=100, help_text="Name of the business.")
    about = models.TextField(blank=True, help_text="About the business.")

    def __str__(self):
        return self.name

    def clean(self):
        if not self.pk and BusinessInfo.objects.exists():
            raise ValidationError('There can only be one instance of BusinessInfo.')


class SocialLinks(models.Model):
    facebook = models.URLField(blank=True, null=True, verbose_name="Facebook URL")
    twitter = models.URLField(blank=True, null=True, verbose_name="Twitter URL")
    instagram = models.URLField(blank=True, null=True, verbose_name="Instagram URL")
    linkedin = models.URLField(blank=True, null=True, verbose_name="LinkedIn URL")
    youtube = models.URLField(blank=True, null=True, verbose_name="YouTube URL")
    tripadvisor = models.URLField(blank=True, null=True, verbose_name="TripAdvisor URL")

    def clean(self):
        if not self.pk and SocialLinks.objects.exists():
            raise ValidationError('There can only be one instance of SocialLinks.')

    def __str__(self):
        return "Social Links"


class TermsOfUse(models.Model):
    content = RichTextField()

    def save(self, *args, **kwargs):
        if not self.pk and TermsOfUse.objects.exists():
            raise ValidationError('There is can be only one TermsOfUse instance')
        return super(TermsOfUse, self).save(*args, **kwargs)

    def __str__(self):
        return "Terms of Use"

class PrivacyPolicy(models.Model):
    content = RichTextField()

    def save(self, *args, **kwargs):
        if not self.pk and PrivacyPolicy.objects.exists():
            raise ValidationError('There is can be only one PrivacyPolicy instance')
        return super(PrivacyPolicy, self).save(*args, **kwargs)

    def __str__(self):
        return "Privacy Policy"

class EnvironmentalPolicy(models.Model):
    content = RichTextField()

    def save(self, *args, **kwargs):
        if not self.pk and EnvironmentalPolicy.objects.exists():
            raise ValidationError('There is can be only one EnvironmentalPolicy instance')
        return super(EnvironmentalPolicy, self).save(*args, **kwargs)

    def __str__(self):
        return "Environmental Policy"