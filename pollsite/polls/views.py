from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

from polls.models import Poll, Choice

# Create your views here.

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_polls'

    def get_queryset(self):
        '''
        Return five of the latest published polls excluding future publish posts
        '''
        return Poll.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Poll
    template_name = 'polls/detail.html'

    def get_object(self, *args, **kwargs):
        return get_object_or_404(Poll, pk=self.kwargs['poll_id'])


class ResultsView(generic.DetailView):
    model = Poll
    template_name = 'polls/results.html'

    def get_object(self, *args, **kwargs):
        return get_object_or_404(Poll, pk=self.kwargs['poll_id'])

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



# def index(request):
#     latest_polls = Poll.objects.order_by('-pub_date')[:5]
#     context = {
#         'latest_polls': latest_polls,
#     }
#     return render(request, 'polls/index.html', context)

# def detail(request, poll_slug, poll_id):
#     try:
#         poll = Poll.objects.get(pk=poll_id)
#     except Poll.DoesNotExist:
#         raise Http404
#     context = {
#         'poll': poll,
#     }
#     return render(request, 'polls/detail.html', context)

# def results(request, poll_slug, poll_id):
#     poll = get_object_or_404(Poll, pk=poll_id)
#     return render(request, 'polls/results.html', {'poll':poll})