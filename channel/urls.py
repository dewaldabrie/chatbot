from django.conf.urls import include, url
from django.contrib import admin
from channel.views import *
from bot.views import get_input
urlpatterns = [
    # Examples:
    url(r'^$', talk_to_bot, name='user_to_channel'),
    url(r'^get-bot-input', get_input, name='channel_to_bot'),
    url(r'^give-user-input', talk_to_client, name='bot_to_channel'),
]
