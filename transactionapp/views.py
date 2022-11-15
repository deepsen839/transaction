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

            if user_type == '1':
                wallet_amount=2500
            else:
                wallet_amount=1000
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
    sendMoneyForm = ProfilesendMoneyForm(request.user) 
    transaction_record_for_user = UserProfile.objects.filter(Q(user_id=request.user.id)| Q(other_id=request.user.id)).all()
    if request.method =='POST':
        if profile_form.is_valid():
            user = UserProfile(
            user_id = request.user.id,    
            other=profile_form.cleaned_data['userlist'],
            amount_requested=profile_form.cleaned_data['amount'],
            )
            user.save()
            return redirect('/userprofile/')     
    return render(request,'profile.html',{'transaction_record':transaction_record_for_user,'transaction_form':profile_form,'sendMoneyForm':sendMoneyForm})


@login_required
def send_money(request):
    sendMoneyForm = ProfilesendMoneyForm(request.user,request.POST or None) 
    if request.method =='POST':
        if sendMoneyForm.is_valid():
            sendfrom = User.objects.filter(pk=request.user.id).first()
            sentto= User.objects.filter(pk=request.POST.get('userlist')).first()
            user1 = UserProfile(
            user = sendfrom,    
            other=sentto,
            amount_given=sendMoneyForm.cleaned_data['amount'],
            )
            user1.save()
    return redirect('/userprofile/')     
    

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
            if userprofile.amount_requested > 0:
                receiver = UserDetails.objects.filter(user=userprofile.user).first()
                payee = UserDetails.objects.filter(user=userprofile.other).first()
            if userprofile.amount_given > 0:
                 payee = UserDetails.objects.filter(user=userprofile.user).first()
                 receiver = UserDetails.objects.filter(user=userprofile.other).first()
     
            superuser = User.objects.filter(is_superuser=1).first()
            superuserdetails = UserDetails.objects.filter(user=superuser).first()
            from_user_charge_percentage = receiver_user_charge_percentage = 0
            if payee.user_type == 1:
                from_user_charge_percentage = 3
            else:
                from_user_charge_percentage = 5
            
            if receiver.user_type == 1:
                receiver_user_charge_percentage = 1
            else:
                receiver_user_charge_percentage = 3   


            if userprofile.amount_requested > 0:
                print('1111111111')
                from_user_charge = (userprofile.amount_requested*from_user_charge_percentage)/100
                to_user_charge = (userprofile.amount_requested*receiver_user_charge_percentage)/100
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
                payee.wallet_amount = payee.wallet_amount-(from_user_charge+userprofile.amount_requested)
                payee.save()

                receiver.wallet_amount = (receiver.wallet_amount+userprofile.amount_requested)-to_user_charge
                receiver.save()
                superuserdetails.wallet_amount = superuserdetails.wallet_amount+to_user_charge+from_user_charge
                superuserdetails.save()

            # =========================

            if userprofile.amount_given > 0:
                print('22222222222')
                from_user_charge = (userprofile.amount_given*from_user_charge_percentage)/100
                to_user_charge = (userprofile.amount_given*receiver_user_charge_percentage)/100
                transaction_between_payee_and_receiver =Transaction(from_user = userprofile.user,
                to_user = userprofile.other,
                transaction_amount = userprofile.amount_given,
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
                payee.wallet_amount = payee.wallet_amount-(from_user_charge+userprofile.amount_given)
                payee.save()

                receiver.wallet_amount = (receiver.wallet_amount+userprofile.amount_given)-to_user_charge
                receiver.save()
                superuserdetails.wallet_amount = superuserdetails.wallet_amount+to_user_charge+from_user_charge
                superuserdetails.save()







            return HttpResponse(json.dumps({'response':200,'success':True}),content_type="application/json")