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

from bot.models import Questionaire, Question, Answer
import channel.views

def channel_to_bot(request):
    #check if user has made a response

    questions = []
    client_token = request.session.get('client_token', '')
    conversation_token = request.session.get('conversation_token')
    latest_question_token = request.session.get('response_to', None)
    if request.session.get('first_interaction', False) == True:
        request.session['first_interaction'] = False
        assert('questionaire' in request.session)
        # lookup new question(s)
        questions = _lookup_questions_from_start(request.session['questionaire'])
        # generate client token
        timestamp = int(time.mktime(datetime.datetime.now().timetuple()))
        client_token = generate_random_string(15, timestamp)
    elif latest_question_token:
        # save answers to prev question
        question = Question.objects.get(id=latest_question_token)
        answer = Answer(
            question=question,
            client_token=client_token,
            answer_text=request.session.get('client_message', '')
        )
        answer.save()

        # lookup new question(s)
        questions = _lookup_questions_from_id(
            request.session['questionaire'],
            int(latest_question_token)  # this is the question id
        )
    # package bot answer
    bot_answer = {}
    done = False
    if questions:
        latest_question_token = questions[-1].id
    else:
        done = True
    bot_answer = dict(
        verbiage=[q.question_text for q in questions],
        latest_question_token=latest_question_token,
        client_token=client_token,
        conversation_token=conversation_token,
        done=done,
    )
    request.session.update(bot_answer)
    request.session.modified = True
    return redirect('bot-to-channel')


def _lookup_questions_from_start(questionaire_name):
    questions = []
    #first questions has blank "after" field
    questions += Question.objects.select_related('question').filter(
        questionaire__name=questionaire_name,
        after__isnull=True
    )
    if questions:
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
    if questions:
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
