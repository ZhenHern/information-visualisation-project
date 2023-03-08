import pandas as pd
df = pd.read_csv("../../datasets/full_data.csv")
df1 = pd.read_csv("../../datasets/countryContinent.csv", encoding = "cp1252") 
df1 = df1.set_index('country')
df['continent'] = df['location'].map(df1['continent'])
mask = df['date'].between('2020-01-01', '2022-12-31')
print(df[mask])