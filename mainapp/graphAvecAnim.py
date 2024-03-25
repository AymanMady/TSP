import time
import matplotlib.pyplot as plt
import random
import openpyxl
import re
import networkx as nx
import numpy as np
import plotly.graph_objects as go
from aco import AntColony

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
        city_coords[city] = (float(lat), float(lon))

    return city_coords

def plot_nodes(cities, w=12, h=8):
    for city, (x, y) in cities.items():
        plt.plot(x, y, "g.", markersize=15)
        plt.text(x, y, city, fontsize=9)
    plt.axis("off")
    fig = plt.gcf()
    fig.set_size_inches([w, h])

def plot_animated_path(cities, ant_count=50, iterations=50):
    COORDS = list(cities.values())
    
    # Initialize ant colony
    colony = AntColony(COORDS, ant_count=ant_count, iterations=iterations)
    optimal_path_coords = colony.get_path()
    
    # Map the optimal path coordinates back to city names
    optimal_path_cities = [list(cities.keys())[list(cities.values()).index(coord)] for coord in optimal_path_coords]
    
    # Plot the initial nodes
    plot_nodes(cities)

    # Define line color
    line_color = 'red'

    fig = go.Figure()

    # Add initial trace (Nouakchott to Nouadhibou)
    x_values = [cities["Nouakchott"][0], cities["Nouadhibou"][0]]
    y_values = [cities["Nouakchott"][1], cities["Nouadhibou"][1]]
    fig.add_trace(go.Scatter(x=x_values, y=y_values, mode='lines+markers', line=dict(color=line_color)))

    # Add city names
    city_names = [optimal_path_cities[0], optimal_path_cities[1]]
    fig.add_trace(go.Scatter(x=x_values, y=y_values, text=city_names, mode="text", textposition="top left"))

    # Define frames
    frames = []
    for i in range(1, len(optimal_path_cities)):
        x_values.append(cities[optimal_path_cities[i]][0])
        y_values.append(cities[optimal_path_cities[i]][1])

        frame_trace = go.Scatter(x=x_values, y=y_values, mode='lines+markers', line=dict(color=line_color))
        frames.append(go.Frame(data=[frame_trace], name=f'frame_{i}'))

        # Add city name
        city_names.append(optimal_path_cities[i])
        fig.add_trace(go.Scatter(x=x_values, y=y_values, text=city_names, mode="text", textposition="top left"))

    # Add the last frame to return to Nouakchott
    x_values.append(cities["Nouakchott"][0])
    y_values.append(cities["Nouakchott"][1])
    frame_trace = go.Scatter(x=x_values, y=y_values, mode='lines+markers', line=dict(color=line_color))
    frames.append(go.Frame(data=[frame_trace], name=f'frame_{len(optimal_path_cities)}'))

    # Add city name
    city_names.append(optimal_path_cities[0])
    fig.add_trace(go.Scatter(x=x_values, y=y_values, text=city_names, mode="text", textposition="top left"))

    fig.frames = frames

    # Update layout
    fig.update_layout(
        title="Animated Path",
        xaxis=dict(range=[15, 25]),  # Adjust range according to your data
        yaxis=dict(range=[-17, -6]),  # Adjust range according to your data
        updatemenus=[{
            "buttons": [
                {
                    "args": [
                        None,
                        {
                            "frame": {"duration": 200, "redraw": True},
                            "fromcurrent": True,
                        }
                    ],
                    "label": "Animate",
                    "method": "animate",
                }
            ],
            "type": "buttons",
            "x": 0.5,
            "y": -0.1,
        }]
    )

    fig.show()

# Example usage:
file_path = 'files/data.xlsx'
cities = excel_to_dict(file_path)

def anim(request):
    plot_animated_path(cities)
