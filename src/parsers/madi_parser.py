import csv
from io import StringIO

import requests


def get_direction_info(direction_number):
    url = f"https://pk.madi.ru/results/api.php?action=search&q={direction_number}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if not data.get("success") or not data.get("data", {}).get("groups"):
            return []

        results = []
        for group in data["data"]["groups"]:
            code = group.get("code", "")

            # Парсинг кода
            parts = code.split("_")
            if len(parts) >= 4:
                full_direction = parts[1]  # например "15.03.01"
                form_code = parts[2]  # З или О
                basis_code = parts[3]  # ПО или Б

                # Расшифровка формы обучения
                education_form = "Заочная" if form_code == "З" else "Очная" if form_code == "О" else form_code

                # Расшифровка основания обучения
                education_basis = "Платное" if basis_code == "ПО" else "Бюджетное" if basis_code == "Б" else basis_code

                results.append({
                    "full_direction": full_direction,
                    "education_form": education_form,
                    "education_basis": education_basis,
                    "code": code,
                    "direction_name": group.get("direction", ""),
                    "total_places": group.get("total_places", 0),
                    "applications_count": group.get("applications_count", 0)
                })

        return results

    except:
        return []


def run_analysis():
    results13 = get_direction_info('13.')
    results15 = get_direction_info('15.')
    results23 = get_direction_info('23.')
    result = ''
    result += "Группа 13:\n"
    result += "-" * 40 + '\n'
    sum = 0
    for i, info in enumerate(results13, 1):
        result += f"Код направления: {info['full_direction']}\n"
        result += f"Количество заявлений: {info['applications_count']}\n\n"
        sum += info['applications_count']
    result += f"\nВсего заявлений: {sum}\n\n"

    result += f"Группа 15:\n"
    result += "-" * 40 + '\n'
    sum = 0
    for i, info in enumerate(results15, 1):
        result += f"Код направления: {info['full_direction']}\n"
        result += f"Количество заявлений: {info['applications_count']}\n\n"
        sum += info['applications_count']
    result += f"\nВсего заявлений: {sum}\n"

    result += f"\nГруппа 23:\n"
    result += "-" * 40 + '\n'
    sum = 0
    for i, info in enumerate(results23, 1):
        result += f"Код направления: {info['full_direction']}\n"
        result += f"Количество заявлений: {info['applications_count']}\n\n"
        sum += info['applications_count']
    result += f"\nВсего заявлений: {sum}\n"
    return result

def export_to_csv(direction_number, filename=None):
    results = get_direction_info(direction_number)

    if not results:
        print(f"Направление {direction_number} не найдено")
        return

    if filename is None:
        filename = f"direction_{direction_number.replace('.', '')}.csv"

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['direction_name', 'full_direction', 'education_form', 'education_basis',
                      'total_places', 'applications_count', 'code']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(results)

    print(f"Данные экспортированы в файл: {filename}")


def get_csv_string(direction_number):
    results = get_direction_info(direction_number)

    if not results:
        return ""

    output = StringIO()
    fieldnames = ['direction_name', 'full_direction', 'education_form', 'education_basis',
                  'total_places', 'applications_count', 'code']
    writer = csv.DictWriter(output, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(results)

    return output.getvalue()


def check_student_enrollment(student_id):
    url = f"https://pk.madi.ru/results/api.php?action=search&q={student_id}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data.get("success") and data.get("data", {}).get("groups"):
            return True
        return False

    except:
        return False
