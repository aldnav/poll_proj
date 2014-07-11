import datetime
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.db import models

class Poll(models.Model):
    slug = models.SlugField(null=True, blank=True)
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date_published')
    flags = models.IntegerField(default=0)

    def __unicode__(self):
        return self.question

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    def was_flagged(self):
        return self.flags > 0

    was_flagged.admin_order_field = 'flags'
    was_flagged.boolean = False
    was_flagged.short_description = 'Was flagged?'

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
    choice = models.ForeignKey(Choice)

    def __unicode__(self):
        return self.ip