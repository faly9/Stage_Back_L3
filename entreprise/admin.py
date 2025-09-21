from django.utils.html import format_html
from django.contrib import admin
from .models import Entreprise
from django.utils.html import format_html  # si tu veux afficher les images

@admin.register(Entreprise)
class EntrepriseAdmin(admin.ModelAdmin):
    list_display = ('id_entreprise', 'nom', 'secteur', 'user', 'profile_thumbnail')
    list_filter = ('secteur',)
    search_fields = ('nom', 'secteur', 'user__email')
    ordering = ('nom',)

    def profile_thumbnail(self, obj):
        if obj.profile_image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius:50%;" />', obj.profile_image.url)
        return "-"
    profile_thumbnail.short_description = 'Image Profil'
