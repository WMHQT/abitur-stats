import PyPDF2
import requests
import io
import re
from collections import Counter


def count_applications_by_direction(pdf_url):
    try:
        # Скачиваем PDF файл
        response = requests.get(pdf_url)
        response.raise_for_status()

        # Создаем объект PDF из скачанного контента
        pdf_file = io.BytesIO(response.content)
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        # Извлекаем текст из всех страниц
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()

        # Ищем все направления в тексте
        # Паттерн для поиска кодов направлений в формате XX.XX.XX
        pattern = r'(\d{2}\.\d{2}\.\d{2})\s*\([^)]+\)'
        matches = re.findall(pattern, text)

        # Подсчитываем количество заявлений по каждому направлению
        direction_counts = Counter(matches)

        # Выводим результаты
        print("Количество заявлений по направлениям:")
        print("-" * 40)
        for direction, count in sorted(direction_counts.items()):
            print(f"{direction}: {count}")

        return dict(direction_counts)

    except Exception as e:
        print(f"Ошибка при обработке PDF: {e}")
        return {}


def run_analysis():
    direction_counts = count_applications_by_direction("https://priem.bmstu.ru/lists/upload/registered/registered-first.pdf")
    result = ''
    result += "Группа 13:\n"
    result += "-" * 40 + '\n'
    filtered = {k: v for k, v in direction_counts.items() if k.startswith('13')}
    sum = 0
    for direction, count in sorted(filtered.items()):
        result += f"Код направления: {direction}\n"
        result += f"Количество заявлений: {count}\n\n"
        sum += count
    result += f"\nВсего заявлений: {sum}\n"

    result += f"\nГруппа 15:\n"
    result += "-" * 40 + '\n'
    filtered = {k: v for k, v in direction_counts.items() if k.startswith('15')}
    sum = 0
    for direction, count in sorted(filtered.items()):
        result += f"Код направления: {direction}\n"
        result += f"Количество заявлений: {count}\n\n"
        sum += count
    result += f"\nВсего заявлений: {sum}\n"

    result += f"\nГруппа 23:\n"
    result += "-" * 40 + '\n'
    filtered = {k: v for k, v in direction_counts.items() if k.startswith('23')}
    sum = 0
    for direction, count in sorted(filtered.items()):
        result += f"Код направления: {direction}\n"
        result += f"Количество заявлений: {count}\n\n"
        sum += count
    result += f"\nВсего заявлений: {sum}\n"
    return result
