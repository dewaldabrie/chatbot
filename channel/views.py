# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import urllib
import time
import datetime
from copy import deepcopy
from django.shortcuts import render, redirect, reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
import bot.views
from chatserver.settings import BOT_PARAMS
from channel.models import Conversation, Verbiage
from bot.views import generate_random_string
from bot.models import Answer

def user_to_channel(request):
    user_input = {}
    if request.method == 'GET':
        user_input = request.GET
    elif request.method == 'POST':
        user_input = request.POST

    #get response from bot
    # create converstaion if this is first interaction
    conversation_token = ''
    params = None
    if 'response_to' not in user_input:
        now = datetime.datetime.now()
        timestamp = int(time.mktime(now.timetuple()))
        conversation_token = generate_random_string(15, timestamp)
        request.session['conversation_token'] = conversation_token
        request.session.update(BOT_PARAMS)
        request.session['first_interaction'] = True
        c = Conversation.objects.create(
            name=conversation_token,
            datetime_start=now,
            bot="bot"
        )
        c.save()
        request.session.modified = True
    else:
        # log any input from user
        assert (user_input['client_message'])
        assert (user_input['conversation_token'])
        assert (user_input['response_to'])  # this is the question id
        assert (user_input['client_token']) # this if generated in the answer field for the first question
        request.session.update(unlistify(user_input))
        timestamp = datetime.datetime.utcnow()
        c = Conversation.objects.get(name=user_input['conversation_token'])
        v = Verbiage.objects.create(
            conversation=c,
            timestamp=timestamp,
            text=user_input['client_message'],
            agent='user'
        )
        v.save()
        request.session.modified = True

    response = redirect('channel-to-bot')
    return response

def unlistify(d):
    d2 = dict()
    for k in d.keys():
        d2[k] = d[k]
    return d2


def bot_to_channel(request):

    #log input from bot
    timestamp = datetime.datetime.utcnow()
    c = Conversation.objects.get(name=request.session['conversation_token'])
    for text in request.session['verbiage']:
        v = Verbiage.objects.create(
            conversation=c,
            timestamp=timestamp,
            text=text,
            agent='bot'
        )
        v.save()

    return redirect('channel-to-user')


def channel_to_user(request):
    #also pass chat history/log to client view
    messages = []
    if 'conversation_token' in request.session:
        c = Conversation.objects.get(name=request.session.get('conversation_token'))
        messages = Verbiage.objects.filter(conversation=c)
    # render to client template
    return render_to_response(
        'channel/chat.html',
        {
            'messages': messages,
            'latest_bot_message_id': request.session.get('latest_question_token',None),
            'client_token': request.session.get('client_token',None),
            'conversation_token': request.session.get('conversation_token', None),
            'done': request.session.get('done', False),
        },
    )

def done(request):
    #also pass chat history/log to client view
    answers = Answer.objects.filter(
        client_token=request.session.get('client_token','')
    )
    ans_dict = dict((str(a.question.name), a.answer_text) for a in answers)
    # render to done template
    return render_to_response(
        'channel/done.html',
        ans_dict
    )

