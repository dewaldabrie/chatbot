# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import datetime

class Conversation(models.Model):
    """
    The converstation is initiated and terminated by the client (browser)
    """
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.CharField(max_length=700, null=False, blank=False)
    datetime_start = models.DateTimeField(default=datetime.datetime.now, null=False, blank=False)
    datetime_end = models.DateTimeField(default=datetime.datetime.now, null=True, blank=True)
    client_token= models.CharField(max_length=100, null=True, blank=True)
    bot = models.CharField(max_length=100, null=False, blank=False)

class Verbiage(models.Model):
    """
    A record of the exchanges made between the two entities
    """
    conversation = models.ForeignKey(Conversation, null=False, blank=False)
    timestamp = models.DateTimeField(default=datetime.datetime.now, null=False, blank=False)
    text = models.CharField(max_length=100, null=False, blank=False)
    agent = models.CharField(max_length=100, null=False, blank=False)
