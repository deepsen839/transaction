from django.contrib import admin
from .models import UserDetails,UserProfile,Transaction,SuperUserReceived,SheduleOfCharges
# Register your models here.

@admin.register(UserDetails)
class UserDetailsAdmin(admin.ModelAdmin):
    list_display = ('id','user','user_type','wallet_amount')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user_id','other','amount_requested','amount_given','accepted','request_date','update_date')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('from_user','to_user','transaction_amount','from_user_percentage','from_user_charge','to_user_percentage','to_user_charge')

@admin.register(SuperUserReceived)
class SuperUserReceivedAdmin(admin.ModelAdmin):
    list_display = ('from_user','amount','charges','tarnsaction_id','date')

@admin.register(SheduleOfCharges)
class SheduleOfChargesAdmin(admin.ModelAdmin):
    list_display = ('user_type','percentage_of_charge')           