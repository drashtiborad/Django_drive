# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, reverse
# from user.views import login


def data(request):
    if request.user.is_authenticated:
        return render(request, 'drive/data.html')
    return redirect(reverse('login'))
