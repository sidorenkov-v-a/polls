from django.db import models
from django.utils.translation import ugettext_lazy as _


class Poll(models.Model):
    title = models.CharField(max_length=100, verbose_name=_('Poll title'))
    date_start = models.DateField(verbose_name=_('Date start'))
    date_end = models.DateField(verbose_name=_('Date end'))
    description = models.TextField(verbose_name=_('Description'))

    def __str__(self):
        return self.title

    def get_questions(self):
        return ', '.join([str(p) for p in self.questions.all()])

    get_questions.short_description = _('Questions')


class Choice(models.Model):
    question = models.ForeignKey(
        'Question',
        on_delete=models.CASCADE,
        related_name='choices',
        verbose_name=_('Question choice')
    )
    text = models.CharField(max_length=256,
                            verbose_name=_('Choice text'))

    def __str__(self):
        return self.text


class Question(models.Model):
    TEXT_ANSWER = 1
    ONE_CHOICE_ANSWER = 2
    MULTI_CHOICE_ANSWER = 3

    TYPES = [
        (TEXT_ANSWER, 'Available text answer'),
        (ONE_CHOICE_ANSWER, 'Available only one choice'),
        (MULTI_CHOICE_ANSWER, 'Available multiple choice')
    ]

    poll = models.ForeignKey(
        Poll,
        on_delete=models.CASCADE,
        related_name='questions',
        verbose_name='Poll'
    )
    text = models.TextField(verbose_name=_('Question text'))
    type = models.IntegerField(
        choices=TYPES,
        verbose_name=_('Type of answer')
    )

    def __str__(self):
        return self.text

    def get_choices(self):
        return ', '.join([str(p) for p in self.choices.all()])

    get_choices.short_description = _('Choices')


class Answer(models.Model):
    question = models.ForeignKey(
        'Question',
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name=_('Question'),
    )
    score = models.ForeignKey(
        'Score',
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name='Question',
    )
    text = models.TextField(verbose_name='Answer text', null=True, blank=True)
    choices = models.ManyToManyField(
        Choice,
        related_name='answers',
        blank=True
    )

    def get_choices(self):
        return ', '.join([str(p) for p in self.choices.all()])

    get_choices.short_description = _('Choices')


class Score(models.Model):
    user_id = models.PositiveIntegerField()
    poll = models.ForeignKey(
        Poll,
        on_delete=models.CASCADE,
        related_name='results',
        verbose_name='Poll'
    )
