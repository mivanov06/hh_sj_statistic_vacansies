import os
from dotenv import load_dotenv

from hh_statistic import hh_get_vacancy_statistic
from job_statistic_func import print_table
from sj_statistic import sj_get_vacancy_statistic


if __name__ == "__main__":
    load_dotenv()
    languages = ['Python']
    # languages = ['Python', 'Java', 'C++', 'C#', 'C',
    #              'PHP', 'Go', 'Ruby', 'JavaScript', 'TypeScript']
    sj_key = os.getenv('SJ_SECRET_KEY')
    hh_salary_ranges, sj_salary_ranges = [], []
    table_lines = [
        ['Язык программирования', 'Вакансий найдено', 'Вакансий обработано',
         'Средняя зарплата']
    ]
    for language in languages:
        # hh_salary_ranges.append(hh_get_vacancy_statistic(language))
        sj_salary_ranges.append(sj_get_vacancy_statistic(language, sj_key))
    print_table(hh_salary_ranges, table_lines.copy(), 'Статистика HeadHunter')
    print_table(sj_salary_ranges, table_lines.copy(), 'Статистика SuperJob')
