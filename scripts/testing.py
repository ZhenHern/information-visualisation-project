import pandas as pd
df = pd.read_csv("./datasets/vaccinations.csv")
df = df[df['total_vaccinations'].notna()]
df1 = df.sort_values('total_vaccinations', ascending=False).drop_duplicates('location').sort_index()
print(df1)