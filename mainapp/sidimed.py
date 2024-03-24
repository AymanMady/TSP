import folium
import itertools
from django.shortcuts import render
import heapq
import sys
import math

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
    graph = {ville["nom"]: {} for ville in villes}

    for i, ville1 in enumerate(villes):
        for j, ville2 in enumerate(villes):
            if i != j:
                distance = math.sqrt((ville1["latitude"] - ville2["latitude"]) ** 2 + (ville1["longitude"] - ville2["longitude"]) ** 2)
                graph[ville1["nom"]][ville2["nom"]] = distance

    # Choisissez une ville de départ arbitraire
    start_ville = villes[0]["nom"]

    # Utiliser l'algorithme de Dijkstra pour trouver le plus court chemin
    distances = dijkstra(graph, start_ville)

    # Trier les villes par leur distance par rapport à la ville de départ
    villes_triees = sorted(villes, key=lambda x: distances[x["nom"]])

    # Retourner la liste des villes triées par leur distance par rapport à la ville de départ
    return villes_triees

def afficher_carte(request):
    villes = [
        {"nom": "Aleg", "latitude": 17.1728009990846, "longitude": -13.9023810848904},
        {"nom": "Nouadhibou", "latitude": 21.0200766331283, "longitude": -15.9151199295992},
        {"nom": "Aioun", "latitude": 16.8366893287323, "longitude": -9.27583480330441},
        {"nom": "Akjoujt", "latitude": 19.9420143167071, "longitude": -14.6440193516613},
        {"nom": "Atar", "latitude": 20.6190971368345, "longitude": -13.4188043441809},
        {"nom": "Nouakchott", "latitude": 18.0783994226296, "longitude": -15.885155269477},
        {"nom": "Sélibaby", "latitude": 15.4729996284158, "longitude": -12.1965786387684},
        {"nom": "Tidjikja", "latitude": 18.6315729894793, "longitude": -11.5524434053275},
        {"nom": "Zoueratt", "latitude": 23.4958870003132, "longitude": -10.1376367144798},
        {"nom": "Kaédi", "latitude": 16.0455219912174, "longitude": -13.1873050779235},
        {"nom": "Kiffa", "latitude": 16.678771880566, "longitude": -11.4111923888962},
        {"nom": "Néma", "latitude": 16.3926143684381, "longitude": -7.34328812930029},
        {"nom": "Rosso", "latitude": 16.6264755333439, "longitude": -15.6941505288147}
    ]

    villes_ordonnees = calculer_plus_court_chemin(villes)

    carte = folium.Map(location=[villes[0]["latitude"], villes[0]["longitude"]], zoom_start=6)

    for ville in villes:
        nom = ville["nom"]
        latitude = ville["latitude"]
        longitude = ville["longitude"]

        # Ajouter un marqueur avec le nom de la ville
        folium.Marker(
            location=[latitude, longitude],
            popup=nom,
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(carte)
        
    

    # Ajouter les lignes reliant chaque paire de villes dans l'ordre du plus court chemin
    premiere_ville=villes_ordonnees[0]
    for i in range(len(villes_ordonnees) - 1):
        
        ville1 = villes_ordonnees[i]
        ville2 = villes_ordonnees[i + 1]
        folium.PolyLine(locations=[(ville1["latitude"], ville1["longitude"]), (ville2["latitude"], ville2["longitude"])], color='green').add_to(carte)
    
    folium.PolyLine(locations=[(ville2["latitude"], ville2["longitude"]), (premiere_ville["latitude"], premiere_ville["longitude"])], color='green').add_to(carte)

    derniere_ville = villes_ordonnees[-1]

    # Ajouter un marqueur rouge pour la dernière ville
    folium.Marker(
        location=[derniere_ville["latitude"], derniere_ville["longitude"]],
        popup=derniere_ville["nom"],
        icon=folium.Icon(color="red", icon="info-sign")
    ).add_to(carte)
    
    
    folium.Marker(
        location=[premiere_ville["latitude"], premiere_ville["longitude"]],
        popup=premiere_ville["nom"],
        icon=folium.Icon(color="green", icon="info-sign")
    ).add_to(carte)
    
    # Convertir la carte Folium en HTML
    carte_html = carte._repr_html_()
    request.session['file'] = 'my_value'

    # Save session data explicitly (optional)
    request.session.save()

    # Access session data
    my_value = request.session.get('file')
    try :
        path='files/data.xlsx'
    except:
        request.session['file']='test'


    return render(request, "carte_villes.html", {"carte_html": carte_html})
