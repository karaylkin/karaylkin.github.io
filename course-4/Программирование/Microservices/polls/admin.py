from django.contrib import admin
from .models import Poll, Choice, Vote


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ['question', 'pub_date', 'total_votes']
    list_filter = ['pub_date']
    search_fields = ['question']
    date_hierarchy = 'pub_date'


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['choice_text', 'poll', 'vote_count']
    list_filter = ['poll']
    search_fields = ['choice_text']


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['choice', 'voted_at']
    list_filter = ['voted_at', 'choice__poll']
    date_hierarchy = 'voted_at'

