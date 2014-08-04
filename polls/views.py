from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.views import generic
import time
import json

from polls.models import Poll, Choice

class IndexView(generic.ListView):
	template_name = 'polls/index.html'
	context_object_name = 'latest_polls'

	def get_queryset(self):
		return Poll.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
	model = Poll
	template_name = 'polls/detail.html'

	def get_queryset(self, *args, **kwargs):
		return Poll.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
	model = Poll
	template_name = 'polls/results.html'

class JSONResponseMixin(object):
	def render_to_response(self, context):
		return self.get_json_response(self.convert_context_to_json(context))

	def get_json_response(self, content, **httpresponse_kwargs):
		return HttpResponse(content,
							content_type='application/json',
							**httpresponse_kwargs)

	def convert_context_to_json(self, context):
		return json.dumps(context)

def vote(request, poll_id):
	poll = get_object_or_404(Poll, pk=poll_id)
	try:
		selected_choice = poll.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		return render(request, 'polls/detail.html', {
			'poll': poll,
			'error_message': 'Please select a valid choice!'
		})
	else:
		selected_choice.votes += 1
		selected_choice.save()

		return HttpResponseRedirect(reverse('polls:results', args=(poll.id, )))

def ajax_vote(request, poll_id):
	poll = get_object_or_404(Poll, pk=poll_id)
	try:
		selected_choice = poll.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		return render(request, 'polls/detail.html', {
			'poll': poll,
			'error_message': 'Please select a valid choice!'
		})
	else:
		selected_choice.votes += 1
		selected_choice.save()

		return HttpResponseRedirect(poll.get_absolute_url())