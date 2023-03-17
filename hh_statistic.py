from itertools import count

import requests
import logging

from job_statistic_func import predict_rub_salary


def hh_get_vacancies(text: str, page: int = 0, per_page: int = 100, period: int = 30) -> list:
    api_url = 'https://api.hh.ru/vacancies'
    MOSCOW = 1
    params = {
        'text': f'Программист {text}',
        'area': MOSCOW,
        'page': page,
        'per_page': per_page,
        'period': period
    }
    response = requests.get(api_url, params=params)
    response.raise_for_status()
    return response.json()


def hh_predict_rub_salary(vacancy):
    if vacancy['salary'] and vacancy['salary']['currency'] == 'RUR':
        return predict_rub_salary(vacancy['salary']['from'], vacancy['salary']['to'])


def hh_get_vacancy_statistic(language: str) -> dict[str, int | str]:
    vacancy_statistic = {
        'language': language,
        'vacancies_processed': 0,
        'average_salary': 0
    }
    logging.basicConfig(level=logging.INFO,  format="%(message)s")
    logging.info(f'{language}. Calculation of vacancies for HeadHunter')
    for page in count(0):
        try:
            vacancies_page = hh_get_vacancies(language, page, 100)
        except requests.exceptions.HTTPError:
            logging.error(f'Page {page} not found')
        if vacancies_page['found']:
            vacancy_statistic['vacancies_found'] = vacancies_page['found']
        if page > (vacancy_statistic['vacancies_found'] // 100):
            break
        vacancies = vacancies_page['items']
        for vacancy in vacancies:
            if vacancy['salary'] and hh_predict_rub_salary(vacancy):
                vacancy_statistic['average_salary'] += hh_predict_rub_salary(vacancy)
                vacancy_statistic['vacancies_processed'] += 1
    try:
        vacancy_statistic['average_salary'] = int(vacancy_statistic['average_salary'] /
                                                  vacancy_statistic['vacancies_processed'])
    except ZeroDivisionError:
        vacancy_statistic['average_salary'] = 0
    return vacancy_statistic
