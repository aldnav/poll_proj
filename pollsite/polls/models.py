import datetime
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.db import models

class Poll(models.Model):
    slug = models.SlugField(null=True, blank=True)
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date_published')
    flags = models.IntegerField(default=0)
    answers = models.IntegerField(default=0)    # this is count for answers, not answers themselves

    def __unicode__(self):
        return self.question

    def was_published_recently(self):
        now = timezone.now()
        # print now, self.pub_date
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    def was_flagged(self):
        return self.flags > 0

    was_flagged.admin_order_field = 'flags'
    was_flagged.boolean = False
    was_flagged.short_description = 'Was flagged?'

    def get_number_of_answers(self):
        return len(Choice.objects.filter(poll_id=self.id))

    def get_number_of_days_past(self):
        delta = str(timezone.now() - self.pub_date).split(':')
        passed = None
        if delta:
            passed = delta[0].split(',')[0]
        return passed

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.question)
        super(Poll, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('polls:detail', (self.slug,self.id))

class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __unicode__(self):
        return self.choice_text

class Voter(models.Model):
    ip = models.CharField(max_length=200)
    poll = models.ForeignKey(Poll)
    choice = models.ForeignKey(Choice)

    def __unicode__(self):
        return self.ip