import pandas as pd
from datetime import datetime


def divide_file_by_year(file_name):
    pd.set_option('expand_frame_repr', False)
    df = pd.read_csv(file_name)

    df['year'] = df['published_at'].apply(lambda d: datetime.strptime(d, '%Y-%m-%dT%H:%M:%S%z').year)
    years = df['year'].unique()
    for year in years:
        data = df[df['year'] == year]
        data.iloc[:, :6].to_csv(rf'csv_files\year_{year}.csv', index=False)

    return years


def divide_currency_file_by_year(file_name):
    pd.set_option('expand_frame_repr', False)
    df = pd.read_csv(file_name)

    df['year'] = df['date'].apply(lambda d: datetime.strptime(d, '%Y-%m').year)
    years = df['year'].unique()
    for year in years:
        data = df[df['year'] == year]
        data = data.drop('year', axis=1)
        data.to_csv(rf'csv_files\year_{year}.csv', index=False)

    return years


divide_currency_file_by_year('currency_dynamic.csv')