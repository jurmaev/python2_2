import math
import numpy as np
import pandas as pd
from datetime import datetime
from dateutil import rrule
import xml.etree.ElementTree as ET
from urllib.request import urlopen


def get_currency_dynamic(file_name):
    pd.set_option('expand_frame_repr', False)
    df = pd.read_csv(file_name)
    df = df.dropna(subset=['salary_from', 'salary_to'], how='all')
    df['currency_count'] = df.groupby('salary_currency')['salary_currency'].transform('count')
    df = df[df['currency_count'] > 5000]
    return df


def get_currency_dynamic_csv(file_name):
    df = get_currency_dynamic(file_name)
    print(df['salary_currency'].value_counts())
    currencies = df['salary_currency'].unique()
    currencies = currencies[currencies != 'RUR']
    start_date = datetime.strptime(df['published_at'].min(), '%Y-%m-%dT%H:%M:%S%z').replace(day=28, hour=12, minute=0,
                                                                                            second=0)
    end_date = datetime.strptime(df['published_at'].max(), '%Y-%m-%dT%H:%M:%S%z').replace(day=28, hour=12, minute=0,
                                                                                          second=0)
    # today = datetime.now()
    # tree = ET.parse(urlopen(f'http://www.cbr.ru/scripts/XML_daily.asp?date_req={end_date.day}/{end_date.month}/{end_date.year}'))
    # currency_ids = {}
    # root = tree.getroot()
    # for child in root.findall('Valute'):
    #     currency_name = child.find('CharCode').text
    #     if currency_name in currencies:
    #         currency_ids[currency_name] = list(child.attrib.values())[0]

    currency_dynamic = {key: [] for key in currencies}
    # print(currency_dynamic)
    currency_dynamic['date'] = []
    for dt in rrule.rrule(rrule.MONTHLY, dtstart=start_date, until=end_date):
        tree = ET.parse(
            urlopen(f'http://www.cbr.ru/scripts/XML_daily.asp?date_req=28/{dt.strftime("%m/%Y")}d=1'))
        root = tree.getroot()
        for child in root.findall('Valute'):
            code = child.find('CharCode').text
            if code in currencies:
                if dt.strftime('%Y-%m') not in currency_dynamic['date']:
                    currency_dynamic['date'] += [dt.strftime('%Y-%m')]
                coeff = float(child.find('Value').text.replace(',', '.')) / float(child.find('Nominal').text)
                currency_dynamic[code] += [coeff]
        for key in currency_dynamic.keys():
            if key != 'date' and len(currency_dynamic['date']) > len(currency_dynamic[key]):
                currency_dynamic[key] += ['NaN']
    print(currency_dynamic['BYR'])
    currency_df = pd.DataFrame(data=currency_dynamic)
    cols = currency_df.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    currency_df = currency_df[cols]
    currency_df.to_csv('currency_dynamic.csv', index=False)

get_currency_dynamic_csv('vacancies_dif_currencies.csv')
def convert_salary_to_rub(file_name):


    def convert_to_rub(row):
        if row['salary_currency'] != 'RUR':
            date = datetime.strptime(row['published_at'], '%Y-%m-%dT%H:%M:%S%z')
            df = pd.read_csv(f'csv_files/year_{date.year}.csv')
            convert_value = df[df['date'] == date.strftime('%Y-%m')][row['salary_currency']].values[0]
            print(type(convert_value))
            return row['salary_currency'] * convert_value
        return row['salary_currency']
    def count_salary(row):
        if math.isnan(row['salary_from']):
            return row['salary_to']
        elif math.isnan(row['salary_to']):
            return row['salary_from']
        return (row['salary_from'] + row['salary_to']) / 2

    df = get_currency_dynamic(file_name)
    df['salary'] = df.apply(count_salary, axis=1)
    df.apply(convert_to_rub, axis=1)
    print(df.head(10))

# convert_salary_to_rub('vacancies_dif_currencies.csv')