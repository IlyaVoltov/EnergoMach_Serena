"""
    Первая страница:
        - интерактивная карта;
        - таблица.
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash_html_components import Div
from pandas.io.formats import style
import plotly.graph_objects as go
import dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

""" READ DATA """
df = pd.read_csv('data//dataFE.csv')
number_name = df.number
site_lat = df.lat
site_lon = df.lon
region_name = df.region
city_name = df.city
wind_name = df.wind
rain_name = df.rain
date_name = df.date
probability_name = df.probability


""" LAYOUT """
mapbox_access_token = open("data//token.mapbox_token").read()

# fig = go.Figure()
# fig.update_layout(
#             legend=dict(
#                 x=0,
#                 y=1,
#                 title_text='Легенда карты (нажмите)',
#                 title_font_family="Rockwell",
#                 font=dict(
#                     family="Rockwell",
#                     size=12,
#                     color="black"
#                 ),
#                 bgcolor="LightCyan",
#                 bordercolor="Cyan",
#                 borderwidth=2
#             ),
#             title='Интерактивная карта аварийных отключений',
#             font=dict(
#                 family="Rockwell",
#                 size=17,
#                 color="rgb(47, 79, 79)"
#             ),
#             autosize=True,
#             hovermode="closest",
#             hoverlabel=dict(
#                 bgcolor="white",
#                 font_size=14,
#                 font_family="Rockwell"
#             ),
#             showlegend=True,
#             mapbox=dict(
#                 accesstoken=mapbox_access_token,
#                 bearing=0,
#                 center=dict(
#                     lat=56.25,
#                     lon=40.15
#                 ),
#                 pitch=0,
#                 zoom=5,
#                 style='satellite'
#             ),
#         )
# fig.add_trace(go.Scattermapbox(
#             name='Центры регионов',
#             lat=site_lat,
#             lon=site_lon,
#             mode='markers',
#             marker=go.scattermapbox.Marker(
#                 size=21,
#                 opacity=0.8,
#                 color='rgb(0, 255, 44)',
#                 ),
#             text=region_name,
#             hoverinfo='text'
#         ))
# '''HARDCODE'''
# fig.add_trace(go.Scattermapbox(
#             name='Регионы с вероятностью аварии',
#             lat=['56.1281561', '48.7072005', '59.2484186', '51.6592378'],
#             lon=['40.4082995', '44.5170207', '39.8356461', '39.1968284'],
#             mode='markers',
#             marker=go.scattermapbox.Marker(
#                 size=12,
#                 opacity = 0.8,
#                 color = 'rgb(254, 1, 1)',
#                 symbol = 'circle'
#             ),
#             text=["Ветер и гроза", "Ветер и гроза", "Ветер и гроза",
#                 "Ветер и гроза"],
#             hoverinfo='text'
#         ))

column_names = [{"name": "№", "id": "number"},
                #{"name": "Широта", "id": "lat"},
                #{"name": "Долгота", "id": "lon"},
                {"name": "Регион", "id": "region"},
                {"name": "Центр региона", "id": "city"},
                {"name": "Ветер, м/с", "id": "wind"},
                {"name": "Дождь", "id": "rain"},
                {"name": "Температура", "id": "temperature"},
                {"name": "Прогноз на", "id": "date"},
                {"name": "Процент вероятности аварии", "id": "probability"},
                ]

date_selector = dcc.RangeSlider(
    id='slider',
    min=min(df.probability),
    max=max(df.probability),
    marks={0: '0', 10: '10', 20: '20', 30: '30', 40: '40', 50: '50', 60: '60', 70: '70', 80: '80', 90: '90', 100: '100'},
    step=1,
    value=[25, 75]
)

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1('Hackathon EnergoMach. Team "Serena SK".',
    style ={
        'color': "rgb(47, 79, 79)",
        'margin-left': "auto",
        'margin-right': "auto",
        'width': "100%",
        'height': '100%',
        'text-align': "center",
        'font-family': "Rockwell",
        'background-color': "rgb(176, 224, 230)"}
        ),
    dcc.Graph(
    #figure=fig,
    id='map',
    style={
        'color': "rgb(47, 79, 79)",
        'width': "100%",
        'height': "850px",
        'background-color': "rgb(176, 224, 230)"}
        ),
    html.Div('Выберите процент вероятности аварийной ситуации',
    style={
        'font-family': "Rockwell",
        'color': "rgb(47, 79, 79)",
        'margin-bottom': '40px',
        'font-size': '24px',
        'margin-left': '90px'}
        ),
    html.Div(date_selector,
    style={
        'width': '100%',
        'margin-bottom': '80px'}
        ),
    dash_table.DataTable(
        id='table',
        columns=column_names,
        #title='Интерактивная карта аварийных отключений',
        style_data_conditional=[{
            'if': {'column_editable': False},
            'textAlign': 'center',
            'border': '1px solid black'
        }],
        style_header_conditional=[{
            'if': {'column_editable': False},
            'textAlign': 'center',
            'textDecoration': 'underline',
            'backgroundColor': 'rgb(176, 224, 230)',
            'border': '1px solid black',
            'color': 'rgb(47, 79, 79)'
        }],
        data=df.to_dict('records'),
        filter_action='native',
        page_action="native",
        page_current= 0,
        page_size= 10,
    )
])

@app.callback(
     Output(component_id='map', component_property='figure'),
     Input(component_id='slider', component_property='value')
   )
def update_map(update):
    new_data = df[(df.probability > update[0]) &
                (df.probability < update[1])]
    #print(new_data)
    fig = go.Figure()
    fig.update_layout(
            legend=dict(
                x=0,
                y=1,
                title_text='Легенда карты (нажмите)',
                title_font_family="Rockwell",
                font=dict(
                    family="Rockwell",
                    size=12,
                    color="black"
                ),
                bgcolor="LightCyan",
                bordercolor="Cyan",
                borderwidth=2
            ),
            title='Интерактивная карта аварийных отключений',
            font=dict(
                family="Rockwell",
                size=17,
                color="rgb(47, 79, 79)"
            ),
            autosize=True,
            hovermode="closest",
            hoverlabel=dict(
                bgcolor="white",
                font_size=14,
                font_family="Rockwell"
            ),
            showlegend=True,
            mapbox=dict(
                accesstoken=mapbox_access_token,
                bearing=0,
                center=dict(
                    lat=56.25,
                    lon=40.15
                ),
                pitch=0,
                zoom=5,
                style='satellite'
            ),
        )
    fig.add_trace(go.Scattermapbox(
                name='Центры регионов',
                lat=new_data.lat,
                lon=new_data.lon,
                mode='markers',
                marker=go.scattermapbox.Marker(
                    size=21,
                    opacity=0.8,
                    color='rgb(0, 255, 44)',
                    ),
                text=region_name,
                hoverinfo='text'
            ))
    '''HARDCODE'''
    fig.add_trace(go.Scattermapbox(
            name='Регионы с вероятностью аварии',
            lat=['56.1281561', '48.7072005', '59.2484186', '51.6592378'],
            lon=['40.4082995', '44.5170207', '39.8356461', '39.1968284'],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=12,
                opacity = 0.8,
                color = 'rgb(254, 1, 1)',
                symbol = 'circle'
            ),
            text=["Ветер и гроза", "Ветер и гроза", "Ветер и гроза",
                "Ветер и гроза"],
            hoverinfo='text'
        ))
    
    return fig


if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=True)