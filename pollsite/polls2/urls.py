from django.conf.urls import patterns, url

from polls2 import views

urlpatterns = patterns('',
	# /polls2/
	url(r'^$', views.IndexView.as_view(), name='index'),
	# /polls2/first-question,1
	url(r'^(?P<poll_slug>[-\w]+),(?P<poll_id>\d+)/$', views.DetailView.as_view(), name='detail'),
	# /polls2/first-question,1/vote/
	url(r'^(?P<poll_slug>[-\w]+),(?P<poll_id>\d+)/vote/$', views.vote, name='vote'),
	# /polls2/first-question,1/results/
	url(r'^(?P<poll_slug>[-\w]+),(?P<poll_id>\d+)/results/$', views.ResultsView.as_view(), name='results'),
)