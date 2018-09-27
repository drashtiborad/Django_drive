from django.contrib import messages
from django.contrib.auth import authenticate, login as initiate_login, logout as initiate_logout
from django.shortcuts import redirect, render, reverse
from django.contrib.auth.decorators import login_required

from django_drive.utils import hashed_pwd
from drive.views import data
from .forms import LoginForm, RegistrationFrom, UpdateAccountForm
from .models import User


def register(request):
    """
    Registers new users and renders template for registration form
    :param request: incoming request object
    :return: rendered template
    """
    if request.user.is_authenticated:
        return redirect(reverse(data, args=('home/',)))
    if request.method == "POST":
        form = RegistrationFrom(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            user = User(username=username, email=form.cleaned_data.get('email'),
                        date_of_birth=form.cleaned_data.get('date_of_birth'),
                        phone_number=form.cleaned_data.get('phone_number'),
                        password=hashed_pwd(form.cleaned_data.get('password')))
            user.save()
            messages.success(request, f'Account created for {username} successfully. You can now login !')
            return redirect('login')
    else:
        form = RegistrationFrom()
    return render(request, 'user/register.html', {'form': form})


def login(request):
    if request.user.is_authenticated:
        return redirect(reverse(data, args=('home/',)))
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user:
                initiate_login(request, user)
            messages.success(request, 'You have logged in successfully')
            return redirect(reverse(data, args=('home/',)))
    else:
        form = LoginForm()
    return render(request, 'user/login.html', {'form': form})


def logout(request):
    if request.user.is_authenticated:
        initiate_logout(request)
    return render(request, 'user/login.html', {'form': LoginForm()})


@login_required(login_url='login')
def account(request):
    if request.method == 'POST':
        form = UpdateAccountForm(request.POST, request.FILES)
        if form.is_valid():
            user = User.objects.get(id=request.user.id)
            user.username=form.cleaned_data.get('username')
            user.date_of_birth=form.cleaned_data.get('date_of_birth')
            user.phone_number=form.cleaned_data.get('phone_number')
            user.profile_picture=request.FILES.get('profile_picture')
            user.save()
            messages.success(request, 'Your account info has been updated ')
            return redirect(reverse('account'))
        else:
            user_data = {'username': request.user.username, 'email': request.user.email,
                         'date_of_birth': request.user.date_of_birth,
                         'phone_number': request.user.phone_number}
            form = UpdateAccountForm(initial=user_data)
            messages.warning(request, 'Please enter valid data for edited fields')
            return render(request, 'user/account.html', {'form': form, 'user': request.user})
    elif request.method == 'GET':
        user = User.objects.filter(id=request.user.id)[0]
        user_data = {'username': user.username, 'email': user.email, 'date_of_birth': user.date_of_birth,
                     'phone_number': user.phone_number}
        form = UpdateAccountForm(initial=user_data)
        return render(request, 'user/account.html', {'form': form, 'user': request.user,
                                                     "image_file": user.profile_picture})
