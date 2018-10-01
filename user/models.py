# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from django_drive.settings import SECRET_KEY
from django_drive.utils import hashed_pwd


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=255)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField()
    phone_number = models.BigIntegerField()
    profile_picture = models.ImageField(default='default.jpeg', upload_to='profile_pics')
    password = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'
    # password = 'password'

    objects = UserManager()

    class Meta:
        db_table = 'user'

    def check_password(self, raw_password):
        return self.password == hashed_pwd(raw_password)

    def generate_token(self, expires_sec=900):
        serializer = Serializer(SECRET_KEY, expires_sec)
        return serializer.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        serializer = Serializer(SECRET_KEY)
        try:
            user_id = serializer.loads(token)['user_id']
        except:
            return
        return User.objects.get(id=user_id)


class File(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    child_path = models.CharField(max_length=255)
    parent_path = models.CharField(default=os.path.join(os.getenv('HOME'), 'data/djando_drive'), max_length=2048)
    original_path = models.CharField(default=os.path.join(os.getenv('HOME'), 'data/djando_drive'), max_length=2048)
    file_type = models.CharField(max_length=30)
    filename = models.FileField(max_length=1024, upload_to='django_drive/')
    size = models.BigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)

    class Meta:
        db_table = 'file'
