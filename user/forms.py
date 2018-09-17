from django import forms
from django.core.validators import RegexValidator

from django_drive.utils import hashed_pwd
from .models import User

username_validator = RegexValidator('^[A-Za-z0-9_.]+$')
phone_number_validator = RegexValidator('^[0-9]{10}$')


class RegistrationFrom(forms.Form):
    username = forms.CharField(label='Username', max_length=15, min_length=7, required=True,
                               validators=[username_validator])
    email = forms.EmailField(label='Email', required=True)
    phone_number = forms.CharField(label='Phone number', required=True, validators=[phone_number_validator])
    date_of_birth = forms.DateField(label='Date of Birth', required=True)
    password = forms.CharField(label='Password', required=True, min_length=8, max_length=20)
    confirm_password = forms.CharField(label=' Confirm Password', required=True, min_length=8, max_length=20, )

    def clean(self):
        cleaned_data = super(RegistrationFrom, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if confirm_password != password:
            raise forms.ValidationError("Password and Confirm Password should be same!!")
        username = cleaned_data.get('username')
        user = User.objects.filter(username=username).first()
        if user:
            raise forms.ValidationError("Username already exists. Please choose another")
        email = cleaned_data.get('email')
        email_id = User.objects.filter(email=email)
        if email_id:
            raise forms.ValidationError("Email ID already exists. Please choose another")
        return cleaned_data


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email', required=True)
    password = forms.CharField(label='Password', required=True, min_length=8, max_length=20)
    remember = forms.BooleanField(label='Keep me logged in', required=False)

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        email = cleaned_data.get('email')
        email_id = User.objects.filter(email=email)
        if not email_id:
            raise forms.ValidationError("Email id is not registered. Please register")
        pwd = hashed_pwd(cleaned_data.get('password'))
        password = User.objects.filter(email=email).first()
        if not pwd == password.password:
            raise forms.ValidationError("Incorrect Password")
