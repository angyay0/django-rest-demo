# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import datetime

'''
    Following models are used in the app just for demonstrate
    Django endpoints and functionality of a simple api for a blog
    used for web and mobile environments
'''
class UserStatus(models.Model):
    title = models.TextField(max_length=20, blank=True)
    created_date = models.DateTimeField(default=datetime.datetime.today, blank=False, editable=False)

class UserModel(models.Model):
    name = models.CharField(max_length=20, blank=False)
    last_name = models.CharField(max_length=30, blank=False)
    email = models.EmailField(blank=False,unique=True)
    password = models.TextField(blank=False)
    status = models.ForeignKey(UserStatus, on_delete=models.SET_NULL, null=True)
    created_date = models.DateTimeField(default=datetime.datetime.today, blank=False, editable=False)
    updated_date = models.DateTimeField(default=datetime.datetime.today, blank=False)
    created_by = models.CharField(max_length=10, blank=False, editable=False)
    updated_by = models.CharField(max_length=10, blank=False)

class Entry(models.Model):
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=False)
    entry = models.TextField(blank=False)
    created_date = models.DateTimeField(default=datetime.datetime.today, blank=False, editable=False)
    updated_date = models.DateTimeField(default=datetime.datetime.today, blank=False)

class Comment(models.Model):
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    author = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True)
    comment = models.CharField(max_length=100, blank=False)
    created_date = models.DateTimeField(default=datetime.datetime.today, blank=False, editable=False)

'''
    Following models are just helpers
'''
class Access(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    device = models.PositiveIntegerField(blank=False)
    description = models.CharField(max_length=50,blank=True)
    created_date = models.DateTimeField(default=datetime.datetime.today, blank=False, editable=False)

'''
class Token(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.PROTECT)
    active = models.BooleanField(default=True, blank=False)
    push_token = models.CharField(max_length=250, blank=False)
    session_token = models.CharField(max_length=250, blank=False)
    created_date = models.DateTimeField(default=datetime.datetime.today, blank=False, editable=False)
    updated_date = models.DateTimeField(default=datetime.datetime.today, blank=False)
'''
