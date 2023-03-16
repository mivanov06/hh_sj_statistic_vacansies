from typing import Dict

import requests
from progress.bar import IncrementalBar as Bar
from requests import exceptions

from job_statistic_func import predict_rub_salary


def sj_get_vacancies_count(text: str, secret_key: str) -> int:
    response = sj_get_vacancies(text, secret_key, per_page=1)
    return response['total']


def sj_get_vacancies(text: str, secret_key: str, page: int = 0, per_page: int = 100, period: int = 30) -> list:
    api_url = 'https://api.superjob.ru/2.0/vacancies/'
    headers = {
        'X-Api-App-Id': secret_key
    }
    params = {
        'page': page,
        'count': per_page,
        'keyword': f'программист {text}',
        'town': 'Москва',
        'period': period
    }
    response = requests.get(api_url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()


def sj_predict_rub_salary(vacance) -> int:
    if vacance['currency'] and vacance['currency'] == 'rub':
        return predict_rub_salary(vacance['payment_from'], vacance['payment_to'])


def sj_get_vacance_statistic(language: str, secret_key: str) -> dict[str, int | str]:
    vacancies_found = sj_get_vacancies_count(language, secret_key)
    pages_count = (vacancies_found // 100) + 1
    bar = Bar(f'for SJ [{language}]: Counting in progress', max=vacancies_found)
    vacance_statistic = {
        'language': language,
        'vacancies_found': vacancies_found,
        'vacancies_processed': 0,
        'average_salary': 0
    }
    for page in range(pages_count + 1):
        try:
            vacancies = sj_get_vacancies(language, secret_key, page, 100)['objects']
        except exceptions.HTTPError:
            print(f' Страница {page} не найдена')
        for vacance in vacancies:
            rub_salary = sj_predict_rub_salary(vacance)
            if rub_salary:
                vacance_statistic['average_salary'] += rub_salary
                vacance_statistic['vacancies_processed'] += 1
            bar.next()
    bar.finish()
    if vacance_statistic['vacancies_processed'] != 0:
        vacance_statistic['average_salary'] = int(vacance_statistic['average_salary'] /
                                                  vacance_statistic['vacancies_processed'])
    return vacance_statistic
