from django.contrib import admin

from polls2.models import Poll, Choice, Voter

class ChoiceInline(admin.TabularInline):
	model = Choice
	extra = 3

class PollAdmin(admin.ModelAdmin):
	fieldsets = [
		(None,			{'fields': ['question', 'answers']}),
		('Date info', 	{'fields': ['pub_date']}),
	]
	inlines = [ChoiceInline]
	list_display = ('question', 'pub_date', 'was_published_recently', 'answers')
	list_filter = ['pub_date']
	search_fields = ['question', 'pub_date']

class VoterAdmin(admin.ModelAdmin):
	fieldsets = [
		(None,			{'fields':['ip','choice', 'poll']}),		
	]
	list_display = ('ip', 'choice', 'poll')

admin.site.register(Poll, PollAdmin)
admin.site.register(Voter, VoterAdmin)