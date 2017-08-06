from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'chatserver.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^bot', include('bot.urls')),
    url(r'^', include('channel.urls')),
    url(r'^admin/', include(admin.site.urls)),
]
