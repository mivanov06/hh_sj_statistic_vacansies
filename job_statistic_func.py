from terminaltables import AsciiTable


def predict_rub_salary(salary_from: int, salary_to: int = None) -> int:
    if salary_from and salary_to:
        return int((salary_from + salary_to) / 2)
    if salary_from:
        return int(salary_from * 1.2)
    if salary_to:
        return int(salary_to * 0.8)


def get_table(table_content, table_row, title):
    for row in table_content:
        table_row.append(
            [
                row['language'],
                row['vacancies_found'],
                row['vacancies_processed'],
                row['average_salary'],

            ]
        )
    return AsciiTable(table_row, title).table
