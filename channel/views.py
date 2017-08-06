# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import urllib
import time
import datetime
from django.shortcuts import render, redirect
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
    if not user_input:
        now = datetime.datetime.now()
        timestamp = int(time.mktime(now.timetuple()))
        conversation_token = generate_random_string(15, timestamp)
        params = urllib.urlencode(BOT_PARAMS)
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
        timestamp = datetime.date.utcnow()
        c = Conversation.objects.get(name=user_input['conversation_token'])
        v = Verbiage.objects.create(
            converstation=c,
            timestamp=timestamp,
            text=user_input['text'],
            agent='user'
        )
        v.save()


        # encode message for url
        params = urllib.urlencode(user_input)

    response = redirect('bot.views.get_input')
    response['Location'] += '?{}'.format(params)
    return response


def talk_to_client(request):
    bot_input = {}
    if request.method == 'GET':
        bot_input = request.GET
    elif request.method == 'POST':
        bot_input = request.POST

    #log input from bot
    timestamp = datetime.date.utcnow()
    c = Conversation.objects.get(name=bot_input['conversation_token'])
    for text in bot_input['text'].split('__and__'):
        v = Verbiage.objects.create(
            converstation=c,
            timestamp=timestamp,
            text=text,
            agent='bot'
        )

    # render to client template
    return render_to_response(
        'channel/chat.html',
        {
            'messages': bot_input['text'].split('__and__'),
            'message_tokens': bot_input['question_tokens'].split('__and__'),
            'client_token': bot_input['client_token'],
            'conversation_token': bot_input['conversation_token'],
        },
    )



