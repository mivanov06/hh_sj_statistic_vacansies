import requests
from progress.bar import IncrementalBar as Bar
from requests import exceptions

from job_statistic_func import predict_rub_salary


def hh_get_vacancies_count(text: str) -> int:
    response = hh_get_vacancies(text, per_page=1)
    return response['found']


def hh_get_vacancies(text: str, page: int = 0, per_page: int = 100, period: int = 30) -> list:
    api_url = 'https://api.hh.ru/vacancies'
    params = {
        'text': f'Программист {text}',
        'area': 1,
        'page': page,
        'per_page': per_page,
        'period': period
    }
    response = requests.get(api_url, params=params)
    response.raise_for_status()
    return response.json()


def hh_predict_rub_salary(vacance):
    if vacance['salary']:
        if vacance['salary']['currency'] == 'RUR':
            return predict_rub_salary(vacance['salary']['from'], vacance['salary']['to'])


def hh_get_vacance_statistic(language: str):
    global vacancies
    vacancies_found = hh_get_vacancies_count(language)
    pages_count = (vacancies_found // 100) + 1
    if pages_count > 19:
        pages_count = 19
    bar = Bar(f'for HH [{language}]: Counting in progress', max=vacancies_found)
    vacance_statistic = {
        'language': language,
        'vacancies_found': vacancies_found,
        'vacancies_processed': 0,
        'average_salary': 0
    }
    for page in range(pages_count + 1):
        try:
            vacancies = hh_get_vacancies(language, page)['items']
        except exceptions.HTTPError:
            print(f' Страница {page} не найдена')
        for vacance in vacancies:
            if vacance['salary']:
                rub_salary = hh_predict_rub_salary(vacance)
                if rub_salary:
                    vacance_statistic['average_salary'] += rub_salary
                    vacance_statistic['vacancies_processed'] += 1
            bar.next()
    bar.finish()
    if vacance_statistic['vacancies_processed'] != 0:
        vacance_statistic['average_salary'] = int(vacance_statistic['average_salary'] /
                                                  vacance_statistic['vacancies_processed'])
    return vacance_statistic
