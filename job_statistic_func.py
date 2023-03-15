from terminaltables import AsciiTable


def predict_rub_salary(salary_from: int, salary_to: int = None) -> int:
    if salary_from and salary_to:
        return int((salary_from + salary_to) / 2)
    if salary_from:
        return int(salary_from * 1.2)
    if salary_to:
        return int(salary_to * 0.8)


def print_table(table_data, table_lines, title):
    for row in table_data:
        table_lines.append(
            [
                row['language'],
                row['vacancies_found'],
                row['vacancies_processed'],
                row['average_salary'],

            ]
        )
    table_instance = AsciiTable(table_lines, title)
    print(table_instance.table)
