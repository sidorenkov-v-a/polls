from django.urls import path, include
from .views import hello
from rest_framework.routers import DefaultRouter
from .views import PollViewSet, QuestionViewSet, ScoreViewSet, AnswerViewSet

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register('poll', PollViewSet, basename='poll')
router.register('question', QuestionViewSet, basename='question')
router.register('score', ScoreViewSet, basename='score')
router.register('answer', AnswerViewSet, basename='answer')


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]

urlpatterns += [
    path('hello/', hello, name='hello')
]
