from .models import UserProfile
from django import forms
from django.http import request 
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserForm(UserCreationForm):
    usertype = (('','select'),(1,'premium'),(2,"Non Premium"))
    email = forms.EmailField(required=True)
    user_type = forms.ChoiceField(choices=usertype,required=True)
    wallet_amount = forms.HiddenInput()
    class Meta:
        model = User
        fields = ("username", "email","password1", "password2")



class ProfileForm(forms.Form):
    userlist=forms.ModelChoiceField(queryset=None)
    amount = forms.CharField(required=True)
    def __init__(self,user,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        superuseradmin = User.objects.filter(is_superuser=1).first()
        # super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['userlist'].queryset = User.objects.exclude(id__in=(self.user.id,superuseradmin.id)).all()

class userloginForm(forms.Form):
    username = forms.CharField(max_length=200,required=True)
    password = forms.CharField(widget=forms.PasswordInput(),required=True,error_messages={'required': 'Please enter correct password'})


class ProfilesendMoneyForm(forms.Form):
    userlist=forms.ModelChoiceField(queryset=None)
    amount = forms.CharField(required=True)
    def __init__(self,user,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        superuseradmin = User.objects.filter(is_superuser=1).first()
        # super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['userlist'].queryset = User.objects.exclude(id__in=(self.user.id,superuseradmin.id)).all()
