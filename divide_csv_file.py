import pandas as pd
from datetime import datetime

pd.set_option('expand_frame_repr', False)
file = './vacancies_by_year.csv'
df = pd.read_csv(file)

df['year'] = df['published_at'].apply(lambda d: datetime.strptime(d, '%Y-%m-%dT%H:%M:%S%z').year)
years = df['year'].unique()
for year in years:
    data = df[df['year'] == year]
    data.iloc[:, :6].to_csv(rf'csv_files\year_{year}.csv', index=False)
