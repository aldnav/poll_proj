from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.views import generic
from ipware.ip import get_ip

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

class ResultsView(generic.DetailView):
    model = Poll
    template_name = 'polls2/results.html'

    def get_object(self, *args, **kwargs):
        return get_object_or_404(Poll, pk=self.kwargs['poll_id'])

def vote(request, poll_slug, poll_id):
	poll = get_object_or_404(Poll, pk=poll_id)
	try:
		selected_choice = poll.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		return render(request, 'polls/detail.html', {
			'poll': poll,
			'error_message': "You did not select a valid choice!"
		})
	else:
		selected_choice.votes += 1
		selected_choice.save()
		poll.answers += 1
		poll.save()
		ip = get_ip(request)
		if ip:
			voter = Voter(ip=ip, choice_id=selected_choice.id, poll_id=poll.id)
			voter.save()

		return HttpResponseRedirect(reverse('polls2:results', args=(poll.slug, poll.id)))