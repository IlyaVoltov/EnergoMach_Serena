"""
    Вторая страница:
        - карта ...;
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

""" READ DATA """
df = pd.read_csv('data//dataSERENA.csv')
number_name = df.number
site_lat = df.lat
site_lon = df.lon
locations_name = df.adress
note_name = df.note
type_name = df.type
description_name = df.description
inference_name = df.inference
party_name = df.party.unique()


""" LAYOUT """
mapbox_access_token = open("data//token.mapbox_token").read()

fig = go.Figure()

fig.add_trace(go.Scattermapbox(
    name='Все объекты проверки',
    lat=site_lat,
    lon=site_lon,
    mode='markers',
    marker=go.scattermapbox.Marker(
        size=17,
        opacity=0.8,
        color='rgb(0, 255, 44)',
        symbol='circle'
    ),
    text=locations_name,
    hoverinfo='text'
))

'''fig.add_trace(go.Scattermapbox(
    name='Акт БУ/БД',
    lat=['60.018156', '60.039324', '60.011986', '60.055470'],
    lon=['30.398639', '30.375849', '30.428499', '30.361727'],
    mode='markers',
    marker=go.scattermapbox.Marker(
        size=9,
        opacity = 0.8,
        color = 'rgb(10, 120, 240)',
        symbol = 'circle'
    ),
    text=["Гражданский пр-кт, д 90 к 2.", "пр-кт Культуры, д 11 к 7.", "ул. Карпинского, д 36 к 1.",
          "Придорожная аллея, дом 18, литера А."],
    hoverinfo='text'
))'''

'''fig.add_trace(go.Scattermapbox(
    name='Замечаний нет',
    lat=['60.046050', '60.078666', '60.037539', '60.042074', '60.042271', '60.022656', '60.007492', '60.053179', '60.038510', '60.007834'],
    lon=['30.324582', '30.337140', '30.381966', '30.375723', '30.379882', '30.326953', '30.423262', '30.323468', '30.331652', '30.368518'],
    mode='markers',
    marker=go.scattermapbox.Marker(
        size=9,
        opacity = 0.8,
        color = 'rgb(255, 0, 29)',
        symbol = 'circle'
    ),
    text=["пр-кт Луначарского, д 40 к. 4 литер а.", "ул. Валерия Гаврилина, д 11 к. 1 стр 1.", "ул. Демьяна Бедного, д 10 к 1 литер а.",
          "пр-кт Культуры, д 17.", "пр-кт Просвещения, д 53 к 4 литер а.", "пр-кт Тореза, д 112 к 1 литер а.",
          "ул. Карпинского, д 20.", "ул. Хошимина, участок  14 (юго-западнее пересечения с пр. Просвещения).", "ул. Есенина, участок 27 (западнее дома 7 лит.А по ул.Есенина)."
        "ул. Политехническая, 28, литера А."],
    hoverinfo='text'
))'''

'''fig.add_trace(go.Scattermapbox(
    name='Отказ в доступе',
    lat=['60.062364'],
    lon=['30.287526'],
    mode='markers',
    marker=go.scattermapbox.Marker(
        size=9,
        opacity = 0.8,
        color = 'rgb(0, 150, 254)',
        symbol = 'circle'
    ),
    text=["Береговая улица, дом 32, корпус 5, литера А."],
    hoverinfo='text'
))'''

fig.update_layout(
    legend=dict(
        x=0,
        y=1,
        title_text='Результаты проверки (нажмите)',
        title_font_family="Rockwell",
        font=dict(
            family="Rockwell",
            size=12,
            color="black"
        ),
        bgcolor="LightCyan",
        bordercolor="Cyan",
        borderwidth=1
    ),
    title='Проверка - Система УПЭ - 3ья партия адресов',
    font=dict(
        family="Rockwell",
        size=17,
        color="blue"
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
            lat=60.026,
            lon=30.314
        ),
        pitch=0,
        zoom=9,
        style='light'
    ),
)

PAGE_SIZE = 6

app = dash.Dash(__name__)
server = app.server
app.layout = html.Div([
    dcc.Graph(
        figure=fig,
        id='map'),
    html.Pre(
        id='relayout-data'),
    dash_table.DataTable(
    id='table',
    columns=[{"name": i, "id": i, 'editable': (i == 'note_name')} for i in df.columns],
    style_data_conditional=[{
        'if': {'column_editable': False},
        'backgroundColor': 'rgb(30, 30, 30)',
        'color': 'white'
    }],
    style_header_conditional=[{
        'if': {'column_editable': False},
        'backgroundColor': 'rgb(30, 30, 30)',
        'color': 'white'
    }],
    data=df.to_dict('records'),
)
])

@app.callback(
    Output('table', 'data'),
    [Input('map', 'clickData')])
def change(clickData):
    if clickData is not None:
        return df[df['adress'] == clickData['points'][0]['text']].to_dict('records')
    return df.to_dict('records')


""" CALLBACKS """

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=True)