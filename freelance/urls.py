from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FreelanceViewSet

router = DefaultRouter()
router.register(r'freelances', FreelanceViewSet, basename='freelance')

urlpatterns = [
    path('', include(router.urls)),
]
