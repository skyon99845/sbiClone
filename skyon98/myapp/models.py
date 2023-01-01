from django.db import models
from datetime import datetime, date
# Create your models here.


class Customer(models.Model):
    customername = models.CharField(max_length=20, unique=True)
    initialbal = models.IntegerField(default=0)
    accno = models.IntegerField(default=0)
    contactnumber = models.IntegerField(default=0)
    email=models.EmailField(max_length=100)
    pernumber = models.IntegerField(default=0)
    operator = models.CharField(max_length=3)

    def __str__(self):
        return self.username


class Userfeed(models.Model):
    contactno = models.IntegerField(default=0)
    complaintdes = models.CharField(max_length=500)

    def __str__(self):
        return self.contactno

class OTP(models.Model):
    identity = models.IntegerField(unique=True)
    otpnumber=models.IntegerField(default=0)
