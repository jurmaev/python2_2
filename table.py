import csv
import re
from prettytable import PrettyTable
from datetime import datetime
import sys


class Salary:
    def __init__(self, salary_from, salary_to, salary_gross, salary_currency):
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.salary_gross = salary_gross
        self.salary_currency = salary_currency

    currency_to_rub = {
        "AZN": 35.68,
        "BYR": 23.91,
        "EUR": 59.90,
        "GEL": 21.74,
        "KGS": 0.76,
        "KZT": 0.13,
        "RUR": 1,
        "UAH": 1.64,
        "USD": 60.66,
        "UZS": 0.0055,
    }
    currency = {
        "AZN": "Манаты",
        "BYR": "Белорусские рубли",
        "EUR": "Евро",
        "GEL": "Грузинский лари",
        "KGS": "Киргизский сом",
        "KZT": "Тенге",
        "RUR": "Рубли",
        "UAH": "Гривны",
        "USD": "Доллары",
        "UZS": "Узбекский сум",
    }

    def get_salary(self):
        salary_from = int(float(self.salary_from))
        salary_to = int(float(self.salary_to))
        salary_from = ' '.join(f'{salary_from:,}'.split(','))
        salary_to = ' '.join(f'{salary_to:,}'.split(','))
        formatted_currency = self.currency[self.salary_currency]
        salary_gross = 'С вычетом налогов' if self.salary_gross == 'False' else 'Без вычета налогов'
        return f'{salary_from} - {salary_to} ({formatted_currency}) ({salary_gross})'

    def get_average_salary_rub(self):
        return ((float(self.salary_from) + float(self.salary_to)) / 2) * self.currency_to_rub[
            self.salary_currency]

    def get_currency(self):
        return self.currency[self.salary_currency]


class Vacancy:
    def __init__(self, name, description, key_skills, experience_id, premium, employer_name, salary, area_name,
                 published_at):
        self.name = name
        self.description = description
        self.key_skills = key_skills
        self.experience_id = experience_id
        self.premium = premium
        self.employer_name = employer_name
        self.salary = salary
        self.area_name = area_name
        self.published_at = published_at


