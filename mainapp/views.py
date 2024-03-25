from django.shortcuts import render,redirect
import networkx as nx
from geopy.distance import geodesic
from .importation import *
import os
from django.core.files.storage import default_storage
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .algo import *
from .sidimed import *
# from django.shortcuts import session
from .graphAvecAnim import *
def home(request):
    return redirect(afficher_tout_posubilite)


   

