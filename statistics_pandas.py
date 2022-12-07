import pandas as pd
from datetime import datetime


def get_main_statistics(file_name, vacancy, return_dict):
    pd.set_option('expand_frame_repr', False)
    df = pd.read_csv(file_name)

    df['published_at'] = df['published_at'].apply(lambda d: datetime.strptime(d, '%Y-%m-%dT%H:%M:%S%z').year)
    df['average_salary'] = df[['salary_from', 'salary_to']].mean(axis=1)
    year = int(df['published_at'].unique())
    df_vacancy = df[df['name'].str.contains(vacancy)]

    salary_level = int(df['average_salary'].mean())
    number_of_vacancies = len(df.index)
    salary_level_by_profession = int(df_vacancy['average_salary'].mean())
    number_of_vacancies_by_profession = len(df_vacancy.index)
    return_dict[year] = [salary_level, number_of_vacancies, salary_level_by_profession,
                         number_of_vacancies_by_profession]


def get_city_statistics(file_name):
    pd.set_option('expand_frame_repr', False)
    df = pd.read_csv(file_name)
    df_length = len(df.index)

    df['average_salary'] = df[['salary_from', 'salary_to']].mean(axis=1)
    df['count'] = df.groupby('area_name')['area_name'].transform('count')
    df = df[df['count'] / df_length >= 0.01]
    df_cities = df.groupby('area_name', as_index=False)['average_salary'].mean().sort_values(by='average_salary',
                                                                                             ascending=False)
    df_cities['average_salary'] = df_cities['average_salary'].apply(lambda x: int(x))
    df_cities = df_cities.head(10)
    salary_level_by_city = dict(zip(df_cities['area_name'], df_cities['average_salary']))

    df['share'] = df['count'] / df_length
    df_share = df.groupby('area_name', as_index=False)['share'].mean().sort_values(by='share', ascending=False)
    share_of_vacancies = dict(zip(df_share['area_name'], round(df_share['share'], 4)))
    return salary_level_by_city, share_of_vacancies
