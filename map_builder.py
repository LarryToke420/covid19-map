import folium
import requests
import pandas as pd
import json
from bs4 import BeautifulSoup
import numpy as np
#data = requests.get("https://covid2019-api.herokuapp.com/v2/current")
#j = data.json()
#df = pd.DataFrame.from_dict(j)
#print(df)

covid_data = requests.get('https://covid2019-api.herokuapp.com/v2/current')
covid_data = covid_data.json()

for data, values in covid_data.items():
    if data == 'data':
        for country in values:
            if country['location'] == 'US':
                country['location']='United States of America'
                print(country['location'])
covid_data = pd.DataFrame.from_dict(covid_data['data'])
#covid_data.location = covid_data.location.replace('US', "United States of America")
covid_data_max = covid_data['confirmed'].max()
covid_data_max = covid_data_max.item()


world_geo = r'countries.geojson'
world_map = folium.Map(location=[4.68, 8.33],
                    tiles='Mapbox Bright', zoom_start=3)
world_map = folium.Choropleth(
    geo_data=world_geo,
    name='choropleth',
    data=covid_data,
    columns=['location','confirmed'],
    key_on='properties.ADMIN',
    threshold_scale = [0,100,(covid_data_max/10),(covid_data_max/4),covid_data_max],
    fill_color='BuPu',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Number of cases per country',
    highlight=True,
    line_color='black'
    ).add_to(world_map)

folium.LayerControl().add_to(world_map)
world_map.save(r'./templates/map.html')