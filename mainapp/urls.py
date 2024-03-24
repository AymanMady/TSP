from django.urls import path
from . import views


urlpatterns = [
    path('',views.afficher_carte,name="afficher_carte"),

]