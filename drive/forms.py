from django import forms
from django.core.validators import RegexValidator
from django.utils import html

username_validator = RegexValidator('^[A-Za-z0-9_.]+$')
phone_number_validator = RegexValidator('^[0-9]{10}$')


class SubmitButtonWidget(forms.Widget):
    def render(self, name, value, attrs=None):
        return '<input type="submit" name="%s" value="%s">' % (html.escape(name), html.escape(value))


class SubmitButtonField(forms.Field):
    def __init__(self, *args, **kwargs):
        if not kwargs:
            kwargs = {}
        kwargs["widget"] = SubmitButtonWidget

        super(SubmitButtonField, self).__init__(*args, **kwargs)

    def clean(self, value):
        return value


class RegistrationFrom(forms.Form):
    username = forms.CharField(label='Username', max_length=15, min_length=7, required=True,
                               validators=[username_validator])
    email = forms.EmailField(label='Email', required=True)
    phone_number = forms.IntegerField(label='Phone number', required=True, validators=[phone_number_validator])
    date_of_birth = forms.DateField(label='Date of Birth', required=True)
    password = forms.CharField(label='Password', required=True, min_length=8, max_length=20)
    confirm_password = forms.CharField(label=' Confirm Password', required=True, min_length=8, max_length=20, )
    submit = SubmitButtonField(label='', initial='Sign Up')

    def clean(self):
        cleaned_data = super(RegistrationFrom,self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if confirm_password != password:
            raise forms.ValidationError("Password and Confirm Password should be same!!")
        return cleaned_data


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email', required=True)
    password = forms.CharField(label='Password', required=True, min_length=8, max_length=20)
    remember = forms.BooleanField(label='Keep me logged in')
    log_in = SubmitButtonField(label='', initial='Log In')
