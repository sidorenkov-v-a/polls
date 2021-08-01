from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .serializers import (
    PollSerializer, QuestionSerializer, PollNoStartDateSerializer, ScoreSerializer, AnswerSerializer
)
from .models import Poll, Question, Score, Answer
from .permissions import IsAdmin
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def hello(request):
    return Response({"message": "Hello, world!"})


class PollViewSet(ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = (IsAdmin,)
    ordering = ['-date_start']

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return PollNoStartDateSerializer
        return self.serializer_class


class QuestionViewSet(ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (IsAdmin,)
    ordering = ['poll']

    @swagger_auto_schema(responses={200: 'Types of question'})
    @action(detail=False, methods=['get'])
    def types(self, request):
        return Response(Question.TYPES)


class ScoreViewSet(ModelViewSet):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer
    permission_classes = [AllowAny]
    filterset_fields = ['user_id']
    http_method_names = ['get', 'post']


class AnswerViewSet(ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [AllowAny]