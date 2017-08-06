# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import urllib
import random
import string
import time
import datetime

from django.shortcuts import render, redirect
from django.http import HttpResponse

from bot.models import Questionaire, Question
def get_input(request):
    #check if user has made a response

    user_input = None
    if request.method == 'GET':
        user_input = request.GET
    elif request.method == 'POST':
        user_input = request.POST

    questions = []
    client_token = ''
    conversation_token = user_input['conversation_token']
    if user_input.get('response_to', False):
        questions = _lookup_questions(user_input['questionaire'])
        #generate client token
        timestamp = int(time.mktime(datetime.datetime.now().timetuple()))
        client_token = generate_random_string(15, timestamp)
    else:
        questions = _lookup_questions(
            user_input['questionaire'],
            user_input['response_to']  # this is the question id
        )
        client_token = user_input['client_token']
    # encode bot response for url
    params = urllib.urlencode(
        dict(
            verbiage='__and__'.join([q.question_text for q in questions]),
            question_tokens='__and__'.join([q.id for q in questions]),
            client_token=client_token,
            conversation_token=conversation_token,
        )
    )

    response = redirect('channel.talk_to_client')
    response['Location'] += '?{}'.format(params)

    return response

def _lookup_questions(questionaire_name, after=''):
    questions = []
    #first questions has blank "after" field
    questions += Question.objects.select_related('bot.question').filter(
        questionaire__name=questionaire_name,
        after=after
    )
    while questions[-1].wait_for_response == False:
        questions += Question.objects.select_related('bot.question').filter(
            questionaire__name=questionaire_name,
            after=questions[-1].id
        )
    return questions


def generate_random_string(size, seed=None):
    if seed != None:
         random.seed(seed)
    return(''.join(random.choice(string.ascii_letters) for i in range(size)))
