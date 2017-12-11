
# coding: utf-8

# In[1]:

# Import of Packages
import pandas as pd
import itertools
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import requests
import json
import numpy as np
from pandas.io.json import json_normalize


# In[2]:

# Import of data
data = pd.read_csv("CCFinalProject/nama_10_gdp_1_Data.csv", na_values=":")


# In[3]:

del data["Flag and Footnotes"]


# In[4]:

#r = requests.get('http://ec.europa.eu/eurostat/wdds/rest/data/v2.1/json/en/nama_10_gdp?precision=1&na_item=B1G&na_item=B1GQ&na_item=D21&na_item=D21X31&na_item=D31&na_item=P3&na_item=P31_S13&na_item=P31_S14&na_item=P31_S14_S15&na_item=P31_S15&na_item=P32_S13&na_item=P3_P5&na_item=P3_P6&na_item=P3_S13&na_item=P41&na_item=P51G&na_item=P5G&na_item=P6&na_item=P61&na_item=P62&na_item=P7&na_item=P71&na_item=P72&na_item=P52_P53&na_item=B11&na_item=B111&na_item=B112&na_item=B2A3G&na_item=D1&na_item=D11&na_item=D12&na_item=D2&na_item=D2X3&na_item=D3&na_item=P52&na_item=P53&na_item=YA0&na_item=YA1&na_item=YA2&unit=CP_MEUR')
#x = r.json()
#df = pd.DataFrame(x)
#print(df)


# In[5]:

df = data.dropna()
available_indicators = df['NA_ITEM'].unique()
unit_indicators = df["UNIT"].unique()
geo_indicators = df["GEO"].unique()
geo_indicators_euro = ['European Union (28 countries)', 'European Union (15 countries)',
       'Euro area (EA11-2000, EA12-2006, EA13-2007, EA15-2008, EA16-2010, EA17-2013, EA18-2014, EA19)',
       'Euro area (19 countries)', 'Euro area (18 countries)',
       'Euro area (12 countries)']

df['GEO_CAT'] = np.where(df['GEO'].isin(geo_indicators_euro), 'Europe Indicators', 'Country Indicators')



# In[18]:

app = dash.Dash(_name_)
server = app.server
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})
#Create List of Indicators for Dropdown Menu

app.layout = html.Div([
    
    # Selection of Units (affects both graphs)
    html.Div
    ([
        dcc.Dropdown
        (
            id='unit',
            options=[{'label': i, 'value': i} for i in unit_indicators],
            value='Chain linked volumes, index 2010=100'
        ),
    ],
        style={'width': '100%', 'display': 'inline-block'}
    ),
    
    # Container for the first graph
    html.Div
    ([
        #Dropdown Menu for x-axis Indicator of graph 1
        html.Div
        ([
            dcc.Dropdown
            (
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Gross domestic product at market prices'
            ),
        ],
            # Style attribute for Dropdown menu for x-axis indicaotr of graph 1
            style={'width': '49%', 'display': 'inline-block'}
        ),
        
        #Dropdown Menu for y-axis indicator of graph 1
        html.Div
        ([
            dcc.Dropdown
            (
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Actual individual consumption'
            ),
        ],
            # Style attribute for Dropdown menu for y-axis indicaotr of graph 1
            style={'width': '49%', 'float': 'right', 'display': 'inline-block'}
        ),
    
        # Graph 1
        dcc.Graph(id='indicator-graphic_1',
        hoverData={'points': [{'customdata': 'Spain'}]}),
    
        #Slider beneath graph 1
        html.Div
        ([
            dcc.Slider
            (
                id='year--slider',
                min=df['TIME'].min(),
                max=df['TIME'].max(),
                value=df['TIME'].max(),
                step=1,
                marks={str(year): str(year) for year in df['TIME'].unique()[[0,5,10,15,20,25,30,35,41]]}
            )
        ],
            style={'width': '90%', "margin":"10px auto"}
        ),
    
    ],
        
        # Style attribute for container of graph 1
        style={'width': '48%', 'display': 'inline-block'}
   
    ),
    
    # Div container to create a space between the two graphs
    html.Div([],style={'width': '4%', 'display': 'inline-block'}),
    
    # Div container for graph 2
    html.Div
    ([
        #Dropdown Menu for country indicator of graph 2
        html.Div
        (
            [
#                dcc.Dropdown(
#                id='country',
#                options=[{'label': i, 'value': i} for i in geo_indicators],
#                value="Spain",
#                multi = True
#                ),
            ],
            # Style attribute for Dropdown menu for country indicaotr of graph 2
            style={'width': '10%', 'display': 'inline-block'}
        ),
        
        #Dropdown Menu for y-axis indicator of graph 2
        html.Div
        (
            [
                dcc.Dropdown(
                id='yaxis-column_graph2',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Actual individual consumption'
                ),
            ],
            # Style attribute for Dropdown menu for y-axis indicaotr of graph 2
            style={'width': '88%', 'display': 'inline-block'}
        ),
        
        # Graph 1
        dcc.Graph(id='indicator-graphic_2',
                clickData={'points': [{'customdata': 'Spain'}]},
                hoverData={'points': [{'customdata': 'Spain'}]}
                 )],
    
        # Style attribute for container of graph 2
        style={'width': '48%', 'display': 'inline-block'}
    
    ),
])



