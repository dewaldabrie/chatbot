from django.conf.urls import include, url
from django.contrib import admin
from channel.views import *

urlpatterns = [
    # Examples:
    url(r'^$', talk_to_bot, name='talk_to_bot'),
]
