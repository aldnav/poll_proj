from django.conf.urls import patterns, url

from polls2 import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index')
)