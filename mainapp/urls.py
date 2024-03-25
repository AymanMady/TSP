from django.urls import path
from . import views


urlpatterns = [
    path('',views.afficher_tout_posubilite,name="afficher_tout_posubilite"),
    # path('resultat/',views.resultat,name="resultat"),
    path('importation/',views.importation,name="importation"),
    path('home/',views.home,name="home"),
    path('approx/',views.affiche_algorithme_approximation,name="approx"),
    path('ant/',views.affiche_algorithme_ant,name="ant"),
    path('Données/',views.visialiserLeDonner,name="Données"),
    path('anim/',views.anim,name="anim"),

]