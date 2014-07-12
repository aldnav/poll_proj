from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.views import generic
from ipware.ip import get_ip

from polls.models import Poll, Choice, Voter

# Create your views here.

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_polls'

    def get_queryset(self):
        '''
        Return five of the latest published polls excluding future publish posts
        '''
        return Poll.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
        # return Poll.objects.all()

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['trending_polls'] = Poll.objects.order_by('-answers')[:10]
        return context


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
            'poll': poll,
            'error_message': "You did not select a valid choice!"
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        poll.answers += 1
        poll.save()
        # get the ip address of the voter
        ip = get_ip(request)
        if ip:
            voter = Voter(ip=ip, choice_id=selected_choice.id, poll_id=poll.id)
            voter.save()

        return HttpResponseRedirect(reverse('polls:results', args=(poll.slug, poll.id)))

def ask(request):
    if request.POST:
        question = request.POST['question']
        try:
            poll = Poll.objects.get(question=question)
            # return with error Poll already exist
        except Poll.DoesNotExist:
            poll = Poll(question=question, pub_date=timezone.now())
            poll.save()
    args = {}
    args.update(csrf(request))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'),'/')

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