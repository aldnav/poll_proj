from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from polls.models import Poll, Choice

# Create your views here.
def index(request):
    latest_polls = Poll.objects.order_by('-pub_date')[:5]
    context = {
        'latest_polls': latest_polls,
    }
    return render(request, 'polls/index.html', context)

def detail(request, poll_slug, poll_id):
    try:
        poll = Poll.objects.get(pk=poll_id)
    except Poll.DoesNotExist:
        raise Http404
    context = {
        'poll': poll,
    }
    return render(request, 'polls/detail.html', context)

def results(request, poll_slug, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    return render(request, 'polls/results.html', {'poll':poll})

def vote(request, poll_slug, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    try:
        selected_choice = poll.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'poll': p,
            'error_message': "You did not select a valid choice!"
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()

        return HttpResponseRedirect(reverse('polls:results', args=(poll.slug, poll.id)))