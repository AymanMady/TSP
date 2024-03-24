from django.urls import path
from . import views


urlpatterns = [
    path('resultat/',views.resultat,name="resultat"),
    path('importation/',views.importation,name="importation"),
    path('',views.afficher_carte,name="afficher_carte"),
    path('home',views.home,name="home"),
    path('visialiserLeDonner',views.visialiserLeDonner,name="visialiserLeDonner"),

]