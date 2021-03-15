#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 13:34:25 2020

@author: sharon
"""

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import json
import requests

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.read_csv('https://raw.githubusercontent.com/MaisHub/Coding-Resume/master/Zillow%20data/State_zhvi_uc_sfr_tier_0.33_0.67_sm_sa_mon.csv')
temp = df[['RegionName','2020-09-30']]
f = requests.get('https://raw.githubusercontent.com/MaisHub/Coding-Resume/master/GepJson/gz_2010_us_040_00_500k.json')
states = json.loads(f.text)
    
fig = px.choropleth_mapbox(temp, geojson=states, locations='RegionName', color='2020-09-30',
                           color_continuous_scale="Viridis", featureidkey="properties.NAME",
                           range_color=(0, 900000),
                           mapbox_style="carto-positron",
                           zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
                           opacity=0.5,
                           labels={'2020-09-30':'unemployment rate'}
                          )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])
  
if __name__ == '__main__':
    #For Development only, otherwise use gunicorn or uwsgi to launch, e.g.
    # gunicorn -b 0.0.0.0:8050 index:app.server
    #app.run_server(port=8050,host='0.0.0.0')
    app.run_server(debug=True)
