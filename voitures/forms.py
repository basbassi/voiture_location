from django import forms
from .models import Reservation

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['date_debut', 'date_fin']  # PAS 'montant_total'
from django import forms
from django.contrib.auth.models import User

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profil

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label='Prénom')
    last_name = forms.CharField(max_length=30, required=True, label='Nom')
    telephone = forms.CharField(max_length=15, required=True, label='Téléphone')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'telephone', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            Profil.objects.create(user=user, telephone=self.cleaned_data['telephone'])
        return user
from django import forms
from .models import Avis

class AvisForm(forms.ModelForm):
    class Meta:
        model = Avis
        fields = ['texte', 'note']
        widgets = {
            'texte': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Votre commentaire…'}),
            'note': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
        }
        labels = {
            'texte': 'Commentaire',
            'note': 'Note (1–5)',
        }
