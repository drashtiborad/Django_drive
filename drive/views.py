# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render


def data(request):
    return render(request, 'drive/data.html')
