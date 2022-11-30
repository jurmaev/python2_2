from unittest import TestCase
from table import Salary, DataSet, Vacancy

class SalaryTests(TestCase):
    def test_get_salary(self):
        self.assertEqual(Salary('1000', '2000', 'False', 'USD').get_salary(), '1 000 - 2 000 (Доллары) (С вычетом налогов)')

    def test_get_average_salary_rub(self):
        self.assertEqual(Salary('1010', '3500', 'True', 'EUR').get_average_salary_rub(), 135074.5)

class DatasetTests(TestCase):
    def test_process_vacancy(self):
        self.assertEqual(DataSet.process_vacancy('Основные функции:</strong></p> <ul> <li>мониторинг состояния промышленных кластеров СУБД'), 'Основные функции: мониторинг состояния промышленных кластеров СУБД')

    def test_formatter(self):
        self.assertEqual(DataSet.formatter(Vacancy('Программист', 'Хорошая вакансия', ['Знание алгоритмов', 'Работа с Git'], 'noExperience', 'Да', 'Контур', Salary('10000', '15000', 'False', 'RUR'),'Челябинск', '2022-07-13T11:03:58+0300')),
                         {'Название': 'Программист', 'Описание': 'Хорошая вакансия', 'Навыки': 'Знание алгоритмов\nРабота с Git', 'Опыт работы': 'Нет опыта', 'Премиум-вакансия': 'Да', 'Компания': 'Контур', 'Оклад': '10 000 - 15 000 (Рубли) (С вычетом налогов)', 'Название региона': 'Челябинск', 'Дата публикации вакансии': '13.07.2022'})

    def test_format_value(self):
        self.assertEqual(DataSet.format_value('ЕвроХим - один из крупнейших и наиболее быстро развивающихся производителей минеральных удобрений в мире. Наша цель – войти в пятерку лидеров отрасли.'), 'ЕвроХим - один из крупнейших и наиболее быстро развивающихся производителей минеральных удобрений в ...')
