from django.contrib import messages
from django.contrib.auth import authenticate, login as initiate_login
from django.shortcuts import redirect, render, reverse

from drive.views import data
from .forms import LoginForm, RegistrationFrom
from .models import User


def register(request):
    """
    Registers new users and renders template for registration form
    :param request: incoming request object
    :return: rendered template
    """
    if request.method == "POST":
        form = RegistrationFrom(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            user = User(username=username, email=form.cleaned_data.get('email'),
                        date_of_birth=form.cleaned_data.get('date_of_birth'),
                        phone_number=form.cleaned_data.get('phone_number'),
                        password=form.cleaned_data.get('password'))
            user.save()
            messages.success(request, f'Account created for {username} successfully. You can now login !')
            return redirect('login')
    else:
        form = RegistrationFrom()
    return render(request, 'user/register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user:
                initiate_login(request, user)
            messages.success(request, 'You have logged in successfully')
            return redirect(reverse(data))
    else:
        form = LoginForm()
    return render(request, 'user/login.html', {'form': form})
