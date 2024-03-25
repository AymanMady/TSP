from django.urls import path
from . import views


urlpatterns = [
    path('resultat/',views.resultat,name="resultat"),
    path('importation/',views.importation,name="importation"),
    path('',views.afficher_tout_posubilite,name="afficher_tout_posubilite"),
    path('home',views.home,name="home"),
    path('Données',views.visialiserLeDonner,name="Données"),
    path('afficher_tout_posubilite',views.afficher_tout_posubilite,name="afficher_tout_posubilite"),
    # path('afficher_page_arbre',views.afficher_page_arbre,name="afficher_page_arbre"),

]