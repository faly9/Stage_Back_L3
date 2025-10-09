from django.urls import path
from .views import candidatures_mission , update_candidature , get_notifications_for_freelance, get_notifications_for_entreprise

urlpatterns = [
    path("candidatures/", candidatures_mission, name="mes_candidatures"),
    path("candidatures/<int:pk>/", update_candidature, name="candidatureupdate"),
    path("note/" , get_notifications_for_freelance , name="notifications" ),
    path("notee/" , get_notifications_for_entreprise , name="notifications-entreprise" ),
]
