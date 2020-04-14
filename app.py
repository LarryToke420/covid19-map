from flask import Flask, render_template
import folium
import requests
import pandas as pd
import json
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def index():
    text = requests.get('https://covid2019-api.herokuapp.com/v2/current')
    new_text = text.json()
    new_text = pd.DataFrame.from_dict(new_text['data'])
    print(new_text)
    world_geo = r'countries.geojson'
    world_map = folium.Map(location=[4.68, 8.33],
                        tiles='Mapbox Bright', zoom_start=3)
    world_map = folium.Choropleth(
        geo_data=world_geo,
        name='choropleth',
        data=new_text,
        columns=['location','confirmed'],
        key_on='properties.ADMIN',
        threshold_scale = [0,1000,5000,130000,580619],
        fill_color='BuPu',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Number of deaths per country',
        highlight=True,
        line_color='black'
        ).add_to(world_map)

    folium.LayerControl().add_to(world_map)
    world_map.save('templates/map.html')
    return render_template('index.html')

@app.route('/map')
def map():
    return render_template('map.html')

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)