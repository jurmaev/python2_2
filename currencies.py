import pandas as pd
from datetime import datetime
from dateutil import rrule
import xml.etree.ElementTree as ET
from urllib.request import urlopen

pd.set_option('expand_frame_repr', False)
df = pd.read_csv('vacancies_dif_currencies.csv')
df = df.dropna(subset=['salary_from', 'salary_to'], how='all')
df['currency_count'] = df.groupby('salary_currency')['salary_currency'].transform('count')
df = df[df['currency_count'] > 5000]
print(df['salary_currency'].value_counts())
start_date = datetime.strptime(df['published_at'].min(), '%Y-%m-%dT%H:%M:%S%z').replace(day=28, hour=12, minute=0,
                                                                                        second=0)
end_date = datetime.strptime(df['published_at'].max(), '%Y-%m-%dT%H:%M:%S%z').replace(day=28, hour=12, minute=0,
                                                                                      second=0)

currencies = df['salary_currency'].unique()
today = datetime.now()
tree = ET.parse(urlopen(f'http://www.cbr.ru/scripts/XML_daily.asp?date_req={today.day}/{today.month}/{today.year}'))
currency_ids = {}
root = tree.getroot()
for child in root.findall('Valute'):
    currency_name = child.find('CharCode').text
    if currency_name in currencies:
        currency_ids[currency_name] = list(child.attrib.values())[0]

currency_dynamic = {key: [] for key in currency_ids.keys()}
currency_dynamic['date'] = []
for dt in rrule.rrule(rrule.MONTHLY, dtstart=start_date, until=end_date):
    tree = ET.parse(
        urlopen(f'http://www.cbr.ru/scripts/XML_daily.asp?date_req=28/{dt.strftime("%m/%Y")}d=1'))
    root = tree.getroot()
    for child in root.findall('Valute'):
        code = child.find('CharCode').text
        if code in currency_ids.keys():
            if dt.strftime('%Y-%m') not in currency_dynamic['date']:
                currency_dynamic['date'] += [dt.strftime('%Y-%m')]
            coeff = float(child.find('Value').text.replace(',', '.')) / float(child.find('Nominal').text)
            currency_dynamic[code] += [coeff]

currency_df = pd.DataFrame(data=currency_dynamic)
cols = currency_df.columns.tolist()
cols = cols[-1:] + cols[:-1]
currency_df = currency_df[cols]
currency_df.to_csv('currency_dynamic.csv', index=False)
