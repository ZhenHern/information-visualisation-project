from dash import Dash, dcc, html, Input, Output, ctx
import plotly.express as px
import pandas as pd

app = Dash(__name__)

app.layout = html.Div([
    html.H4('Line Graph'),
    dcc.Dropdown(['Total Cases', 'Total Vaccinations'], "Total Cases", id="line-graph-dropdown"),
    dcc.Graph(id="graph"),
    dcc.Checklist(
        id="checklist",
        options=["Asia", "Europe", "Africa","Americas","Oceania"],
        value=["Asia"],
        inline=True
    ),
])

@app.callback(
    Output("graph", "figure"),
    Input("line-graph-dropdown", "value"), 
    Input("checklist", "value"))
def update_line_graph(title, continents):
    triggered_id = ctx.triggered_id
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
    
app.run_server(debug=True)