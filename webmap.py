import folium
from folium.map import FeatureGroup
import pandas as pd


map = folium.Map(location=[38.58, -99.09], zoom_start=6, tiles='cartodb dark_matter')

# map.add_child(folium.Marker(location=[38.2, -99.1], popup="I am a Marker", icon=folium.Icon(color="green")))
# or( a better way to add children)
fgv = folium.FeatureGroup(name="Volcanoes")

# features = [[38.2, -99.1], [39.2, -97.1]]
# for feature in features:
#     fg.add_child(folium.Marker(location=feature, popup="I am a Marker", icon=folium.Icon(color="green")))

# adding coordinates from a textfile('volcanoes_usa.txt' in this case)
data = pd.read_csv("Volcanoes_USA.csv")
lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])

def color_producer(elevation):
    if elevation < 1500:
        return "green"
    elif 1500 <= elevation < 2500:
        return "orange"
    else:
        return "grey"

# for lt, ln, el in zip(lat, lon, elev):
#     fg.add_child(folium.Marker(location=[lt, ln], popup=str(el)+"m", icon=folium.Icon(color=color_producer(el))))

# using circle markers
for lt, ln, el in zip(lat, lon, elev):
    fgv.add_child(folium.CircleMarker(location=[lt, ln], radius=8, popup=str(el)+"m", 
    fill_color=color_producer(el), color="grey", fill_opacity=0.7))

fgp = folium.FeatureGroup(name="Population")

fgp.add_child(folium.GeoJson(data=open('world.json', 'r', encoding='utf-8-sig').read(), 
style_function=lambda x: {'fillColor':'yellow' if x['properties']['POP2005'] < 10000000 
else 'white' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'}))

map.add_child(fgv)
map.add_child(fgp)

map.add_child(folium.LayerControl())

map.save("Map1.html")
