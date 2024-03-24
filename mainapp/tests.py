
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
            mode='markers',
            marker=dict(size=10, color='blue'),
            text=nom,
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
        width=300,
        height=300
    )
    
    fig = go.Figure(data=nodes + edges, layout=layout)
    fig.update_layout(margin=dict(t=40, r=0, l=0, b=0))
    
    # Convert the figure to HTML code
    html_code = pio.to_html(fig, full_html=False)
    
    return html_code






# def afficher_tout_posubilite(request):
#     fichier_excel = 'files/data.xlsx'
#     try:
#         columns_to_read = ['Ville', 'Latitude', 'Longitude']
#         df = pd.read_excel(fichier_excel, usecols=columns_to_read)
#     except Exception as e:
#         return render(request, "importation.html", {"message": "il faut importer un fichier excel"})  # Gérer les erreurs de lecture du fichier

#     villes = df.to_dict('records')
#     # Créer une carte centrée 
#     # sur la première ville
#     carte = folium.Map(location=[villes[0]["Latitude"], villes[0]["Longitude"]], zoom_start=6)

#     # Ajouter un marqueur pour chaque ville
#     for ville in villes:
#         nom = ville["Ville"]
#         latitude = ville["Latitude"]
#         longitude = ville["Longitude"]

#         # Ajouter un marqueur avec le nom de la ville
#         folium.Marker(
#             location=[latitude, longitude],
#             popup=nom,
#             icon=folium.Icon(color="blue", icon="info-sign")
#         ).add_to(carte)

#     # Ajouter les lignes reliant chaque paire de villes
#     for ville1, ville2 in itertools.combinations(villes, 2):
#         folium.PolyLine(locations=[(ville1["Latitude"], ville1["Longitude"]), (ville2["Latitude"], ville2["Longitude"])], color='red').add_to(carte)

#     # Sauvegarder la carte dans un fichier HTML
#     carte_html = carte._repr_html_()

#     return render(request, "home.html", {"carte_html": carte_html})
