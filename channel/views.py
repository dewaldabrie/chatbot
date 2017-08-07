# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import urllib
import time
import datetime
from django.shortcuts import render, redirect, reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
import bot.views
from chatserver.settings import BOT_PARAMS
from channel.models import Conversation, Verbiage
from bot.views import generate_random_string

def talk_to_bot(request):
    user_input = {}
    if request.method == 'GET':
        user_input = request.GET
    elif request.method == 'POST':
        user_input = request.POST

    #get response from bot
    # create converstaion if this is first interaction
    conversation_token = ''
    params = None
    if request.session.get('conversation_token') != '':
        now = datetime.datetime.now()
        timestamp = int(time.mktime(now.timetuple()))
        conversation_token = generate_random_string(15, timestamp)
        request.session['conversation_token'] = conversation_token
        request.session.update(BOT_PARAMS)
        c = Conversation.objects.create(
            name=conversation_token,
            datetime_start=now,
            bot="bot"
        )
        c.save()
    else:
        # log any input from user
        assert (user_input['text'])
        assert (user_input['converstation_token'])
        assert (user_input['response_to'])  # this is the question id
        assert (user_input['client_token']) # this if generated in the answer field for the first question
        request.session.update(user_input)
        timestamp = datetime.date.utcnow()
        c = Conversation.objects.get(name=user_input['conversation_token'])
        v = Verbiage.objects.create(
            converstation=c,
            timestamp=timestamp,
            text=user_input['text'],
            agent='user'
        )
        v.save()

    response = redirect('/get-bot-input')
    return response


def talk_to_client(request):
    request.session = {}

    #log input from bot
    timestamp = datetime.date.utcnow()
    c = Conversation.objects.get(name=request.session['conversation_token'])
    for text in request.session['verbiage']:
        v = Verbiage.objects.create(
            converstation=c,
            timestamp=timestamp,
            text=text,
            agent='bot'
        )
        v.save()

    #also pass chat history/log to client view
    messages = Verbiage.objects.filter(conversation=c).order('timestamp')
    # render to client template
    return render_to_response(
        'channel/chat.html',
        {
            'messages': messages,
            'latest_bot_message_id': request.session['latest_question_token'],
            'client_token': request.session['client_token'],
            'conversation_token': request.session['conversation_token'],
        },
    )



