# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.db import models


class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=255)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField()
    phone_number = models.BigIntegerField()
    profile_picture = models.ImageField(default=os.path.join(os.getenv('HOME'), 'Drive_files', 'profile_pictures',
                                                             'default-profile-img.png'))
    password = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user'


class File(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    child_path = models.CharField(max_length=255)
    parent_path = models.CharField(default=os.path.join(os.getenv('HOME'), 'Drive_files', 'files'), max_length=2048)
    original_path = models.CharField(default=os.path.join(os.getenv('HOME'), 'Drive_files', 'files'), max_length=2048)
    file_type = models.CharField(max_length=30)
    filename = models.CharField(max_length=1024)
    size = models.BigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField()

    class Meta:
        db_table = 'file'
