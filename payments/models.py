from django.db import models
from payments.models import *
from apartments.models import *



class Payment(models.Model):
    booking                     =     models.OneToOneField(Booking,on_delete=models.CASCADE)
    apartment                   =     models.ForeignKey(Apartment,on_delete=models.CASCADE)
    payment_recieved            =     models.IntegerField()
    payment_recieved_date_time  =     models.DateTimeField()
    created_at                  =     models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self(self.id)