import folium
import itertools
from django.shortcuts import render
import heapq
import sys
import math
import pandas as pd

def dijkstra(graph, start):
    distances = {vertex: sys.maxsize for vertex in graph}
    distances[start] = 0
    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)

        if current_distance > distances[current_vertex]:
            continue

        for neighbor, weight in graph[current_vertex].items():
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances
import math

def calculer_plus_court_chemin(villes):
    graph = {ville["Ville"]: {} for ville in villes}

    for i, ville1 in enumerate(villes):
        for j, ville2 in enumerate(villes):
            if i != j:
                distance = math.sqrt((ville1["Latitude"] - ville2["Latitude"]) ** 2 + (ville1["Longitude"] - ville2["Longitude"]) ** 2)
                graph[ville1["Ville"]][ville2["Ville"]] = distance

    start_ville = villes[0]["Ville"]

    distances = dijkstra(graph, start_ville)

    villes_triees = sorted(villes, key=lambda x: distances[x["Ville"]])

    return villes_triees



def afficher_carte(request):
    fichier_excel = 'files/data.xlsx'
    
    try:
        df = pd.read_excel(fichier_excel)
    except Exception as e:
        return render(request, "importation.html", {"message": "il faut importer un fichier excel"})  # Gérer les erreurs de lecture du fichier

    villes = df.to_dict('records')
    
    villes_ordonnees = calculer_plus_court_chemin(villes)
    
    carte = folium.Map(location=[villes[0]["Latitude"], villes[0]["Longitude"]], zoom_start=6)

    for ville in villes:
        nom = ville["Ville"]
        latitude = ville["Latitude"]
        longitude = ville["Longitude"]

        folium.Marker(
            location=[latitude, longitude],
            popup=nom,
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(carte)

    premiere_ville = villes_ordonnees[0]
    for i in range(len(villes_ordonnees) - 1):
        ville1 = villes_ordonnees[i]
        ville2 = villes_ordonnees[i + 1]
        folium.PolyLine(locations=[(ville1["Latitude"], ville1["Longitude"]), (ville2["Latitude"], ville2["Longitude"])], color='green').add_to(carte)
    
    folium.PolyLine(locations=[(ville2["Latitude"], ville2["Longitude"]), (premiere_ville["Latitude"], premiere_ville["Longitude"])], color='green').add_to(carte)

    derniere_ville = villes_ordonnees[-1]

    folium.Marker(
        location=[derniere_ville["Latitude"], derniere_ville["Longitude"]],
        popup=derniere_ville["Ville"],
        icon=folium.Icon(color="red", icon="info-sign")
    ).add_to(carte)

    folium.Marker(
        location=[premiere_ville["Latitude"], premiere_ville["Longitude"]],
        popup=premiere_ville["Ville"],
        icon=folium.Icon(color="green", icon="info-sign")
    ).add_to(carte)

    carte_html = carte._repr_html_()

    return render(request, "carte_villes.html", {"carte_html": carte_html})