from django.contrib import admin
from polls.models import Poll, Choice, Voter

# Register your models here.
class ChoiceInline(admin.TabularInline):
	model = Choice
	extra = 3

class PollAdmin(admin.ModelAdmin):
	fieldsets = [
		(None,			{'fields': ['question','flags','answers']}),
		('Date info', 	{'fields': ['pub_date']}),
	]
	inlines = [ChoiceInline]
	list_display = ('question', 'pub_date', 'was_published_recently', 'was_flagged', 'answers')
	list_filter = ['pub_date']
	search_fields = ['question', 'pub_date']

class VoterAdmin(admin.ModelAdmin):
	fieldsets = [
		(None,			{'fields':['ip','choice', 'poll']}),		
	]
	list_display = ('ip', 'choice', 'poll')

admin.site.register(Poll, PollAdmin)
admin.site.register(Voter, VoterAdmin)