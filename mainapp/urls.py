from django.urls import path
from . import views


urlpatterns = [
    path('',views.resultat,name="resultat"),
    path('importation/',views.importation,name="importation"),

]