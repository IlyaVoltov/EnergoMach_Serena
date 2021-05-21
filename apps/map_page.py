"""
    Вторая страница:
        - карта ...;
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output

#import pandas as pd

mapbox_access_token = open("data//token.mapbox_token").read()