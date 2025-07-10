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


def run_analysis(prefix):
    direction_counts = count_applications_by_direction("https://priem.bmstu.ru/lists/upload/registered/registered-first.pdf")

    print(f"\nГруппа 13:")
    print("-" * 40)
    filtered = {k: v for k, v in direction_counts.items() if k.startswith('13')}
    sum = 0
    for direction, count in sorted(filtered.items()):
        print(f"Код направления: {direction}")
        print(f"Количество заявлений: {count}\n")
        sum += count
    print(f"\nВсего заявлений: {sum}")

    print(f"\nГруппа 15:")
    print("-" * 40)
    filtered = {k: v for k, v in direction_counts.items() if k.startswith('15')}
    sum = 0
    for direction, count in sorted(filtered.items()):
        print(f"Код направления: {direction}")
        print(f"Количество заявлений: {count}\n")
        sum += count
    print(f"\nВсего заявлений: {sum}")

    print(f"\nГруппа 23:")
    print("-" * 40)
    filtered = {k: v for k, v in direction_counts.items() if k.startswith('23')}
    sum = 0
    for direction, count in sorted(filtered.items()):
        print(f"Код направления: {direction}")
        print(f"Количество заявлений: {count}\n")
        sum += count
    print(f"\nВсего заявлений: {sum}")
    # return filtered


# Пример использования

# Пример использования
# results = count_applications_by_direction("https://example.com/students.pdf")
results = count_applications_by_direction("https://priem.bmstu.ru/lists/upload/registered/registered-first.pdf")
filter_by_prefix(results, "15")
# print(results)
