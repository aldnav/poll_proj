from django.conf.urls import patterns, include, url

from polls import views

urlpatterns = patterns('',
    #/polls/
    url(r'^$', views.IndexView.as_view(), name='index'),
    #/polls/1
    url(r'^(?P<poll_id>\d+)/$', views.DetailView.as_view(), name='detail'),
)