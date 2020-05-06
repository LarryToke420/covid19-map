from flask import Flask, render_template
import folium
import requests
import pandas as pd
import json
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def index():
    covid_data = requests.get('https://covid2019-api.herokuapp.com/v2/current')
    covid_data = covid_data.json()
    covid_data = pd.DataFrame.from_dict(covid_data['data'])
    covid_data_max = covid_data['confirmed'].max()
    covid_data_max = covid_data_max.item()

    covid_data.at['location','US'] = 'USA'
    print(covid_data['location']['USA'])


    world_geo = r'countries.geojson'
    world_map = folium.Map(location=[4.68, 8.33],
                        tiles='Mapbox Bright', zoom_start=3)
    world_map = folium.Choropleth(
        geo_data=world_geo,
        name='choropleth',
        data=covid_data,
        columns=['location','confirmed'],
        key_on='properties.ADMIN',
        threshold_scale = [0,int((covid_data_max/15)),int((covid_data_max/10)),int((covid_data_max/4)),covid_data_max],
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