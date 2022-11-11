from django.shortcuts import render,redirect
# Create your views here.
from .forms import *
from .models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
import json
def registration(request):
    if request.user.is_authenticated:
        return redirect('/userprofile/') 
    user_register_form = UserForm(request.POST or None)
    if request.method == 'POST':
        if user_register_form.is_valid():
           user_register_form.save()
           username = user_register_form.cleaned_data.get('username')
           user_type = user_register_form.cleaned_data.get('user_type')
           if user_type == 0:
            wallet_amount=1000
           else:
            wallet_amount=2500
            user = User.objects.get(username=username)
            user_data = UserDetails.objects.create(user=user, wallet_amount=wallet_amount, user_type=user_type)
            user_data.save() 
            return redirect('/')
    return render(request,'registration.html',{'registerform':user_register_form})

def userlogin(request):
    if request.user.is_authenticated:
        return redirect('userprofile/') 
    login_form = userloginForm(request.POST or None)
    if request.method == "POST":
        if login_form.is_valid():
            user = authenticate(request,username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                login(request, user)
                return redirect('/userprofile/')
        # return redirect('/')
    return render(request,'login.html',{'login_form':login_form})
        
@login_required
def userlogout(request):
    logout(request)
    return redirect('/')
@login_required
def user_profile(request):
    profile_form = ProfileForm(request.user,request.POST or None)
    print()
    transaction_record_for_user = UserProfile.objects.filter(Q(user_id=request.user.id)| Q(other_id=request.user.id)).all()
    print(transaction_record_for_user.count())
    if request.method =='POST':
        if profile_form.is_valid():
            user = UserProfile(
            user_id = request.user.id,    
            other=profile_form.cleaned_data['userlist'],
            amount_requested=profile_form.cleaned_data['amount'],
            )
            user.save()
            return redirect('/userprofile/')     
    return render(request,'profile.html',{'transaction_record':transaction_record_for_user,'transaction_form':profile_form})


def savetransaction(request):
    if request.method=='POST':
        id = request.POST.get('id')
        accepted = request.POST.get('accepted')
        userprofile = UserProfile.objects.filter(pk=id).first()
        userprofile.accepted=accepted
        userprofile.save()
        if accepted == '0':
            return HttpResponse(json.dumps({'response':200,'success':True}),content_type="application/json")
        elif accepted == '1':
            payee = UserDetails.objects.filter(user=userprofile.user).first()
            receiver = UserDetails.objects.filter(user=userprofile.other).first()
            from_user_charge_percentage = receiver_user_charge_percentage = 0
            if payee.user_type == 1:
                from_user_charge_percentage = 3
            else:
                from_user_charge_percentage = 5
            
            if receiver.user_type == 1:
                receiver_user_charge_percentage = 1
            else:
                receiver_user_charge_percentage = 3   

            from_user_charge = (userprofile.amount_requested*from_user_charge_percentage)/100
            to_user_charge = (userprofile.amount_requested*receiver_user_charge_percentage)/100
            print(userprofile.amount_requested,payee.user_type,from_user_charge_percentage,receiver_user_charge_percentage)
            transaction_between_payee_and_receiver =Transaction(from_user = userprofile.user,
            to_user = userprofile.other,
            transaction_amount = userprofile.amount_requested,
            from_user_charge = from_user_charge,
            to_user_charge = to_user_charge,
            from_user_percentage = from_user_charge_percentage,
            to_user_percentage = receiver_user_charge_percentage
            )
            transaction_between_payee_and_receiver.save()

            superuser = User.objects.filter(is_superuser=1).first()
            superuser_received_from_payee = SuperUserReceived(
                from_user=userprofile.user,
                amount = from_user_charge,
                charges = from_user_charge_percentage,
                tarnsaction_id_id=transaction_between_payee_and_receiver.id,
            )
            superuser_received_from_payee.save()
            superuser_received_from_receiver = SuperUserReceived(
                from_user=userprofile.other,
                amount = to_user_charge,
                charges = receiver_user_charge_percentage,
                tarnsaction_id_id=transaction_between_payee_and_receiver.id,
            )
            superuser_received_from_receiver.save()
            return HttpResponse(json.dumps({'response':200,'success':True}),content_type="application/json")