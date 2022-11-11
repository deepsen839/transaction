from django.db import models
from django import forms
from django.contrib.auth.models import User

# Create your models here.

usertype = (('','select'),(1,'premium'),(0,"Non Premium"))

class UserDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.BooleanField(default=0)
    wallet_amount = models.FloatField(default=0)

class Transaction(models.Model):
    from_user = models.ForeignKey(User,related_name='from_user',on_delete=models.CASCADE)
    to_user = models.ForeignKey(User,related_name='to_user',on_delete=models.CASCADE)
    transaction_amount = models.IntegerField(default=0)
    from_user_percentage = models.FloatField(default=0)
    from_user_charge = models.FloatField(default=0)
    to_user_percentage = models.FloatField(default=0)
    to_user_charge = models.FloatField(default=0)
    
class SuperUserReceived(models.Model):
    from_user = models.ForeignKey(User,on_delete=models.CASCADE)
    amount = models.FloatField(default=0)
    charges = models.FloatField(default=0)
    tarnsaction_id=models.ForeignKey(Transaction,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

class SheduleOfCharges(models.Model):
    user_type = models.CharField(max_length=50,choices=usertype)
    percentage_of_charge = models.FloatField(default=0)

class UserProfile(models.Model):
    user = models.ForeignKey(User,related_name='user',on_delete=models.CASCADE)
    other = models.ForeignKey(User,related_name='other',on_delete=models.CASCADE)
    amount_requested = models.FloatField(default=0)
    amount_given = models.FloatField(default=0)
    accepted= models.BooleanField(default=0)
    request_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(null=True)    