from django.urls import path
from . import views

urlpatterns = [
    path('', views.redirect_to_login, name='root_redirect'), 
    path('index/', views.index, name='index'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('voiture/<int:id>/', views.voiture_detail, name='voiture_detail'),
    path('reserver/<int:id>/', views.reserver_voiture, name='reserver_voiture'),
    path('paiement/<int:id>/', views.paiement, name='paiement'),
    path('historique/', views.historique_reservations, name='historique'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('voitures/add/', views.ajouter_voiture, name='ajouter_voiture'),
    path('voitures/delete/<int:id>/', views.supprimer_voiture, name='supprimer_voiture'),
    path('reservation/<int:id>/modifier/', views.modifier_reservation, name='modifier_reservation'),
    path('reservation/<int:id>/supprimer/', views.supprimer_reservation, name='supprimer_reservation'),
]
