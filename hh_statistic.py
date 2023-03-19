import logging
import requests
from itertools import count

from job_statistic_func import predict_rub_salary

logger = logging.getLogger(__file__)


def hh_get_vacancies(text: str, page: int = 0, per_page: int = 100, period: int = 30) -> list:
    api_url = 'https://api.hh.ru/vacancies'
    moscow_id = 1
    params = {
        'text': f'Программист {text}',
        'area': moscow_id,
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
    vacancies_statistic = {
        'language': language,
        'vacancies_processed': 0,
        'average_salary': 0
    }
    logger.info(f'{language}. Calculation of vacancies for HeadHunter')
    for page in count(0):
        try:
            vacancies_page = hh_get_vacancies(language, page, 100)
        except requests.exceptions.HTTPError:
            logger.error(f'Page {page} not found')
        if page > (vacancies_page['found'] // 100):
            break
        vacancies = vacancies_page['items']
        for vacancy in vacancies:
            rub_salary = hh_predict_rub_salary(vacancy)
            if rub_salary:
                vacancies_statistic['average_salary'] += rub_salary
                vacancies_statistic['vacancies_processed'] += 1
    vacancies_statistic['vacancies_found'] = vacancies_page['found']
    if vacancies_statistic['vacancies_processed']:
        vacancies_statistic['average_salary'] = int(vacancies_statistic['average_salary'] /
                                                    vacancies_statistic['vacancies_processed'])
    return vacancies_statistic
