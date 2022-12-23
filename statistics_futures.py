import concurrent.futures
import divide_csv_file
import statistics_pandas
import currencies


def get_statistics(file_name, vacancy):
    salary_info_file = 'salary_info.csv'
    currencies.convert_salary_to_rub(file_name).to_csv(salary_info_file)
    years = divide_csv_file.divide_file_by_year(salary_info_file)
    return_dict = {}
    file_years = [rf'csv_files\year_{year}.csv' for year in years]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        [executor.submit(statistics_pandas.get_main_statistics, file, vacancy, return_dict) for file in
                   file_years]

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

    salary_level_by_city, share_of_vacancies = statistics_pandas.get_city_statistics(salary_info_file)

    print('Динамика уровня зарплат по годам:', salary_level)
    print('Динамика количества вакансий по годам:', number_of_vacancies)
    print('Динамика уровня зарплат по годам для выбранной профессии:', salary_level_by_profession)
    print('Динамика количества вакансий по годам для выбранной профессии:', number_of_vacancies_by_profession)
    print('Уровень зарплат по городам (в порядке убывания):', salary_level_by_city)
    print('Доля вакансий по городам (в порядке убывания):', share_of_vacancies)

    return salary_level, number_of_vacancies, salary_level_by_profession, number_of_vacancies_by_profession, salary_level_by_city, share_of_vacancies

def get_statistics_by_city(file_name, vacancy, city):
    salary_info_file = 'salary_info.csv'
    currencies.convert_salary_to_rub(file_name).to_csv(salary_info_file)
    years = divide_csv_file.divide_file_by_year(salary_info_file)
    return_dict = {}
    file_years = [rf'csv_files\year_{year}.csv' for year in years]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        [executor.submit(statistics_pandas.get_main_statistics_by_city, file, vacancy, city, return_dict) for file in
                   file_years]

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

    salary_level_by_city, share_of_vacancies = statistics_pandas.get_city_statistics(salary_info_file)

    print('Динамика уровня зарплат по годам и региону:', salary_level)
    print('Динамика количества вакансий по годам и региону:', number_of_vacancies)
    print('Динамика уровня зарплат по годам для выбранной профессии и региона:', salary_level_by_profession)
    print('Динамика количества вакансий по годам для выбранной профессии и региона:', number_of_vacancies_by_profession)
    print('Уровень зарплат по городам (в порядке убывания):', salary_level_by_city)
    print('Доля вакансий по городам (в порядке убывания):', share_of_vacancies)

    return salary_level, number_of_vacancies, salary_level_by_profession, number_of_vacancies_by_profession, salary_level_by_city, share_of_vacancies

