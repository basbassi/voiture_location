from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

from django.shortcuts import render
from .models import Voiture

from django.shortcuts import render, redirect
from .models import Voiture

from django.shortcuts import render, redirect
from .models import Voiture

from django.shortcuts import render, redirect
from .models import Voiture

def index(request):
    if not request.user.is_authenticated:
        return redirect('login')  # redirige vers la page login si pas connecté

    # Récupère toutes les marques disponibles
    marques_disponibles = Voiture.objects.filter(disponible=True).values_list('marque', flat=True).distinct()

    marque_selectionnee = request.GET.get('marque')
    voitures = Voiture.objects.filter(disponible=True)

    if marque_selectionnee:
        voitures = voitures.filter(marque=marque_selectionnee)

    return render(request, 'location/index.html', {
        'voitures': voitures,
        'marques': marques_disponibles,
        'marque_selectionnee': marque_selectionnee,
    })


def redirect_to_login(request):
    return redirect('login')
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib import messages

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Compte créé avec succès. Connectez-vous.")
            return redirect('login')  # ou autre URL
    else:
        form = CustomUserCreationForm()
    return render(request, 'location/signup.html', {'form': form})




def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  # ou autre page après connexion
        else:
            messages.error(request, "Identifiants incorrects")
    return render(request, 'location/login.html')

def logout_view(request):
    # log out logic here (ex: logout(request))
    return redirect('index')

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .models import Voiture, Avis
from .forms import AvisForm

@login_required
def voiture_detail(request, id):
    voiture = get_object_or_404(Voiture, pk=id)
    avis_list = Avis.objects.filter(voiture=voiture).order_by('-date')
    form = AvisForm()

    if request.method == 'POST':
        form = AvisForm(request.POST)
        if form.is_valid():
            nouvel_avis = form.save(commit=False)
            nouvel_avis.voiture = voiture
            nouvel_avis.client = request.user
            nouvel_avis.save()
            return redirect('voiture_detail', id=voiture.id)

    return render(request, 'location/voiture_detail.html', {
        'voiture': voiture,
        'avis_list': avis_list,
        'form': form,
    })



from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Voiture, Reservation
from decimal import Decimal

from django.contrib import messages

@login_required
def reserver_voiture(request, id):
    voiture = get_object_or_404(Voiture, pk=id)

    if request.method == 'POST':
        date_debut = request.POST.get('date_debut')
        date_fin = request.POST.get('date_fin')

        if date_debut and date_fin:
            d1 = timezone.datetime.strptime(date_debut, "%Y-%m-%d").date()
            d2 = timezone.datetime.strptime(date_fin, "%Y-%m-%d").date()
            jours = (d2 - d1).days

            if jours > 0:
                montant_total = Decimal(jours) * voiture.prix_par_jour

                Reservation.objects.create(
                    client=request.user,
                    voiture=voiture,
                    date_debut=d1,
                    date_fin=d2,
                    montant_total=montant_total
                )

                voiture.disponible = False
                voiture.save()

                messages.success(request, "Réservation enregistrée avec succès !")
                return redirect('historique')

            else:
                messages.error(request, "La date de fin doit être après la date de début.")

    return render(request, 'location/reservation.html', {'voiture': voiture})


def paiement(request, id):
    return render(request, 'location/paiement.html', {'id': id})

from django.contrib.auth.decorators import login_required
from .models import Reservation

@login_required
def historique_reservations(request):
    reservations = Reservation.objects.filter(client=request.user).order_by('-date_debut')
    return render(request, 'location/historique.html', {'reservations': reservations})


def admin_dashboard(request):
    return render(request, 'location/admin_dashboard.html')

def ajouter_voiture(request):
    return render(request, 'location/ajouter_voiture.html')

def supprimer_voiture(request, id):
    # logique de suppression ici
    return redirect('admin_dashboard')



from django.shortcuts import get_object_or_404, redirect, render
from .models import Reservation
from .forms import ReservationForm

def modifier_reservation(request, id):
    reservation = get_object_or_404(Reservation, id=id)

    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.montant_total = reservation.calculer_montant_total()
            reservation.save()
            return redirect('historique')  # assure-toi que ce nom existe bien dans urls.py
    else:
        form = ReservationForm(instance=reservation)

    return render(request, 'location/modifier_reservation.html', {'form': form})


# views.py

from django.shortcuts import get_object_or_404, redirect
from .models import Reservation, Voiture

def supprimer_reservation(request, id):
    reservation = get_object_or_404(Reservation, id=id)
    voiture = reservation.voiture  # Récupérer la voiture liée

    reservation.delete()

    # Vérifier s'il ne reste plus de réservation pour cette voiture
    reservations_restantes = Reservation.objects.filter(voiture=voiture).exists()
    if not reservations_restantes:
        voiture.disponible = True
        voiture.save()

    return redirect('historique')
