import datetime
from django.db import models
from django.utils import timezone
from django.template.defaultfilters import slugify

class Poll(models.Model):
    slug = models.SlugField()
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date_published')
    answers = models.IntegerField(default=0)

    def __unicode__(self):
        return self.question

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    def get_number_of_answers(self):
        return len(Choice.objects.filter(poll_id=self.id))

    def get_number_of_days_past(self):
        delta = str(timezone.now() - self.pub_date).split(':')
        passed = 0
        if delta:
            passed = delta[0].split(',')[0]
        return passed

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.question)
        super(Poll, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('polls:detail', (self.slug, self.id))

class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __unicode__(self):
        return self. choice_text

class Voter(models.Model):
    ip = models.CharField(max_length=200)
    poll = models.ForeignKey(Poll)
    choice = models.ForeignKey(Choice)

    def __unicode__(self):
        return self.ip