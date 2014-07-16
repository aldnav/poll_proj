from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pollsite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^polls/', include('polls.urls', namespace='polls')),
    url(r'^polls2/', include('polls2.urls', namespace='polls2')),
    url(r'^admin/', include(admin.site.urls)),
)
