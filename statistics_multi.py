import multiprocessing

import divide_csv_file
import statistics_pandas
from multiprocessing import Process, Pool

file_name = input('Введите название файла:')
vacancy = input('Введите название профессии:')
# file_name = 'vacancies_by_year.csv'
# vacancy = 'Аналитик'
years = divide_csv_file.divide_file_by_year(file_name)

if __name__ == '__main__':
    manager = multiprocessing.Manager()
    return_dict = manager.dict()
    processes = [Process(target=statistics_pandas.get_main_statistics,
                         args=(rf'csv_files\year_{year}.csv', vacancy, return_dict)) for year in years]

    for process in processes:
        process.start()
    for process in processes:
        process.join()

    salary_level = {}
    number_of_vacancies = {}
    salary_level_by_profession = {}
    number_of_vacancies_by_profession = {}
    salary_level_by_city = {}
    share_of_vacancies = {}

    return_dict = dict(sorted(return_dict.items(), key=lambda x: x[0]))

    for year in return_dict.keys():
        salary_level[year] = return_dict[year][0]
        number_of_vacancies[year] = return_dict[year][1]
        salary_level_by_profession[year] = return_dict[year][2]
        number_of_vacancies_by_profession[year] = return_dict[year][3]

    salary_level_by_city, share_of_vacancies = statistics_pandas.get_city_statistics(file_name)

    print('Динамика уровня зарплат по годам:', salary_level)
    print('Динамика количества вакансий по годам:', number_of_vacancies)
    print('Динамика уровня зарплат по годам для выбранной профессии:', salary_level_by_profession)
    print('Динамика количества вакансий по годам для выбранной профессии:', number_of_vacancies_by_profession)
    print('Уровень зарплат по городам (в порядке убывания):', salary_level_by_city)
    print('Доля вакансий по городам (в порядке убывания):', share_of_vacancies)
