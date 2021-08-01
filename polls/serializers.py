from rest_framework.serializers import ModelSerializer, ValidationError
from rest_framework import serializers
from .models import Poll, Question, Choice, Answer, Score


class ChoiceSerializer(ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'text']


class QuestionSerializer(ModelSerializer):
    choices = ChoiceSerializer(many=True, required=False)

    class Meta:
        model = Question
        fields = ['id', 'poll', 'text', 'type', 'choices']

    def create(self, validated_data):
        choices = validated_data.pop('choices', [])
        question = Question.objects.create(**validated_data)
        for data in choices:
            Choice.objects.create(question=question, **data)
        return question

    def update(self, instance, validated_data):
        choices = validated_data.pop('choices', [])
        instance.choices.all().delete()
        for data in choices:
            Choice.objects.create(question=instance, **data)
        return super().update(instance, validated_data)

    def validate(self, attrs):
        type = attrs['type']
        choices = attrs.get('choices', [])
        if type == Question.TEXT_ANSWER and choices:
            raise ValidationError(
                {'choices': f'Not allowed for this question type: {type}'}
            )
        if type == Question.ONE_CHOICE_ANSWER:
            if len(choices) < 1:
                raise ValidationError(
                    {'choices': ('Should be at least 1 choice for this'
                                 f' question type: {type}')}
                )
        if type == Question.MULTI_CHOICE_ANSWER:
            if len(choices) < 2:
                raise ValidationError(
                    {'choices': ('Should be at least 2 choices for this'
                                 f' question type: {type}')}
                )

        return super().validate(attrs)


class PollSerializer(ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Poll
        fields = '__all__'

    def validate(self, attrs):
        date_start = attrs.get('date_start', None)
        date_end = attrs.get('date_end', None)

        if not date_start and self.instance:
            date_start = self.instance.date_start

        if date_start and date_end:
            if date_start > date_end:
                raise ValidationError(
                    {'error': 'Date start should be less than date end'}
                )
        return attrs


class PollNoStartDateSerializer(PollSerializer):
    class Meta:
        model = Poll
        exclude = ['date_start']


class AnswerSerializer(ModelSerializer):
    choices_id = serializers.PrimaryKeyRelatedField(
        queryset=Choice.objects.all(),
        many=True, write_only=True, required=False
    )
    choices = serializers.SlugRelatedField(
        slug_field='text', many=True, read_only=True
    )

    question_id = serializers.PrimaryKeyRelatedField(
        queryset=Question.objects.all(), write_only=True
    )
    question = serializers.SlugRelatedField(slug_field='text', read_only=True)

    class Meta:
        model = Answer
        fields = '__all__'
        read_only_fields = ['score']

    def _validate_type(self, attrs):
        def required_detail(value, type):
            return {value: f'Required for this question type: {type}'}

        def not_allowed_detail(value, type):
            return {value: f'Not allowed for this question type: {type}'}

        question = attrs['question_id']
        type = question.type
        choices = attrs.get('choices_id', [])
        text = attrs.get('text', None)
        if type == Question.TEXT_ANSWER:
            if choices:
                raise ValidationError(not_allowed_detail('choices_id', type))
            if not text:
                raise ValidationError(required_detail('text', type))

        if (type == Question.ONE_CHOICE_ANSWER or
                type == Question.MULTI_CHOICE_ANSWER):
            if text:
                raise ValidationError(not_allowed_detail('text', type))
            if not choices:
                raise ValidationError(required_detail('choices_id', type))

        if type == Question.ONE_CHOICE_ANSWER and len(choices) > 1:
            raise ValidationError(
                {'choices_id':
                     f'Only one choice allowed for this question type: {type}'
                 }
            )

    def _validate_choices(self, attrs):
        question = attrs['question_id']
        set_choices = {_.pk for _ in attrs.get('choices_id', [])}
        set_question_choices = {_.pk for _ in question.choices.all()}
        if not set_choices.issubset(set_question_choices):
            raise ValidationError(
                {'Choices':
                     ('IDs should be in question choices range: '
                      f'{list(set_question_choices)}')
                 }
            )

    def validate(self, attrs):
        self._validate_choices(attrs)
        self._validate_type(attrs)
        return attrs


class ScoreSerializer(ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Score
        fields = '__all__'

    def validate(self, attrs):
        poll = attrs['poll']
        questions = poll.questions.all()
        answers = attrs['answers']
        for answer in answers:
            if answer['question_id'] not in questions:
                raise ValidationError(
                    {'question_id': 'Wrong question id for this poll'}
                )
        return attrs

    def create(self, validated_data):
        answers = validated_data.pop('answers', [])
        score = Score.objects.create(**validated_data)
        for data in answers:
            choices = data.pop('choices_id', [])
            question = data.pop('question_id')
            answer = Answer.objects.create(score=score, question=question,
                                           **data)
            answer.choices.set(choices)
        return score
