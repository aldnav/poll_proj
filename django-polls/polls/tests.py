import datetime

from django.core.urlresolvers import reverse
from django.utils import timezone
from django.test import TestCase

from polls.models import Poll

class PollMethodTests(TestCase):

    def test_was_published_recently_with_future_poll(self):
        """
        the method was_published_recently() is expected to return False for polls whose
        pub_date is in the future / future
        """
        future_poll = Poll(pub_date=timezone.now() + datetime.timedelta(days=30))
        self.assertEqual(future_poll.was_published_recently(), False)

    def test_was_published_recently_with_old_poll(self):
        """
        was_published_recently() should return False for older polls / past
        """
        old_poll = Poll(pub_date=timezone.now() - datetime.timedelta(days=30))
        self.assertEqual(old_poll.was_published_recently(), False)

    def test_was_published_recently_with_recent_poll(self):
        """
        was_published_recently() should return True for polls whose pub_date is within the last day / recent
        """
        recent_poll = Poll(pub_date=timezone.now() - datetime.timedelta(hours=1))
        self.assertEqual(recent_poll.was_published_recently(), True)

def create_poll(question, days):
    return Poll.objects.create(question=question, pub_date=timezone.now() + datetime.timedelta(days=days))

class PollViewTests(TestCase):

    def test_index_view_with_no_polls(self):
        """
        If no polls exist, an appropriate message should be displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_polls'], [])

    def test_index_view_with_a_past_poll(self):
        """
        Past polls should be displayed on the index page.
        """
        create_poll(question="I am a past poll.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_polls'],
            ['<Poll: I am a past poll.>']
        )

    def test_index_view_with_a_future_poll(self):
        """
        Future polls should not be posted.
        """
        create_poll(question="Future polll.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.", status_code=200)
        self.assertQuerysetEqual(response.context['latest_polls'], [])

    def test_index_view_with_future_poll_and_past_poll(self):
        """
        With past and future polls in db, only past polls are displayed.
        """
        create_poll(question="Past poll 1.", days=-30)
        create_poll(question="Past poll 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_polls'],
            ['<Poll: Past poll 2.>', '<Poll: Past poll 1.>']
        )

class PollIndexDetailTests(TestCase):
    def test_detail_view_with_a_future_poll(self):
        """
        The future poll's detail view should return a 404 as status code
        """
        future_poll = create_poll(question="Future poll.", days=5)
        response = self.client.get(reverse('polls:detail', args=(future_poll.id,)))
        self.assertEqual(response.status_code, 404)

    def test_detail_view_with_a_past_poll(self):
        """
        The past poll's detail view should return 200 as status code
        """
        past_poll = create_poll(question='Past Poll.', days=-5)
        response = self.client.get(reverse('polls:detail', args=(past_poll.id,)))
        self.assertContains(response, past_poll.question, status_code=200)