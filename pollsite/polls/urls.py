from django.conf.urls import patterns, url

from polls import views

urlpatterns = patterns('',
	# /polls/
	url(r'^$', views.index, name='index'),
	# /polls/1
	url(r'^(?P<poll_slug>[-\w]+),(?P<poll_id>\d+)/$', views.detail, name='detail'),
	# /polls/a-question,1/results/
	url(r'^(?P<poll_slug>[-\w]+),(?P<poll_id>\d+)/results/$', views.results, name='results'),
	# /polls/a-question,1/vote/
	url(r'^(?P<poll_slug>[-\w]+),(?P<poll_id>\d+)/vote/$', views.vote, name='vote'),
)