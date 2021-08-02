from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Poll, Question, Score
from .permissions import IsAdmin
from .serializers import (PollNoStartDateSerializer, PollSerializer,
                          QuestionSerializer, ScoreSerializer)


class PollViewSet(ModelViewSet):
    queryset = Poll.objects.all().order_by('date_start')
    serializer_class = PollSerializer
    permission_classes_by_action = {'list': [AllowAny], 'default': [IsAdmin]}

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return PollNoStartDateSerializer
        return self.serializer_class


class QuestionViewSet(ModelViewSet):
    queryset = Question.objects.all().order_by('poll')
    serializer_class = QuestionSerializer
    permission_classes = [IsAdmin]

    @swagger_auto_schema(responses={200: 'Types of question'})
    @action(detail=False, methods=['get'])
    def types(self, request):
        return Response(Question.TYPES)


class ScoreViewSet(ModelViewSet):
    queryset = Score.objects.all().order_by('poll')
    serializer_class = ScoreSerializer
    permission_classes = [AllowAny]
    filterset_fields = ['user_id']
    http_method_names = ['get', 'post', 'delete']
    permission_classes_by_action = {'delete': [IsAdmin], 'default': [AllowAny]}
