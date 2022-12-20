import requests
import pandas as pd
from datetime import datetime


def try_get_json(page, start_date, end_date):
    for i in range(100):
        response = requests.get(
            f'https://api.hh.ru/vacancies?date_from={start_date}&date_to={end_date}&specialization=1&per_page=100&page={page}')
        if response.status_code == 200:
            return response.json()
    raise requests.exceptions.RetryError('Не удалось получить ответ от сервеа')


def get_vacancies(start_date, end_date):
    json = requests.get(
        f'https://api.hh.ru/vacancies?date_from={start_date}&date_to={end_date}&specialization=1&per_page=100').json()
    pages = json['pages']
    vacancies = []
    for page in range(pages):
        json = try_get_json(page, start_date, end_date)
        for vacancy in json['items']:
            new_vacancy = {'name': vacancy['name'],
                           'salary_from': vacancy['salary']['from'] if vacancy['salary'] else None,
                           'salary_to': vacancy['salary']['to'] if vacancy['salary'] else None,
                           'salary_currency': vacancy['salary']['currency'] if vacancy['salary'] else None,
                           'area_name': vacancy['area']['name'], 'published_at': vacancy['published_at']}
            vacancies.append(new_vacancy)
    return vacancies


date1 = datetime.strptime('2022-12-15T14:51:41+0300', '%Y-%m-%dT%H:%M:%S%z').replace(hour=0, minute=0,
                                                                                     second=0).strftime(
    '%Y-%m-%dT%H:%M:%S')
date2 = datetime.strptime('2022-12-15T14:51:41+0300', '%Y-%m-%dT%H:%M:%S%z').replace(hour=6, minute=0,
                                                                                     second=0).strftime(
    '%Y-%m-%dT%H:%M:%S')
date3 = datetime.strptime('2022-12-15T14:51:41+0300', '%Y-%m-%dT%H:%M:%S%z').replace(hour=12, minute=0,
                                                                                     second=0).strftime(
    '%Y-%m-%dT%H:%M:%S')
date4 = datetime.strptime('2022-12-15T14:51:41+0300', '%Y-%m-%dT%H:%M:%S%z').replace(hour=18, minute=0,
                                                                                     second=0).strftime(
    '%Y-%m-%dT%H:%M:%S')
date5 = datetime.strptime('2022-12-15T14:51:41+0300', '%Y-%m-%dT%H:%M:%S%z').replace(hour=23, minute=59,
                                                                                     second=59).strftime(
    '%Y-%m-%dT%H:%M:%S')

vacancies = get_vacancies(date1, date2) + get_vacancies(date2, date3) + get_vacancies(date3, date4) + get_vacancies(
    date4, date5)

pd.set_option('expand_frame_repr', False)
df = pd.DataFrame.from_dict(vacancies)
df.to_csv('api_vacancies.csv')
