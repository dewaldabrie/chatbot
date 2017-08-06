# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import Questionaire, Question, Answer


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_created')
    list_filter = ('questionaire',)


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 5


class QuestionaireAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_created')
    inlines = (QuestionInline, )


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'date_answered')
    list_filter = ('question__questionaire', 'question')


admin.site.register(Questionaire, QuestionaireAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)

