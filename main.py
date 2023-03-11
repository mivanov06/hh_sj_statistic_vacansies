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


def hh_get_vacansies_info(vacancy_id: int):
    api = f'https://api.hh.ru/vacancies/{vacancy_id}'
    response = requests.get(api)
    response.raise_for_status()
    return response.json()


def predict_rub_salary(vacance):
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


def get_hh_vacansies_statistics(language: str):
    salary_count = 0
    salary_sum = 0
    vacancies_count = hh_get_vacancies_count(language)
    pages_count = (vacancies_count//100)+1
    bar = Bar(f'[{language}]: Counting in progress', max=vacancies_count)
    for page in range(pages_count+1):
        vacancies = hh_get_vacancies(language, page)['items']
        for vacance in vacancies:
            salary = vacance['salary']
            if salary is not None:
                rub_salary = predict_rub_salary(vacance)
                if rub_salary is not None:
                    salary_sum += rub_salary
                    salary_count += 1
            bar.next()
    bar.finish()
    return int(salary_sum/salary_count)


if __name__ == "__main__":
    languages = ['Python', 'Java', 'C++', 'PHP']
    salary_ranges = list()
    for language in languages:
        print('')
        salary_ranges.append({language, get_hh_vacansies_statistics(language)})
    for salary_range in salary_ranges:
        print(salary_range)