@app.callback(
    dash.dependencies.Output('indicator-graphic_1', 'figure'),
    [dash.dependencies.Input('unit', 'value'),
     dash.dependencies.Input('xaxis-column', 'value'),
     dash.dependencies.Input('yaxis-column', 'value'),
     dash.dependencies.Input('year--slider', 'value')])

def update_graph(unit_name, xaxis_column_name, yaxis_column_name,
                 year_value):
    dff = df[df['TIME'] == year_value][df["UNIT"] == unit_name]
   
    return {
        'data': [go.Scatter(
            x=dff[dff['NA_ITEM'] == xaxis_column_name][dff["GEO_CAT"]==i]['Value'],
            y=dff[dff['NA_ITEM'] == yaxis_column_name][dff["GEO_CAT"]==i]['Value'],
            text=dff[dff['NA_ITEM'] == yaxis_column_name][dff["GEO_CAT"]==i]['GEO'],
            mode='markers',
            customdata=dff[dff['NA_ITEM'] == yaxis_column_name][dff["GEO_CAT"]==i]['GEO'],
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=i
        ) for i in df.GEO_CAT.unique()
        ],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name + " - " + str(year_value),
                'type': 'linear'
            },
            yaxis={
                'title': yaxis_column_name + " - " + str(year_value),
                'type': 'linear'
            },
            margin={'l': 60, 'b': 60, 't': 10, 'r': 0},
            hovermode='closest',
            showlegend = True,
            legend={"orientation":"h", "y":100,"yanchor":"top"}
        )
    }

@app.callback(
    dash.dependencies.Output('indicator-graphic_2', 'figure'),
    [dash.dependencies.Input('indicator-graphic_1', 'hoverData'),
     dash.dependencies.Input('indicator-graphic_1', 'clickData'),
     dash.dependencies.Input('unit', 'value'),
     dash.dependencies.Input('yaxis-column_graph2', 'value')])

def update_graph(hoverData, selectedData,
    unit_name, yaxis_column_name):
    #country_name_list = []
    #country_name_list.append()
    dff2 = df[df["UNIT"] == unit_name][df['NA_ITEM'] == yaxis_column_name]
    #traces = []
    
    
    return {
        'data': [go.Scatter(
        x=dff2[dff2["GEO"]==hoverData['points'][0]['customdata']]['TIME'],
        y=dff2[dff2["GEO"]==hoverData['points'][0]['customdata']]['Value'],
        text=dff2[dff2["GEO"]==hoverData['points'][0]['customdata']]['TIME'],
        mode='line',
        name=hoverData['points'][0]['customdata']
        )],
        'layout': go.Layout(
            xaxis={
                'title': "Years",
                'type': 'linear'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear'
            },
            margin={'l': 60, 'b': 60, 't': 10, 'r': 0},
            hovermode='closest',
            showlegend = True,
            legend={"orientation":"h", "y":100, "yanchor":"top"}
        )
    }

if __name__ == '__main__':
    app.run_server()


# In[ ]:



