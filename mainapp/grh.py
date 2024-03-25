import folium
import itertools

def afficher_carte(villes):
    # Créer une carte centrée sur la première ville
    carte = folium.Map(location=[villes[0]["latitude"], villes[0]["longitude"]], zoom_start=6)

    # Ajouter un marqueur pour chaque ville
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

    # Ajouter les lignes reliant chaque paire de villes
    for ville1, ville2 in itertools.combinations(villes, 2):
        folium.PolyLine(locations=[(ville1["latitude"], ville1["longitude"]), (ville2["latitude"], ville2["longitude"])], color='red').add_to(carte)

    # Sauvegarder la carte dans un fichier HTML
    carte.save("carte_villes.html")

# Nouvelles données de villes avec latitude et longitude
nouvelles_villes = [
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

# Afficher la carte avec les villes reliées entre elles
afficher_carte(nouvelles_villes)