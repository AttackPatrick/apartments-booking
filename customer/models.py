
from django.db import models

class Customer(models.Model):
    name            = models.CharField(max_length=100)
    phone           = models.CharField(max_length=100)
    email           = models.CharField(max_length=100)
    created_at      = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name