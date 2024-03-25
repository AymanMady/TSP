import folium
from folium.plugins import AntPath
import pandas as pd
import math
import heapq
import sys
from django.shortcuts import render


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
        columns_to_read = ['Ville', 'Latitude', 'Longitude']

        # Read the Excel file with specified columns
        df = pd.read_excel(fichier_excel, usecols=columns_to_read)
    except Exception as e:
        return render(request, "importation.html", {"message": "il faut importer un fichier excel"})  # Gérer les erreurs de lecture du fichier

    villes = df.to_dict('records')
    
    villes_ordonnees = calculer_plus_court_chemin(villes)
    
    # create a map object
    carte = folium.Map(location=[villes[0]["Latitude"], villes[0]["Longitude"]], zoom_start=6)

    # Add markers for cities
    for ville in villes:
        folium.Marker(
            location=[ville["Latitude"], ville["Longitude"]],
            popup=ville["Ville"],
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(carte)

    # Create animated lines
    for i in range(len(villes_ordonnees)):
        ville1 = villes_ordonnees[i]
        ville2 = villes_ordonnees[(i + 1) % len(villes_ordonnees)]  # Circularly iterate through the cities

        AntPath([(ville1["Latitude"], ville1["Longitude"]), (ville2["Latitude"], ville2["Longitude"])],
                delay=400,  # Delay between animation frames in milliseconds
                dash_array=[30, 15],  # Dash pattern [dash, gap] in pixels
                color="green",  # Line color
                weight=3  # Line weight in pixels
                ).add_to(carte)

    # Generate HTML representation of the map
    carte_html = carte.repr_html()

    return render(request, "carte_villes.html", {"carte_html": carte_html})