import folium
import itertools
from django.shortcuts import render
import heapq
import sys
import math
import pandas as pd
import math
import plotly.offline as pyo
import plotly.graph_objs as go
import plotly.io as pio
import random


def approximation(villes):
    graph = {ville["Ville"]: {} for ville in villes}

    for i, ville1 in enumerate(villes):
        for j, ville2 in enumerate(villes):
            if i != j:
                distance = math.sqrt((ville1["Latitude"] - ville2["Latitude"]) ** 2 + (ville1["Longitude"] - ville2["Longitude"]) ** 2)
                graph[ville1["Ville"]][ville2["Ville"]] = distance

    start_ville = villes[0]["Ville"]
    visited = set([start_ville])
    path = [start_ville]
    current = start_ville

    while len(visited) < len(graph):
        nearest_neighbor = None
        min_distance = sys.maxsize

        for neighbor, weight in graph[current].items():
            if neighbor not in visited and weight < min_distance:
                nearest_neighbor = neighbor
                min_distance = weight

        if nearest_neighbor is not None:
            visited.add(nearest_neighbor)
            path.append(nearest_neighbor)
            current = nearest_neighbor
        else:
            break

    return [ville for ville in villes if ville["Ville"] in path]

def affiche_algorithme_approximation(request):
    fichier_excel = 'files/data.xlsx'
    
    try:
        columns_to_read = ['Ville', 'Latitude', 'Longitude']

        # Read the Excel file with specified columns
        df = pd.read_excel(fichier_excel, usecols=columns_to_read)
    except Exception as e:
        return render(request, "importation.html", {"message": "il faut importer un fichier excel"})  

    villes = df.to_dict('records')
    villes_ordonnees = approximation(villes)
    
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

def ant_colony_optimization(graph, num_ants=100, num_iterations=100, evaporation_rate=0.5, alpha=1, beta=2):
    num_cities = len(graph)
    pheromone = [[1] * num_cities for _ in range(num_cities)]
    best_path = None
    best_distance = float('inf')

    for _ in range(num_iterations):
        for ant in range(num_ants):
            current_vertex = random.choice(range(num_cities))
            visited = [current_vertex]
            path = [current_vertex]
            distance = 0

            while len(visited) < num_cities:
                unvisited_neighbors = [neighbor for neighbor in range(num_cities) if neighbor not in visited]
                probabilities = [((pheromone[current_vertex][neighbor]) ** alpha) * ((1 / graph[current_vertex][neighbor]) ** beta) for neighbor in unvisited_neighbors]
                total_probability = sum(probabilities)
                probabilities = [prob / total_probability for prob in probabilities]
                next_vertex = random.choices(unvisited_neighbors, weights=probabilities)[0]
                visited.append(next_vertex)
                path.append(next_vertex)
                distance += graph[current_vertex][next_vertex]
                current_vertex = next_vertex
            
            distance += graph[path[-1]][path[0]]  # Add distance from last city back to starting city

            if distance < best_distance:
                best_distance = distance
                best_path = path

            for i in range(num_cities - 1):
                pheromone[path[i]][path[i+1]] += 1 / distance
                pheromone[path[i+1]][path[i]] += 1 / distance
        
        # Evaporation
        for i in range(num_cities):
            for j in range(num_cities):
                pheromone[i][j] *= (1 - evaporation_rate)
    
    return best_path