class DataSet:
    def __init__(self, file_name):
        self.file_name = file_name
        self.vacancies_objects = DataSet.create_vacancies_objects(self.file_name)

    en_to_rus_headings = {
        'name': 'Название',
        'description': 'Описание',
        'key_skills': 'Навыки',
        'experience_id': 'Опыт работы',
        'premium': 'Премиум-вакансия',
        'employer_name': 'Компания',
        'salary_from': 'Нижняя граница вилки оклада',
        'salary_to': 'Верхняя граница вилки оклада',
        'salary_gross': 'Оклад указан до вычета налогов',
        'salary_currency': 'Идентификатор валюты оклада',
        'area_name': 'Название региона',
        'published_at': 'Дата и время публикации вакансии',
    }
    experience = {
        "noExperience": "Нет опыта",
        "between1And3": "От 1 года до 3 лет",
        "between3And6": "От 3 до 6 лет",
        "moreThan6": "Более 6 лет",
    }
    experience_to_num = {
        "noExperience": 0,
        "between1And3": 1,
        "between3And6": 3,
        "moreThan6": 6,
    }

    bools = {
        'True': 'Да',
        'False': 'Нет'
    }

    filter_table = {
        'Название': lambda f, d: f == d.name,
        'Компания': lambda f, d: f == d.employer_name,
        'Название региона': lambda f, d: f == d.area_name,
        'Премиум-вакансия': lambda f, d: f == DataSet.bools[d.premium],
        'Идентификатор валюты оклада': lambda f, d: f == d.salary.get_currency(),
        'Опыт работы': lambda f, d: f == DataSet.experience[d.experience_id],
        'Дата публикации вакансии': lambda f, d: f == datetime.strptime(d.published_at,
                                                                        '%Y-%m-%dT%H:%M:%S%z').strftime(
            '%d.%m.%Y'),
        'Навыки': lambda f, d: set(f.split(', ')).issubset(d.key_skills),
        'Оклад': lambda f, d: int(float(d.salary.salary_from)) <= int(f) <= int(float(d.salary.salary_to))
    }

    sort_table = {
        'Название': lambda d: d.name,
        'Компания': lambda d: d.employer_name,
        'Название региона': lambda d: d.area_name,
        'Премиум-вакансия': lambda d: DataSet.bools[d.premium],
        'Идентификатор валюты оклада': lambda d: d.salary.get_currency(),
        'Опыт работы': lambda d: DataSet.experience_to_num[d.experience_id],
        'Дата публикации вакансии': lambda d: datetime.strptime(d.published_at, '%Y-%m-%dT%H:%M:%S%z'),
        'Навыки': lambda d: len(d.key_skills),
        'Оклад': lambda d: d.salary.get_average_salary_rub()
    }

    format_table = {
        'Название': lambda row: row.name,
        'Описание': lambda row: row.description,
        'Навыки': lambda row: '\n'.join(row.key_skills),
        'Опыт работы': lambda row: row.experience_id,
        'Премиум-вакансия': lambda row: row.premium,
        'Компания': lambda row: row.employer_name,
        'Оклад': lambda row: row.salary.get_salary(),
        'Название региона': lambda row: row.area_name,
        'Дата публикации вакансии': lambda row: datetime.strptime(row.published_at, '%Y-%m-%dT%H:%M:%S%z').strftime(
            '%d.%m.%Y')
    }

    @staticmethod
    def csv_reader(file_name):
        file_csv = open(file_name, encoding='utf_8_sig')
        reader = csv.reader(file_csv)
        list_data = [i for i in reader]

        if len(list_data) == 0:
            print('Пустой файл')
            sys.exit()
        return list_data[0], [i for i in list_data[1:] if '' not in i and len(i) == len(list_data[0])]

    @staticmethod
    def create_vacancies_objects(file_name):
        headings, vacancies = DataSet.csv_reader(file_name)
        filtered_vacancies = DataSet.csv_filter(vacancies, headings)
        vacancies_objects = [Vacancy(vacancy['name'],
                                     vacancy['description'],
                                     [skill for skill in vacancy['key_skills'].split('; ')],
                                     vacancy['experience_id'],
                                     vacancy['premium'],
                                     vacancy['employer_name'],
                                     Salary(vacancy['salary_from'], vacancy['salary_to'],
                                            vacancy['salary_gross'], vacancy['salary_currency']),
                                     vacancy['area_name'],
                                     vacancy['published_at']
                                     ) for vacancy in filtered_vacancies]
        return vacancies_objects

    @staticmethod
    def csv_filter(reader, list_naming):
        return [{list_naming[i]: DataSet.process_vacancy(vacancy[i]) for i, v in enumerate(vacancy)} for vacancy in
                reader]

    @staticmethod
    def process_vacancy(vacancy):
        return ' '.join(('; '.join(re.sub(re.compile('<.*?>'), '', vacancy).split('\n')).split()))

    def filter_vacancies(self, filter_parameter):
        if filter_parameter == '':
            return self.vacancies_objects
        filter_parameter = filter_parameter.split(': ')
        field = filter_parameter[0] if len(filter_parameter) >= 1 else ''
        parameter = filter_parameter[1] if len(filter_parameter) == 2 else ''

        self.vacancies_objects = list(
            filter(lambda vacancy: DataSet.filter_table[field](parameter, vacancy), self.vacancies_objects))

        if not self.vacancies_objects:
            print('Ничего не найдено')
            sys.exit()

    def sort_vacancies(self, parameter, order):
        if parameter == '':
            return self.vacancies_objects
        if order == '':
            order = False

        order = order == 'Да'
        self.vacancies_objects.sort(key=DataSet.sort_table[parameter], reverse=order)

    def create_table(self):
        if len(self.vacancies_objects) == 0:
            print('Нет данных')
            sys.exit()

        table = PrettyTable()
        columns = ['№'] + list(DataSet.formatter(self.vacancies_objects[0]).keys())
        table.field_names = columns

        for index, vacancy in enumerate(self.vacancies_objects):
            formatted_vacancy = DataSet.formatter(vacancy)
            table.add_row([str(index + 1)] + list(DataSet.format_value(v) for v in formatted_vacancy.values()))

        table.max_width = 20
        table.align = 'l'
        table.hrules = True
        return table

    @staticmethod
    def formatter(row):
        return {k: DataSet.format_value(v(row)) for k, v in DataSet.format_table.items()}

    @staticmethod
    def print_table(table, vacancy_numbers, fields):
        vacancy_numbers = vacancy_numbers.split() if vacancy_numbers != '' else []
        fields = ['№'] + fields.split(', ') if fields != '' else table.field_names
        start = int(vacancy_numbers[0]) - 1 if len(vacancy_numbers) >= 1 else 0
        end = int(vacancy_numbers[1]) - 1 if len(vacancy_numbers) == 2 else len(table.rows)
        print(table.get_string(start=start, end=end, fields=fields))

    @staticmethod
    def format_value(value):
        for d in [DataSet.bools, DataSet.experience, Salary.currency]:
            value = d[value] if value in d else value
        return value if len(value) <= 100 else value[:100] + '...'

    def print_final_table(self, inputs):
        self.filter_vacancies(inputs.filter_parameter)
        self.sort_vacancies(inputs.sorting_parameter,
                            inputs.sorting_order)
        vacancy_table = self.create_table()
        DataSet.print_table(vacancy_table, inputs.numbers, inputs.cols)


class Interface:
    def __init__(self):
        inputs = Interface.check_inputs()
        self.file_name = inputs[0]
        self.filter_parameter = inputs[1]
        self.sorting_parameter = inputs[2]
        self.sorting_order = inputs[3]
        self.numbers = inputs[4]
        self.cols = inputs[5]

    @staticmethod
    def check_inputs():
        file_name = input('Введите название файла: ')
        filter_parameter = input('Введите параметр фильтрации: ')
        sorting_parameter = input('Введите параметр сортировки: ')
        sorting_order = input('Обратный порядок сортировки (Да / Нет): ')
        numbers = input('Введите диапазон вывода: ')
        cols = input('Введите требуемые столбцы: ')

        if filter_parameter != '' and ':' not in filter_parameter:
            print('Формат ввода некорректен')
            sys.exit()
        if filter_parameter != '' and filter_parameter.split(': ')[0] not in DataSet.filter_table.keys():
            print('Параметр поиска некорректен')
            sys.exit()
        if sorting_parameter != '' and sorting_parameter not in DataSet.sort_table.keys():
            print('Параметр сортировки некорректен')
            sys.exit()
        if sorting_order != '' and sorting_order != 'Да' and sorting_order != 'Нет':
            print('Порядок сортировки задан некорректно')
            sys.exit()
        return file_name, filter_parameter, sorting_parameter, sorting_order, numbers, cols


def get_table() :
    inputs = Interface()
    dataset = DataSet(inputs.file_name)
    dataset.print_final_table(inputs)