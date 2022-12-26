import pandas as pd
import sqlite3

file_name = 'vacancies_dif_currencies.csv'
dynamic_file_name = 'currency_dynamic.csv'
df = pd.read_csv(dynamic_file_name)

conn = sqlite3.connect('currency_dynamic.sqlite3')
c = conn.cursor()
c.execute(
    'CREATE TABLE IF NOT EXISTS currency_dynamic (date text, USD float, EUR float, KZT float, UAH float, BYR float)')
conn.commit()
df.to_sql('currency_dynamic', conn, if_exists='replace', index=False)
c.execute('SELECT * FROM currency_dynamic')
for row in c.fetchmany(10):
    print(row)

conn.close()
