# entreprise/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EntrepriseViewSet , get_my_entreprise 

router = DefaultRouter()
router.register(r'entreprises', EntrepriseViewSet, basename='entreprise')

urlpatterns = [
    path('', include(router.urls)),
    path('id/', get_my_entreprise , name='id-entreprise'),
]
