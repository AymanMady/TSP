from django.shortcuts import render,redirect
import networkx as nx
from geopy.distance import geodesic
from .importation import *
import os
from django.core.files.storage import default_storage
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .algo import *


def home(request):
    return redirect(afficher_carte)

def resultat(request):
    coords = {
        "Aleg": (17.1728009990846, -13.9023810848904),
        "Nouadhibou": (21.0200766331283, -15.9151199295992),
        "Aioun": (16.8366893287323, -9.27583480330441),
        "Akjoujt": (19.9420143167071, -14.6440193516613),
        "Atar": (20.6190971368345, -13.4188043441809),
        "Nouakchott": (18.0783994226296, -15.885155269477),
        "Sélibaby": (15.4729996284158, -12.1965786387684),
        "Tidjikja": (18.6315729894793, -11.5524434053275),
        "Zoueratt": (23.4958870003132, -10.1376367144798),
        "Kaédi": (16.0455219912174, -13.1873050779235),
        "Kiffa": (16.678771880566, -11.4111923888962),
        "Néma": (16.3926143684381, -7.34328812930029),
        "Rosso": (16.6264755333439, -15.6941505288147),
    }
    def nearest_neighbor_tsp(coords):
        G = nx.Graph()

        for city in coords:
            G.add_node(city)

        for city1 in coords:
            for city2 in coords:
                if city1 != city2:
                    distance = geodesic(coords[city1], coords[city2]).km
                    G.add_edge(city1, city2, weight=distance)

        path = ["Tidjikja"] 
        current_city = "Tidjikja"

        while len(path) < len(coords):
            nearest_city = None
            min_distance = float('inf')
            for neighbor in G.neighbors(current_city):
                distance = G[current_city][neighbor]['weight']
                if distance < min_distance and neighbor not in path:
                    min_distance = distance
                    nearest_city = neighbor
            path.append(nearest_city)
            current_city = nearest_city

        path.append("Tidjikja")

        return path
    result = nearest_neighbor_tsp(coords)
    return render(request,"index.html",{'result':result})
from .sidimed import *
