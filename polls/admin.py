from django.contrib import admin

from .models import Answer, Choice, Poll, Question, Score


class PollAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'title', 'date_start', 'date_end', 'description', 'get_questions'
    )
    list_display_links = ('title',)


class ChoiceInline(admin.TabularInline):
    model = Choice
    min_num = 0
    extra = 0


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'poll', 'text', 'type', 'get_choices')
    inlines = [ChoiceInline]


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('pk', 'question', 'text', 'get_choices')


class ScoreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user_id', 'poll')


admin.site.register(Poll, PollAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Score, ScoreAdmin)
