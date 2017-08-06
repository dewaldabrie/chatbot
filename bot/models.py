# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
import datetime


class Questionaire(models.Model):
    # name of questionaire
    name = models.CharField(max_length=700, null=False, blank=False, unique=True)
    # description of questionaire
    description = models.CharField(max_length=700, null=False, blank=False)
    # Keep track of when this was created
    date_created = models.DateTimeField(default=datetime.datetime.now, null=False, blank=False)


    def __repr__(self):
        return self.name

class Question(models.Model):
    # Short name to identify question
    name = models.CharField(max_length=100, null=False, blank=False)
    # Questionaire parent
    questionaire = models.ForeignKey(Questionaire, null=False, blank=False)
    # order in questionare, linked-list type of referencing
    after = models.OneToOneField('self', null=True, blank=True)
    # question text
    question_text = models.CharField(max_length=700, null=False, blank=False)
    # Keep track of when this was created
    date_created = models.DateTimeField(default=datetime.datetime.now, null=False, blank=False)
    # Should the bot wait for a response?
    wait_for_response = models.BooleanField(default=False, null=False, blank=False)

    def __repr__(self):
        return '::'.join([self.questionaire.name, self])

    # class Meta:
    #     ordering = ('name', 'after')


class Answer(models.Model):
    FIELD_TYPE_CHOICES = (
        ('text', 'Text'),
        ('boolean', 'Boolean'),
        ('radio', 'Radio Box'),
        ('checkbox', 'Checkbox'),
        ('select', 'Drop-down list'),
    )

    # corresponding question
    question = models.ForeignKey(Question, null=False, blank=False)
    # corresponding user TODO: add user functionality if required
    # user = models.ForeignKey(User, null=False, blank=False)
    client_token = models.CharField(max_length=700, null=True, blank=True)
    # answer validation regex
    answer_validation_regex = models.CharField(max_length=700, null=True, blank=True)
    # Field type for answer (in case of select , radio, or checkbox)
    answer_field_type = models.CharField(max_length=200, null=False, blank=False, choices=FIELD_TYPE_CHOICES)
    # Field contents for answer
    answer_text = models.CharField(max_length=700, null=False, blank=False)
    # Keep track of when this was answered
    date_answered = models.DateTimeField(default=datetime.datetime.now, null=False, blank=False)

    def __repr__(self):
        return '::'.join([self.question.questionaire.name, self.question.name, 'answer'])


