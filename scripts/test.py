from dash import Dash, dcc, html, Input, Output, ctx
import plotly.express as px
import pandas as pd

app = Dash(__name__)

app.layout = html.Div([
    html.H1('Covid-19 Information Visualization Report 2020-2022',
                style= {
                    'text-align': 'center'
                }
            ),
    html.Div([
        html.Div([
            html.Div([
                html.H4('Line Graph'),
                dcc.Dropdown(
                    ['Total Cases', 'Total Vaccinations'], 
                    "Total Cases", 
                    id="line-graph-dropdown",
                    style= {
                        'height': '100%',
                        'width': '200px'
                    }
                )    
            ],
            style= {
                'width': '20%',
                'display': 'flex',
                'justify-content': 'space-between',
                'align-items': 'center'
            }
            ),
            dcc.Graph(id="line-graph"),
            dcc.Checklist(
                id="checklist",
                options=["Asia", "Europe", "Africa","Americas","Oceania"],
                value=["Asia"],
                inline=True,
                style= {
                    'color': 'blue'
                }
            )
        ],
        id='line-graph-id',
        style= {
            'width': '80%',
            'padding-left': '5%',
            'padding-top': '2%',
            'padding-bottom': '2%',
            'padding-right': '5%',
            'background-color': '#fff',
            'color': '#000',
            'border-radius': '4px',
            'box-shadow': '0px 2px 15px rgb(0 0 0 / 17%)'
        }
        ),
    ],
    style = {
        'display' : 'flex',
        'justify-content': 'center',
        'margin-bottom': '50px'
    }
    ),
    html.Div([
        html.Div([
            html.Div([
                html.H4('Choropleth'),
                dcc.Dropdown(
                    ['Total Cases', 'Total Vaccinations'], 
                    "Total Cases", 
                    id="choropleth-dropdown",
                    style= {
                        'height': '100%',
                        'width': '200px'
                    }
                )    
            ],
            style= {
                'width': '20%',
                'display': 'flex',
                'justify-content': 'space-between',
                'align-items': 'center'
            }
            ),
            dcc.Graph(id="choropleth"),
        ],
        id='choropleth-id',
        style= {
            'width': '80%',
            'padding-left': '5%',
            'padding-top': '2%',
            'padding-bottom': '2%',
            'padding-right': '5%',
            'background-color': '#fff',
            'color': '#000',
            'border-radius': '4px',
            'box-shadow': '0px 2px 15px rgb(0 0 0 / 17%)'
        }
        ),
    ],
    style = {
        'display' : 'flex',
        'justify-content': 'center',
        'margin-bottom': '50px'
    }
    ),
    html.Div([
        html.Div([
            html.Div([
                html.H4('Scatterplot'),
                dcc.Dropdown(
                    ['Correlation between Total Vaccinations and New Cases', 'Correlation between Total Vaccinations and Case Fatality Rate'],
                    "Correlation between Total Vaccinations and New Cases",
                    id="scatterplot-dropdown",
                    style= {
                        'height': '100%',
                        'width': '500px'
                    }
                )    
            ],
            style= {
                'width': '40%',
                'display': 'flex',
                'justify-content': 'space-between',
                'align-items': 'center'
            }
            ),
            dcc.Graph(id="scatterplot"),
        ],
        id='scatterplot-id',
        style= {
            'width': '80%',
            'padding-left': '5%',
            'padding-top': '2%',
            'padding-bottom': '2%',
            'padding-right': '5%',
            'background-color': '#fff',
            'color': '#000',
            'border-radius': '4px',
            'box-shadow': '0px 2px 15px rgb(0 0 0 / 17%)'
        }
        ),
    ],
    style = {
        'display' : 'flex',
        'justify-content': 'center',
        'margin-bottom': '50px'
    }
    )
],
style= {
    "font-family": "'Roboto', sans-serif"
}
)

@app.callback(
    Output("line-graph", "figure"),
    Input("line-graph-dropdown", "value"), 
    Input("checklist", "value"))
def update_line_graph(title, continents):
    if title == "Total Cases":
        df = pd.read_csv("../../datasets/full_data.csv")
        df2 = pd.read_csv("../../datasets/vaccinations.csv") 
        df2 = df2[df2['total_vaccinations'].notna()]
        df2 = df2.sort_values('total_vaccinations', ascending=False).drop_duplicates('location').sort_index()
        df2 = df2.set_index('location')
        df['iso_code'] = df['location'].map(df2['iso_code'])
        x, y = 'date', 'total_cases'
    else:
        df = pd.read_csv("../../datasets/vaccinations.csv")
        df = df[df['total_vaccinations'].notna()]
        x, y = 'date', 'total_vaccinations'
    df1 = pd.read_csv("../../datasets/countryContinent.csv", encoding = "cp1252") 
    df1 = df1.set_index('code_3')
    df['continent'] = df['iso_code'].map(df1['continent'])
    dateMask = df['date'].between('2020-01-01', '2022-12-31')
    df  = df[dateMask]
    mask = df.continent.isin(continents)


    fig = px.line(df[mask], x=x, y=y, color="location")    
    return fig
    
@app.callback(
    Output("choropleth", "figure"), 
    Input("choropleth-dropdown", "value"))
def display_choropleth(title):
    if title == "Total Cases":
        df = pd.read_csv("../../datasets/full_data.csv")
        df = df.sort_values('total_cases', ascending=False).drop_duplicates('location').sort_index()
        df1 = pd.read_csv("../../datasets/vaccinations.csv") 
        df1 = df1[df1['total_vaccinations'].notna()]
        df1 = df1.sort_values('total_vaccinations', ascending=False).drop_duplicates('location').sort_index()
        df1 = df1.set_index('location')
        df ['iso'] = df['location'].map(df1['iso_code'])
        fig = px.choropleth(
        df, locations="iso", color="total_cases", hover_name="location",
        range_color=[0, 110000000], color_continuous_scale=px.colors.sequential.Sunsetdark)
    else:
        df = pd.read_csv("../../datasets/vaccinations.csv")
        df = df[df['total_vaccinations'].notna()]
        df = df.sort_values('total_vaccinations', ascending=False).drop_duplicates('location').sort_index()
        fig = px.choropleth(
        df, locations="iso_code", color="total_vaccinations", hover_name="location",
        range_color=[0, 3500000000], color_continuous_scale=px.colors.sequential.Sunsetdark)
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig

@app.callback(
    Output("scatterplot", "figure"), 
    Input("scatterplot-dropdown", "value"))
def display_scatterplot(title):
    df = pd.read_csv("../../datasets/full_data.csv")
    df1 = pd.read_csv("../../datasets/vaccinations.csv")
    dateMask = df['date'].between('2020-11-01', '2022-12-31')
    df  = df[dateMask]
    df1 = df1[dateMask]

    df = df.loc[df['location'] == "World"]
    df1 = df1.loc[df1['location'] == "World"]
    df1 = df1.set_index('date')
    df ['total_vaccinations'] = df['date'].map(df1['total_vaccinations'])
    df = df.fillna(0)
    df['case_fatality_rate'] = df.total_deaths / df.total_cases * 100
    if title == "Correlation between Total Vaccinations and New Cases":
        x,y = "total_vaccinations", "new_cases"
    else:
        x,y = "total_vaccinations", "case_fatality_rate"
    fig = px.scatter(
        df, x=x, y=y
    )
    return fig
app.run_server(debug=True)