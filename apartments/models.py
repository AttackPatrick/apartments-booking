from django.db import models
from ckeditor.fields import RichTextField
from django.db.models.signals import post_save
from customer.models import Customer
from datetime import datetime
import warnings

class ApartmentCategory(models.Model):

    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ApartmentOwner(models.Model):

    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    payment_options = models.CharField(max_length=255)
    ownership_details = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name


class ApartmentOwnerAddress(models.Model):
    postcode = models.CharField(max_length=20)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    street = models.CharField(max_length=60)
    owner = models.ForeignKey(ApartmentOwner, on_delete=models.CASCADE)

    def __str__(self):
        return self.postcode


class Apartment(models.Model):

    APARTMENT_CHOICES = (
        ("Available", "Available"),
        ("Booked", "Booked")
    )

    clean_status = models.BooleanField(default=False)
    inspected_status = models.BooleanField(default=False)
    title = models.CharField(max_length=100)
    apartment_status = models.CharField(
        max_length=255, choices=APARTMENT_CHOICES, default='Available')
    services = models.CharField(max_length=255)
    capacity = models.IntegerField()
    bed = models.CharField(max_length=100)

    price = models.IntegerField()
    persons = models.IntegerField()

    category = models.ForeignKey(ApartmentCategory, on_delete=models.CASCADE)
    owner = models.ForeignKey(
        ApartmentOwner, on_delete=models.CASCADE, null=True, blank=True)

    title_image = models.ImageField(upload_to='apartments')

    description = RichTextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        from apartments.models import ApartmentAddress
        apartment_address = ApartmentAddress.objects.filter(apartment=self)

        if apartment_address.count():
            name = "pass"

        return f'{self.title} - {self.bed} '

    def apartment_images(self):
        from apartments.models import ApartmentImage

        for i in ApartmentImage.objects.filter(apartment=self):
            print(i.image.url)

        return ApartmentImage.objects.filter(apartment=self)


class ApartmentAddress(models.Model):
    postcode = models.CharField(max_length=20)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    street = models.CharField(max_length=60)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.postcode)


class ApartmentImage(models.Model):

    image = models.ImageField(upload_to='apartments_images')

    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.apartment.title


class Booking(models.Model):

    # available = models.BooleanField(default=True)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, null=True, blank=True)

    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    guest = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)

    check_in_date = models.DateField()
    check_in_time = models.TimeField()
    check_out_date = models.DateField()
    check_out_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.apartment.title


class ApartmentCleaner(models.Model):
    title = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255,null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ApartmentCleaningExpense(models.Model):

    expense = models.IntegerField()
    cleaner = models.ForeignKey(ApartmentCleaner, on_delete=models.CASCADE)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.apartment.title


class ApartmentMaintenance(models.Model):

    expense = models.IntegerField()
    description = models.TextField()
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.apartment.title


class ApartmentEarning(models.Model):
    cleaning_expenses = models.IntegerField(default=0)
    total_earnings = models.IntegerField(default=0)
    turnover = models.IntegerField(default=0)
    apartment = models.OneToOneField(Apartment, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id) + "-" + self.apartment.title


class ApartmentEarningTransaction(models.Model):
    CHOICES = (
        ('Credit', 'Credit'),
        ('Debit', 'Debit')
    )

    transaction_type = models.CharField(max_length=100, choices=CHOICES)
    transaction_amount = models.IntegerField(default=0)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    apartment_earning = models.ForeignKey(
        ApartmentEarning, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id) + "-" + self.apartment.title


def create_invoice(sender, instance, created, **kwargs):

    apartment_e_obj, _ = ApartmentEarning.objects.get_or_create(
        apartment=instance.apartment
    )

    check_in_date_ = str(instance.check_in_date)
    check_out_date_ = str(instance.check_out_date)

    check_in_date = datetime.strptime(check_in_date_, '%Y-%m-%d')
    check_out_date = datetime.strptime(check_out_date_, '%Y-%m-%d')
    total_days = abs(check_out_date - check_in_date)
    total_days = total_days.days
    total_price = total_days * instance.apartment.price

    ApartmentEarningTransaction.objects.create(
        transaction_type="Credit",
        transaction_amount=total_price,
        apartment=instance.apartment,
        apartment_earning=apartment_e_obj,
    )

    total_earning = 0
    for obj in ApartmentEarningTransaction.objects.filter(apartment=instance.apartment):
        total_earning += obj.transaction_amount

    total_cleaning_expense = 0
    for obj in ApartmentCleaningExpense.objects.filter(apartment=instance.apartment):
        total_cleaning_expense += obj.expense

    apartment_e_obj.cleaning_expenses = total_cleaning_expense
    apartment_e_obj.total_earnings = total_earning
    apartment_e_obj.turnover = total_earning - total_cleaning_expense
    apartment_e_obj.save()


def email_customer(sender, instance, created, **kwargs):

    pass


post_save.connect(create_invoice, sender=Booking)


# change auto expense
def create_expense(sender, instance, created, **kwargs):
    apartment_e_obj, _ = ApartmentEarning.objects.get_or_create(
        apartment=instance.apartment
    )
    apartment_e_obj.cleaning_expenses = apartment_e_obj.cleaning_expenses + instance.expense
    apartment_e_obj.turnover = apartment_e_obj.turnover - instance.expense
    apartment_e_obj.save()


post_save.connect(create_expense, sender=ApartmentCleaningExpense)


def create_maintenance(sender, instance, created, **kwargs):
    apartment_e_obj, _ = ApartmentEarning.objects.get_or_create(
        apartment=instance.apartment
    )
    apartment_e_obj.cleaning_expenses = apartment_e_obj.cleaning_expenses + instance.expense
    apartment_e_obj.turnover = apartment_e_obj.turnover - instance.expense
    apartment_e_obj.save()


post_save.connect(create_maintenance, sender=ApartmentMaintenance)