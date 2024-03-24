from django.urls import path
from . import views


urlpatterns = [
    path('resultat/',views.resultat,name="resultat"),
    path('importation/',views.importation,name="importation"),
    path('',views.afficher_carte,name="afficher_carte"),
    path('index/',views.index,name="index"),
]