import requests
import logging

from itertools import count

from job_statistic_func import predict_rub_salary


def sj_get_vacancies(text: str, secret_key: str, page: int = 0, per_page: int = 100, period: int = 30) -> list:
    api_url = 'https://api.superjob.ru/2.0/vacancies/'
    town = 'Москва'
    headers = {
        'X-Api-App-Id': secret_key
    }
    params = {
        'page': page,
        'count': per_page,
        'keyword': f'программист {text}',
        'town': town,
        'period': period
    }
    response = requests.get(api_url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()


def sj_predict_rub_salary(vacancy) -> int:
    if vacancy['currency'] and vacancy['currency'] == 'rub':
        return predict_rub_salary(vacancy['payment_from'], vacancy['payment_to'])


def sj_get_vacancy_statistic(language: str, secret_key: str) -> dict[str, int | str]:
    vacancies_statistic = {
        'language': language,
        'vacancies_processed': 0,
        'average_salary': 0,
        'total': 0
    }
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    logging.info(f'{language}. Calculation of vacancies for SuperJob')
    for page in count(0):
        try:
            vacancies_page = sj_get_vacancies(language, secret_key, page, 100)
        except requests.exceptions.HTTPError:
            logging.error(f'Page {page} not found')
        if page > (vacancies_page['total'] // 100):
            break
        vacancies = vacancies_page['objects']
        for vacancy in vacancies:
            rub_salary = sj_predict_rub_salary(vacancy)
            if rub_salary:
                vacancies_statistic['average_salary'] += rub_salary
                vacancies_statistic['vacancies_processed'] += 1
    vacancies_statistic['vacancies_found'] = vacancies_page['total']
    if vacancies_statistic['vacancies_processed'] is not None:
        vacancies_statistic['average_salary'] = int(vacancies_statistic['average_salary'] /
                                                    vacancies_statistic['vacancies_processed'])
    return vacancies_statistic
