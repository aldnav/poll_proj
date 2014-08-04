from django.conf.urls import patterns, include, url

from polls import views

urlpatterns = patterns('',
	#/polls/
	url(r'^$', views.IndexView.as_view(), name='index'),
	#/polls/1
	url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
	#/polls/1/results
	url(r'^(?P<pk>\d+)/results/$', views.ResultsView.as_view(), name='results'),
	#/polls/1/vote
	url(r'^(?P<poll_id>\d+)/vote/$', views.vote, name='vote'),
	#ajax vote
	url(r'^(?P<poll_id>\d+)/ajaxvote/$', views.ajax_vote, name='voteajax'),
)