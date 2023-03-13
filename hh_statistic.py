import requests
from progress.bar import IncrementalBar as Bar


def hh_get_vacancies_count(text: str):
    result = hh_get_vacancies(text, per_page=1)
    return result['found']


def hh_get_vacancies(text: str, page: int = 0, per_page: int = 100):
    api_url = 'https://api.hh.ru/vacancies'
    params = {
        'text': f'NAME:{text}',
        'area': 1,
        'page': page,
        'per_page': per_page

    }
    response = requests.get(api_url, params=params)
    response.raise_for_status()
    return response.json()


def predict_rub_salary_for_hh(vacance):
    salary = vacance['salary']
    if salary is not None:
        if salary['currency'] == 'RUR':
            if salary['from'] is not None:
                if salary['to'] is not None:
                    return int((salary['from'] + salary['to']) / 2)
                else:
                    return int(salary['from'] * 1.2)
            else:
                return int(salary['to'] * 0.8)
    return None


def hh_get_vacance_statistic(language: str):
    vacancies_found = hh_get_vacancies_count(language)
    pages_count = (vacancies_found // 100) + 1
    bar = Bar(f'[{language}]: Counting in progress', max=vacancies_found)
    vacance_statistic = {
        language: {
            'vacancies_found': vacancies_found,
            'vacancies_processed': 0,
            'average_salary': 0
        }
    }
    for page in range(pages_count + 1):
        vacancies = hh_get_vacancies(language, page)['items']
        for vacance in vacancies:
            salary = vacance['salary']
            if salary is not None:
                rub_salary = predict_rub_salary_for_hh(vacance)
                if rub_salary is not None:
                    vacance_statistic[language]['average_salary'] += rub_salary
                    vacance_statistic[language]['vacancies_processed'] += 1
            bar.next()
    bar.finish()
    if vacance_statistic[language]['vacancies_processed'] != 0:
        vacance_statistic[language]['average_salary'] = int(vacance_statistic[language]['average_salary'] /
                                                            vacance_statistic[language]['vacancies_processed'])
    return vacance_statistic