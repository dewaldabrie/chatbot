from django.conf.urls import include, url
from django.contrib import admin
from bot.views import engage

urlpatterns = [
    # Examples:
    url(r'^$', engage, name='engage'),
]
