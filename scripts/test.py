from dash import Dash, dcc, html, Input, Output, ctx
import plotly.express as px
import pandas as pd

app = Dash(__name__)

app.layout = html.Div([
    html.H4('Line Graph'),
    dcc.Dropdown(['Total Cases', 'Total Vaccinations'], "Total Cases", id="line-graph-dropdown"),
    dcc.Graph(id="line-graph"),
    dcc.Checklist(
        id="checklist",
        options=["Asia", "Europe", "Africa","Americas","Oceania"],
        value=["Asia"],
        inline=True,
        style= {
            'color': 'blue'
        }
    ),
    html.H4('Choropleth'),
    dcc.Dropdown(['Total Cases', 'Total Vaccinations'], "Total Cases", id="choropleth-dropdown"),
    dcc.Graph(id="choropleth"),
    html.H4('Scatterplot'),
    dcc.Graph(id="scatterplot")
])

@app.callback(
    Output("line-graph", "figure"),
    Input("line-graph-dropdown", "value"), 
    Input("checklist", "value"))
def update_line_graph(title, continents):
    if title == "Total Cases":
        df = pd.read_csv("./datasets/full_data.csv")
        x, y = 'date', 'total_cases'
    else:
        df = pd.read_csv("./datasets/vaccinations.csv")
        df = df[df['total_vaccinations'].notna()]
        x, y = 'date', 'total_vaccinations'
    df1 = pd.read_csv("./datasets/countryContinent.csv", encoding = "cp1252") 
    df1 = df1.set_index('country')
    df ['continent'] = df['location'].map(df1['continent'])
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
        df = pd.read_csv("./datasets/full_data.csv")
        df = df.sort_values('total_cases', ascending=False).drop_duplicates('location').sort_index()
        df1 = pd.read_csv("./datasets/vaccinations.csv") 
        df1 = df1[df1['total_vaccinations'].notna()]
        df1 = df1.sort_values('total_vaccinations', ascending=False).drop_duplicates('location').sort_index()
        df1 = df1.set_index('location')
        df ['iso'] = df['location'].map(df1['iso_code'])
        fig = px.choropleth(
        df, locations="iso", color="total_cases", hover_name="location",
        range_color=[0, 110000000], color_continuous_scale=px.colors.sequential.Sunsetdark)
    else:
        df = pd.read_csv("./datasets/vaccinations.csv")
        df = df[df['total_vaccinations'].notna()]
        df = df.sort_values('total_vaccinations', ascending=False).drop_duplicates('location').sort_index()
        fig = px.choropleth(
        df, locations="iso_code", color="total_vaccinations", hover_name="location",
        range_color=[0, 3500000000], color_continuous_scale=px.colors.sequential.Sunsetdark)
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig

app.run_server(debug=True)