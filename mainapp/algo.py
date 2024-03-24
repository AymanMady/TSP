import folium
import itertools
from django.shortcuts import render
import heapq
import sys
import math
import pandas as pd
import openpyxl
import re
import networkx as nx
from geopy.distance import geodesic
import numpy as np
from django.shortcuts import render

# Function to convert the excel file to a dictionary
import openpyxl
import re

def excel_to_dict(file_path):
    try:
        # Load the workbook and select the first worksheet
        wb = openpyxl.load_workbook(file_path)
        ws = wb.active

        # Check if the headers are correct
        headers = [cell.value.strip() for cell in ws[1]]

        if headers != ["Ville", "Latitude", "Longitude"]:
            raise ValueError("Les en-têtes des colonnes ne correspondent pas au format attendu.")

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

            # Add to dictionary if all values are not None
            if city and lat is not None and lon is not None:
                city_coords[city] = (lat, lon)

        return city_coords
    except Exception as e:
        return render('importation.html', {'message': "Une erreur s'est produite lors de la lecture du fichier Excel. Il faut importer un fichier Excel."})


# View function to visualize the data
# View function to visualize the data
def visialiserLeDonner(request):
    try:
        coord = excel_to_dict('files/data.xlsx') 
    except Exception as e:
        return render(request, 'importation.html', {'message': "Une erreur s'est produite lors de la lecture du fichier Excel. Il faut importer un fichier Excel."})

    return render(request, 'selectdata.html', {'data': coord})