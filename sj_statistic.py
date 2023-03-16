from itertools import count
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


def sj_get_vacancy_statistic(language: str, secret_key: str):  # dict[str, int | str]
    vacancy_statistic = {
        'language': language,
        'vacancies_processed': 0,
        'average_salary': 0
    }
    for page in count(0):
        try:
            vacancies_page = sj_get_vacancies(language, secret_key, page, 100)
        except exceptions.HTTPError:
            print(f' Страница {page} не найдена')
            continue
        if vacancies_page['total']:
            vacancy_statistic['vacancies_found'] = vacancies_page['total']
        if page >= (vacancy_statistic['vacancies_found'] // 100):
            break
        vacancies = vacancies_page['objects']
        for vacancy in vacancies:
            rub_salary = sj_predict_rub_salary(vacancy)
            if rub_salary:
                vacancy_statistic['average_salary'] += rub_salary
                vacancy_statistic['vacancies_processed'] += 1
        vacancy_statistic['average_salary'] = int(vacancy_statistic['average_salary'] /
                                                  vacancy_statistic['vacancies_processed'])
    return vacancy_statistic
