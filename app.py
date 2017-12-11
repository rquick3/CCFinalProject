
# Import of Packages
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import numpy as np

# Import of data and some minor cleaning
data = pd.read_csv("https://raw.githubusercontent.com/rquick3/CCFinalProject/master/nama10gdp1Data.csv", na_values=":")
del data["Flag and Footnotes"]
df = data.dropna()

# Set dropdown menues and categories
available_indicators = df['NA_ITEM'].unique()
unit_indicators = df["UNIT"].unique()
geo_indicators = df["GEO"].unique()
geo_indicators_euro = ['European Union (28 countries)', 'European Union (15 countries)',
       'Euro area (EA11-2000, EA12-2006, EA13-2007, EA15-2008, EA16-2010, EA17-2013, EA18-2014, EA19)',
       'Euro area (19 countries)', 'Euro area (18 countries)',
       'Euro area (12 countries)']
df['GEO_CAT'] = np.where(df['GEO'].isin(geo_indicators_euro), 'Europe Indicators', 'Country Indicators')

# Set default value for right graph
selected_values = ["Spain"]

# Code of the app
app = dash.Dash(__name__)
server = app.server
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})


app.layout = html.Div([
    
    # Selection of Units (affects both graphs)
    html.Div
    ([	html.Label('Measurement Unit'),
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
        ([	html.Label('Indicator on X-Axis'),
            dcc.Dropdown
            (
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Gross domestic product at market prices'
            ),
        ],
            # Style attribute for Dropdown menu for x-axis indicaotr of graph 1
            style={'width': '98%', 'display': 'inline-block'}
        ),
        
        #Dropdown Menu for y-axis indicator of graph 1
        html.Div
        ([	html.Label('Indicator on Y-axis'),
            dcc.Dropdown
            (
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Actual individual consumption'
            ),
        ],
            # Style attribute for Dropdown menu for y-axis indicaotr of graph 1
            style={'width': '98%', 'display': 'inline-block', "margin-bottom": "30px"}
        ),
    
        # Graph 1
        html.Label('Click data to add to right graph', style={"align":"center"}),
        dcc.Graph(id='indicator-graphic_1',
        #hoverData={'points': [{'customdata': 'Spain'}]}, <- remainder of old code (can be easily redeployed if needed)
        clickData={'points': [{'customdata': 'Spain'}]}),
    
        #Slider beneath graph 1
        html.Div
        ([	html.Label('Select Year'),
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
        style={'width': '47%', "float":"left", 'display': 'inline-block'}
   
    ),
    
    # Div container to create a space between the two graphs
    html.Div([],style={'width': '4%', 'display': 'inline-block'}),
    
    # Div container for graph 2
    html.Div
    ([
        #Dropdown Menu for country indicator of graph 2
        html.Div
        (
            [	html.Label('Countries'),
                dcc.Dropdown(
                id='country',
                options=[{'label': i, 'value': i} for i in geo_indicators],
                multi = True,
                value=[]
                ),
            ],
            # Style attribute for Dropdown menu for country indicaotr of graph 2
            style={'width': '98%', 'display': 'inline-block'}
        ),
        
        #Dropdown Menu for y-axis indicator of graph 2
        html.Div
        (
            [	html.Label('Indicator on Y-Axis'),
                dcc.Dropdown(
                id='yaxis-column_graph2',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Actual individual consumption'
                ),
            ],
            # Style attribute for Dropdown menu for y-axis indicaotr of graph 2
            style={'width': '98%', 'display': 'inline-block', "margin-bottom": "30px"}
        ),
        
        # Graph 2
        dcc.Graph(id='indicator-graphic_2')],
    
        # Style attribute for container of graph 2
        style={'width': '47%', 'display': 'inline-block'}
    
    ),
])


# This callback links the left graph's click data to the country dropdown menu
@app.callback(dash.dependencies.Output('country', 'value'),
			[dash.dependencies.Input('indicator-graphic_1', 'clickData')])

def update_graph(clickData):
	selected_values.append(clickData['points'][0]['customdata'])
	return selected_values

#This callback updates the left graph
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

# This callback updates the right graph
@app.callback(
    dash.dependencies.Output('indicator-graphic_2', 'figure'),
    [#dash.dependencies.Input('indicator-graphic_1', 'hoverData'), <- remainder of old code (can be easily redeployed if needed)
     #dash.dependencies.Input('indicator-graphic_1', 'clickData'), <- remainder of old code (can be easily redeployed if needed)
     dash.dependencies.Input('country', 'value'),
     dash.dependencies.Input('unit', 'value'),
     dash.dependencies.Input('yaxis-column_graph2', 'value')])

def update_graph(#hoverData, clickData, <- remainder of old code (can be easily redeployed if needed)
	country,
    unit_name, yaxis_column_name):
    
    # resetting the selected values to what is currently displayed in the dropdown
    global selected_values
    selected_values = country
	
	# Filtering the dataframe
    dff2 = df[df["UNIT"] == unit_name][df['NA_ITEM'] == yaxis_column_name]
    
    # Setting up one trace for each country selected
    traces = []
    for country_element in selected_values:
    	traces.append(go.Scatter(
        	x=dff2[dff2["GEO"]==country_element]['TIME'],
        	y=dff2[dff2["GEO"]==country_element]['Value'],
        	text=dff2[dff2["GEO"]==country_element]['TIME'],
        	mode='line',
        	name=country_element
        	))
    
    return {
        'data': [trace for trace in traces],
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



