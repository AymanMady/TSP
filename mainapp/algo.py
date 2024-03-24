import openpyxl
import re
import networkx as nx
from geopy.distance import geodesic
import numpy as np
from django.shortcuts import render


try :
    file_path = 'files/data.xlsx'
except:
    file_path = ''

# Function to convert the excel file to a dictionary
def excel_to_dict(file_path):
    # Load the workbook and select the first worksheet
    
    wb = openpyxl.load_workbook(file_path)
    ws = wb.active

    # Initialize an empty dictionary
    city_coords = {}

    # Start from row 2 to skip headers
    for row in ws.iter_rows(min_row=2):
        # Each row has cells: city, latitude, longitude
        city = row[0].value
        lat = row[1].value
        lon = row[2].value

        # Some cleaning for the city name might be necessary if there are any issues
        city = re.sub(r"[^a-zA-Z ]+", "", city) if city else city

        # Add to dictionary
        city_coords[city] = (lat, lon)

    return city_coords



# Convert the Excel file to a dictionary
coords = excel_to_dict(file_path)
print(coords)
def visialiserLeDonner(request):
    coords = excel_to_dict(file_path)
    return render(request,'selectdata.html',{'data':coords})


# Définition des fonctions

def initialize_pheromone_matrix(graph, initial_pheromone):
    pheromone_matrix = {}
    for edge in graph.edges():
        pheromone_matrix[edge] = initial_pheromone
    return pheromone_matrix

def choose_next_city(pheromone_matrix, graph, current_city, unvisited_cities, alpha, beta):
    probabilities = []
    pheromone = np.array([pheromone_matrix[(current_city, city)] if (current_city, city) in pheromone_matrix 
                          else pheromone_matrix[(city, current_city)] for city in unvisited_cities])
    visibility = 1 / np.array([graph[current_city][city]['weight'] for city in unvisited_cities])
    probabilities = (pheromone ** alpha) * (visibility ** beta)
    probabilities /= probabilities.sum()
    next_city = np.random.choice(unvisited_cities, p=probabilities)
    return next_city

def update_pheromone_matrix(pheromone_matrix, ants_paths, decay_rate):
    for edge in pheromone_matrix:
        pheromone_matrix[edge] *= (1 - decay_rate)  # Évaporation des phéromones
    for path, distance in ants_paths:
        for i in range(len(path) - 1):
            edge = (path[i], path[i + 1])
            reverse_edge = (path[i + 1], path[i])  # Arête dans la direction inverse
            if edge in pheromone_matrix:
                pheromone_matrix[edge] += 1.0 / distance
            elif reverse_edge in pheromone_matrix:
                pheromone_matrix[reverse_edge] += 1.0 / distance
            else:
                raise KeyError(f"Edge {edge} not found in the pheromone matrix.")

def ant_colony_tsp(graph, num_ants, num_iterations, initial_pheromone, pheromone_evaporation_rate, alpha, beta, start_city):
    pheromone_matrix = initialize_pheromone_matrix(graph, initial_pheromone)
    best_path = None
    best_distance = float('inf')
    for _ in range(num_iterations):
        ants_paths = []
        for _ in range(num_ants):
            path = [start_city]
            unvisited_cities = list(set(graph.nodes()) - set([start_city]))
            while unvisited_cities:
                next_city = choose_next_city(pheromone_matrix, graph, path[-1], unvisited_cities, alpha, beta)
                path.append(next_city)
                unvisited_cities.remove(next_city)
            path.append(start_city)  # Revenir à la ville de départ
            distance = sum([graph[path[i]][path[i + 1]]['weight'] for i in range(len(path) - 1)])
            ants_paths.append((path, distance))
            if distance < best_distance:
                best_path = path
                best_distance = distance
        update_pheromone_matrix(pheromone_matrix, ants_paths, pheromone_evaporation_rate)
    return best_path, best_distance

# Données d'exemple


G = nx.Graph()
for city in coords:
    G.add_node(city)
for city1 in coords:
    for city2 in coords:
        if city1 != city2:
            distance = geodesic(coords[city1], coords[city2]).km
            G.add_edge(city1, city2, weight=distance)

# Paramètres de l'ACO
num_ants = 10
num_iterations = 100
initial_pheromone = 1.0 / G.size(weight='weight')
pheromone_evaporation_rate = 0.1
alpha = 1  # Influence de la phéromone
beta = 1   # Influence de la visibilité (l'inverse de la distance)

# Choix de la ville de départ
start_city = "Nouakchott"

# Exécution de l'algorithme ACO
best_path, best_distance = ant_colony_tsp(G, num_ants, num_iterations, initial_pheromone, pheromone_evaporation_rate, alpha, beta, start_city)

print("Meilleur chemin trouvé par ACO :", best_path)
print("Distance du meilleur chemin :",  best_distance)