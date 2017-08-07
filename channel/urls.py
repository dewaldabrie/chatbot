from django.conf.urls import include, url
from django.contrib import admin
from channel.views import *
from bot.views import channel_to_bot
urlpatterns = [
    # Examples:
    url(r'^$', user_to_channel, name='entry'),
    url(r'^user_to_channel', user_to_channel, name='user-to-channel'),
    url(r'^channel_to_bot', channel_to_bot, name='channel-to-bot'),
    url(r'^channel_to_user', channel_to_user, name='channel-to-user'),
    url(r'^bot_to_channel', bot_to_channel, name='bot-to-channel'),
    url(r'^done', done, name='done'),
]