def affiche_algorithme_ant(request):
    fichier_excel = 'files/data.xlsx'
    
    try:
        columns_to_read = ['Ville', 'Latitude', 'Longitude']

        # Read the Excel file with specified columns
        df = pd.read_excel(fichier_excel, usecols=columns_to_read)
    except Exception as e:
        return render(request, "importation.html", {"message": "il faut importer un fichier excel"})  

    villes = df.to_dict('records')
    
    # Créer un dictionnaire de distances entre les villes
    graph = {}
    for i, ville1 in enumerate(villes):
        graph[i] = {}
        for j, ville2 in enumerate(villes):
            if i != j:
                distance = math.sqrt((ville1["Latitude"] - ville2["Latitude"]) ** 2 + (ville1["Longitude"] - ville2["Longitude"]) ** 2)
                graph[i][j] = distance

    # Utiliser l'algorithme de colonies de fourmis pour l'approximation
    villes_ordonnees = ant_colony_optimization(graph)  
    
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
        folium.PolyLine(locations=[(villes[ville1]["Latitude"], villes[ville1]["Longitude"]), (villes[ville2]["Latitude"], villes[ville2]["Longitude"])], color='green').add_to(carte)
    
    folium.PolyLine(locations=[(villes[ville2]["Latitude"], villes[ville2]["Longitude"]), (villes[premiere_ville]["Latitude"], villes[premiere_ville]["Longitude"])], color='green').add_to(carte)

    derniere_ville = villes_ordonnees[-1]

    folium.Marker(
        location=[villes[derniere_ville]["Latitude"], villes[derniere_ville]["Longitude"]],
        popup=villes[derniere_ville]["Ville"],
        icon=folium.Icon(color="red", icon="info-sign")
    ).add_to(carte)

    folium.Marker(
        location=[villes[premiere_ville]["Latitude"], villes[premiere_ville]["Longitude"]],
        popup=villes[premiere_ville]["Ville"],
        icon=folium.Icon(color="green", icon="info-sign")
    ).add_to(carte)

    carte_html = carte._repr_html_()

    return render(request, "carte_villes.html", {"carte_html": carte_html})

    fichier_excel = 'files/data.xlsx'
    
    try:
        columns_to_read = ['Ville', 'Latitude', 'Longitude']

        # Read the Excel file with specified columns
        df = pd.read_excel(fichier_excel, usecols=columns_to_read)
    except Exception as e:
        return render(request, "importation.html", {"message": "il faut importer un fichier excel"})  

    villes = df.to_dict('records')
    
    # Utiliser l'algorithme de colonies de fourmis pour l'approximation
    villes_ordonnees = ant_colony_optimization(villes)  
    
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



def afficher_arbre(data):
    # Create nodes
    nodes = []
    for ville in data:
        nom = ville["Ville"]
        latitude = ville["Latitude"]
        longitude = ville["Longitude"]
        nodes.append(go.Scatter(
            x=[longitude],
            y=[latitude],
            mode='markers+text',
            marker=dict(size=10, color='blue'),
            text=nom,
            textposition="bottom center",
            name=nom
        ))
    
    # Create edges
    edges = []
    for ville1, ville2 in itertools.combinations(data, 2):
        nom1 = ville1["Ville"]
        nom2 = ville2["Ville"]
        latitude1, longitude1 = ville1["Latitude"], ville1["Longitude"]
        latitude2, longitude2 = ville2["Latitude"], ville2["Longitude"]
        edges.append(go.Scatter(
            x=[longitude1, longitude2],
            y=[latitude1, latitude2],
            mode='lines',
            line=dict(width=1, color='red'),
            hoverinfo='none'
        ))
    
    # Create layout with white background
    layout = go.Layout(
        title='Arbre des Villes',
        paper_bgcolor='white',
        plot_bgcolor='white',
        width=800,
        height=500
    )
    
    fig = go.Figure(data=nodes + edges, layout=layout)
    fig.update_layout(showlegend=False,margin=dict(t=40, r=0, l=0, b=0))
    
    
    # Convert the figure to HTML code
    html_code = pio.to_html(fig, full_html=False)
    
    return html_code




def afficher_tout_posubilite(request):
    fichier_excel = 'files/data.xlsx'
    try:
        columns_to_read = ['Ville', 'Latitude', 'Longitude']
        df = pd.read_excel(fichier_excel, usecols=columns_to_read)
    except Exception as e:
        return render(request, "importation.html", {"message": "il faut importer un fichier excel"})  # Gérer les erreurs de lecture du fichier

    villes = df.to_dict('records')
    arbre_html = afficher_arbre(villes)
    
    return render(request, "home.html", {"carte_html": arbre_html})
