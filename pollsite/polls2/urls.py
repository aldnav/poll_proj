from django.conf.urls import patterns, url

from polls2 import views

urlpatterns = patterns('',
	# /polls2/
	url(r'^$', views.index, name='index'),
	# /polls2/first-question,1
	url(r'^(?P<poll_slug>[-\w]+),(?P<poll_id>\d+)/$', views.detail, name='detail'),
)