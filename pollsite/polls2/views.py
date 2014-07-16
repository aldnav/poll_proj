from django.http import Http404
from django.utils import timezone
from django.shortcuts import render
from polls2.models import Poll, Choice, Voter

def index(request):	
	context = {}
	context['latest_poll_list'] = Poll.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
	return render(request, 'polls2/index.html', context)

def detail(request, poll_slug, poll_id):
	try:
		poll = Poll.objects.get(pk=poll_id)
	except Poll.DoesNotExist:
		raise Http404
	context = {
		'poll': poll,
	}
	return render(request, 'polls2/detail.html', context)