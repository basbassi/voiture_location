from django.db import models
from django.contrib.auth.models import User

class Voiture(models.Model):
    marque = models.CharField(max_length=100)
    modele = models.CharField(max_length=100)
    categorie = models.CharField(max_length=50)
    prix_par_jour = models.DecimalField(max_digits=8, decimal_places=2)
    disponible = models.BooleanField(default=True)
    image = models.ImageField(upload_to='voitures/')
    localisation = models.TextField(blank=True, null=True)  # <-- Nouveau champ

    def __str__(self):
        return f"{self.marque} {self.modele}"


from datetime import timedelta

class Reservation(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    voiture = models.ForeignKey(Voiture, on_delete=models.CASCADE)
    date_debut = models.DateField()
    date_fin = models.DateField()
    montant_total = models.DecimalField(max_digits=10, decimal_places=2)
    statut = models.CharField(max_length=20, default='En attente')

    def calculer_montant_total(self):
        nb_jours = (self.date_fin - self.date_debut).days + 1
        return nb_jours * self.voiture.prix_par_jour


class Paiement(models.Model):
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE)
    date_paiement = models.DateTimeField(auto_now_add=True)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    mode_paiement = models.CharField(max_length=50)

class Avis(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    voiture = models.ForeignKey(Voiture, on_delete=models.CASCADE)
    texte = models.TextField()
    note = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)


from django.contrib.auth.models import User
from django.db import models

class Profil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telephone = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.user.username} - {self.telephone}"