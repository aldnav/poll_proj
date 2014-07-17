from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.views import generic
from ipware.ip import get_ip

from polls.models import Poll, Choice, Voter

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_polls'

    def get_queryset(self):
        return Poll.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['trending_polls'] = Poll.objects.filter(answers__gte=5).order_by('-answers')[:10]
        return context

class DetailView(generic.DetailView):
    model = Poll
    template_name = 'polls/detail.html'

    # def get_object(self, *args, **kwargs):
        # return get_object_or_404(Poll, pk=self.kwargs['poll_id'])

    def get_queryset(self, *args, **kwargs):
        return Poll.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Poll
    template_name = 'polls/results.html'

    def get_object(self, *args, **kwargs):
        return get_object_or_404(Poll, pk=self.kwargs['poll_id'])

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
        poll.answers += 1
        poll.save()

        ip = get_ip(request)
        if ip:
            voter = Voter(ip=ip, choice_id=selected_choice.id, poll_id=poll.id)
            voter.save()

        return HttpResponseRedirect(reverse('polls:results', args=(poll.id,)))