from django.contrib import admin
from .models import Voiture, Reservation, Paiement, Avis

@admin.register(Voiture)
class VoitureAdmin(admin.ModelAdmin):
    list_display = ('marque', 'modele', 'categorie', 'prix_par_jour', 'disponible')
    search_fields = ('marque', 'modele')
    list_filter = ('categorie', 'disponible')

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('client', 'voiture', 'date_debut', 'date_fin', 'montant_total', 'statut')
    search_fields = ('client__username', 'voiture__marque')
    list_filter = ('statut',)

@admin.register(Paiement)
class PaiementAdmin(admin.ModelAdmin):
    list_display = ('reservation', 'date_paiement', 'montant', 'mode_paiement')
    search_fields = ('reservation__client__username',)

@admin.register(Avis)
class AvisAdmin(admin.ModelAdmin):
    list_display = ('client', 'voiture', 'note', 'date')
    search_fields = ('client__username', 'voiture__marque')
    list_filter = ('note',)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profil

# Inline model (affiche le Profil dans la page d’un utilisateur)
class ProfilInline(admin.StackedInline):
    model = Profil
    can_delete = False
    verbose_name_plural = 'Profil'

# Extension du UserAdmin
class CustomUserAdmin(UserAdmin):
    inlines = (ProfilInline, )

# Supprimer l'ancien UserAdmin et enregistrer le nouveau
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

from django.contrib import admin
from .models import Profil

@admin.register(Profil)
class ProfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'telephone')
    search_fields = ('user__username', 'telephone')
