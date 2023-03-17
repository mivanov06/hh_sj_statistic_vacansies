import os
from dotenv import load_dotenv
import logging

from hh_statistic import hh_get_vacancy_statistic
from sj_statistic import sj_get_vacancy_statistic
from job_statistic_func import get_table

logger = logging.getLogger(__file__)

if __name__ == "__main__":
    load_dotenv()
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    logger.setLevel(logging.INFO)
    languages = ['Python']
    # languages = ['Python', 'Java', 'C++', 'C#', 'C', 'PHP', 'Go', 'Ruby', 'JavaScript', 'TypeScript']
    sj_key = os.getenv('SJ_SECRET_KEY')
    hh_salary_ranges, sj_salary_ranges = [], []
    table_lines = [
        ['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']
    ]
    for language in languages:
        hh_salary_ranges.append(hh_get_vacancy_statistic(language))
        sj_salary_ranges.append(sj_get_vacancy_statistic(language, sj_key))
    print(get_table(hh_salary_ranges, table_lines.copy(), 'Статистика HeadHunter'))
    print(get_table(sj_salary_ranges, table_lines.copy(), 'Статистика SuperJob'))
