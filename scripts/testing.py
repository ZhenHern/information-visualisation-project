import pandas as pd
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
print(df)