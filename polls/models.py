import datetime
from django.utils import timezone
from django.db import models

class Poll(models.Model):
	question = models.CharField(max_length=200)
	pub_date = models.DateTimeField('date_published')
	likes = models.IntegerField(default=0)

	def __unicode__(self):
		return self.question

	def was_published_recently(self):
		now = timezone.now()
		return now - datetime.timedelta(days=1) <= self.pub_date <= now

	was_published_recently.admin_order_field = 'pub_date'
	was_published_recently.boolean = True
	was_published_recently.short_description = 'Published recently?'

	def get_number_of_days_past(self):
		delta = str(timezone.now() - self.pub_date).split(':')
		passed = 0
		if delta:
			passed = delta[0].split(',')[0]
		return passed