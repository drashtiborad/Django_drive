from django.shortcuts import render, redirect, reverse
from .forms import RegistrationFrom, LoginForm
from django.contrib import messages
from drive.views import data


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
            messages.success(request, f'Account created for {username} successfully. You can now login !')
            return redirect('login')
    else:
        form = RegistrationFrom()
    return render(request, 'user/register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            messages.success(request, 'You have logged in successfully')
            return redirect(reverse(data))
    else:
        form = LoginForm()
    return render(request, 'user/login.html', {'form': form})

