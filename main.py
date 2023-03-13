import os

import requests
from progress.bar import IncrementalBar as Bar
from pprint import pprint

from dotenv import load_dotenv
from hh_statistic import hh_get_vacance_statistic





def predict_rub_salary_for_superJob(vacance):
    if vacance['currency'] is not None and vacance['currency'] == 'rub':
        if vacance['payment_from'] != 0:
            if vacance['payment_to'] != 0:
                return int((vacance['payment_from'] + vacance['payment_to']) / 2)
            else:
                return int(vacance['payment_from'] * 1.2)
        else:
            return int(vacance['payment_to'] * 0.8)



if __name__ == "__main__":
    load_dotenv()
    # languages = ['Python', 'Java', 'C++', 'PHP', 'Go', 'Ruby', 'JavaScript']
    # # languages = ['Python']
    # salary_ranges = list()
    # for language in languages:
    #     print('')
    #     salary_ranges.append(hh_get_vacance_statistic(language))
    # for salary_range in salary_ranges:
    #     print(salary_range)

    sj_key = os.getenv('SJ_SECRET_KEY')
    url = 'https://api.superjob.ru/2.0/vacancies/'
    headers = {
        'X-Api-App-Id': sj_key
    }
    params = {
        'keyword': 'Программист',
        'town': 'Москва'
    }
    response = requests.get(url, headers=headers, params=params)

    vacancies = response.json()['objects']
    for number, vacance in enumerate(vacancies):
        print(f"{number} - {vacance['profession']} - {vacance['town']['title']} - {vacance['payment_from']} - {vacance['payment_to']}"
              f"- {predict_rub_salary_for_superJob(vacance)} - {vacance['currency']}")
