from django.contrib import messages
from django.contrib.auth import authenticate, login as initiate_login, logout as initiate_logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import redirect, render, reverse

from django_drive.settings import EMAIL_HOST_USER
from django_drive.utils import hashed_pwd
from drive.views import data
from .forms import ChangePassword, LoginForm, RegistrationFrom, ResetPassword, UpdateAccountForm
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
    """
    Logs in users by authenticating with email and password
    :param request: incoming request object
    :return: rendered template
    """
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
    """
    Logs out user and destroys current session and cookies
    :param request: incoming request object
    :return: rendered template
    """
    if request.user.is_authenticated:
        initiate_logout(request)
    return redirect(reverse('login'))


# @login_required(login_url='login')
def account(request):
    """
    For user details display and modification
    :param request: incoming request object
    :return: rendered template
    """
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = UpdateAccountForm(request.POST, request.FILES)
            if form.is_valid():
                user = User.objects.get(id=request.user.id)
                user.username = form.cleaned_data.get('username')
                user.date_of_birth = form.cleaned_data.get('date_of_birth')
                user.phone_number = form.cleaned_data.get('phone_number')
                user.profile_picture = request.FILES.get('profile_picture')
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
    else:
        return redirect(reverse('login'))


def reset_password(request):
    """
    Provides functionality to reset password
    :param request: incoming request object
    :return: rendered template
    """
    if request.method == 'GET':
        form = ResetPassword()
        return render(request, 'user/reset_password.html', {'form': form})
    elif request.method == 'POST':
        form = ResetPassword(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user = User.objects.get(email=email)
            token = user.generate_token()
            link = request.build_absolute_uri(reverse('change_password', args=(token,)))
            send_mail("Password Reset Request", f"Click here to reset your email { link }"
                      , EMAIL_HOST_USER, [email])
            messages.success(request, "Reset email has been sent to the email")
            return redirect(reverse('login'))


def change_password(request, token):
    """
    Changes user password by validating incoming request
    :param request: incoming request object
    :param token: reset password token generated by reset_password request
    :return: rendered template
    """
    if request.user.is_anonymous:
        """
        When user forgets password
        """
        user = User.verify_reset_token(token)
        if user:
            form = ChangePassword(request.POST)
            user_id = User.objects.get(id=user.id)
            if form.is_valid():
                user_id.password = hashed_pwd(form.cleaned_data.get('password'))
                user_id.save()
                return redirect(reverse('login'))
            else:
                form = ChangePassword()
                return render(request, 'user/change_password.html', {'form': form})
        else:
            messages.warning(request, 'The link is expired or invalid, please try again')
            return redirect(reverse('reset_password'))
    else:
        """
        For logged in users
        """
        import pdb;pdb.set_trace()
        if request.method == "GET":
            form = ChangePassword()
            return render(request, 'user/change_password.html', {'form': form})
        elif request.method == "POST":
            form = ChangePassword(request.POST)
            if form.is_valid():
                user = User.objects.get(id=request.user.id)
                user.password = hashed_pwd(form.cleaned_data.get('password'))
                user.save()
                messages.success(request, "Your password has been successfully changed!")
                initiate_logout(request)
                initiate_login(request, user)
                return redirect(reverse('account'))
            else:
                messages.warning(request, "Both password must match!")
                return redirect(reverse('change_password', args=("-",)))
