# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import urllib
import random
import string
import time
import datetime
import hashlib

from django.shortcuts import render, redirect
from django.http import HttpResponse

from bot.models import Questionaire, Question

def get_input(request):
    #check if user has made a response

    questions = []
    client_token = ''
    conversation_token = request.session['conversation_token']
    if request.session.get('response_to') != '':
        assert('questionaire' in request.session)
        questions = _lookup_questions_from_start(request.session['questionaire'])
        #generate client token
        timestamp = int(time.mktime(datetime.datetime.now().timetuple()))
        client_token = generate_random_string(15, timestamp)
    else:
        questions = _lookup_questions_from_id(
            request.session['questionaire'],
            int(request.session['response_to'])  # this is the question id
        )
        client_token = request.session['client_token']
    # encode bot response for url
    bot_answer = dict(
            verbiage=[q.question_text for q in questions],
            latest_question_token=questions[-1].id,
            client_token=client_token,
            conversation_token=conversation_token,
        )
    request.session.update(bot_answer)

    response = redirect('give-user-input')
    return response


def _lookup_questions_from_start(questionaire_name):
    questions = []
    #first questions has blank "after" field
    questions += Question.objects.select_related('question').filter(
        questionaire__name=questionaire_name,
        after__isnull=True
    )
    while questions[-1].wait_for_response == False:
        questions += Question.objects.select_related('question').filter(
            questionaire__name=questionaire_name,
            after=questions[-1].id
        )
    return questions

def _lookup_questions_from_id(questionaire_name, previous_id):
    questions = []
    #first questions has blank "after" field
    questions += Question.objects.select_related('question').filter(
        questionaire__name=questionaire_name,
        after=previous_id
    )
    while questions[-1].wait_for_response == False:
        questions += Question.objects.select_related('question').filter(
            questionaire__name=questionaire_name,
            after=questions[-1].id
        )
    return questions


def generate_random_string(size, seed=None):
    if seed != None:
         random.seed(seed)
    return(''.join(random.choice(string.ascii_letters) for i in range(size)))
