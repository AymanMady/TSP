
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
