from rest_framework.routers import DefaultRouter
from .views import EntrepriseViewSet

router = DefaultRouter()
router.register(r'entreprises', EntrepriseViewSet, basename='entreprise')

urlpatterns = router.urls
