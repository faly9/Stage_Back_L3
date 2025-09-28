from django.urls import path
from .views import candidatures_mission , update_candidature

urlpatterns = [
    path("candidatures/", candidatures_mission, name="mes_candidatures"),
    path("candidatures/<int:pk>/", update_candidature, name="candidatureupdate"),
]
