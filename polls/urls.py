from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import PollViewSet, QuestionViewSet, ScoreViewSet

router = DefaultRouter()
router.register('poll', PollViewSet, basename='poll')
router.register('question', QuestionViewSet, basename='question')
router.register('score', ScoreViewSet, basename='score')

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]
