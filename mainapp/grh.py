import pandas as pd
import networkx as nx

def generate_shortest_distance_graph(file_path):
    try:
        # Step 1: Read Excel file to extract data
        df = pd.read_excel(file_path)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

    try:
        # Step 2: Initialize graph and calculate shortest distances
        G = nx.Graph()
        cities = df['Ville'].unique()  # Extract unique city names
        num_cities = len(cities)

        for i in range(num_cities):
            for j in range(i + 1, num_cities):
                city1, city2 = cities[i], cities[j]
                shortest_distance = calculate_shortest_distance(df, city1, city2)
                if shortest_distance is not None:
                    G.add_edge(city1, city2, weight=shortest_distance)

        return G
    except KeyError:
        print("Error: 'Ville' column not found in the Excel file.")
        return None

def calculate_shortest_distance(df, city1, city2):
    # Placeholder for your implementation of Dijkstra's algorithm or a suitable approximation
    pass

# Example usage:
file_path = '../files/data.xlsx'
graph = generate_shortest_distance_graph(file_path)
if graph:
    print("Graph generated successfully.")
   