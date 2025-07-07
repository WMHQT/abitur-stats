import io
import re

import PyPDF2
import requests


def check_student_in_pdf(pdf_url, student_id):
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

        # Ищем студента по номеру в тексте
        # Используем регулярное выражение для поиска номера студента
        pattern = rf'\b{re.escape(str(student_id))}\b'

        return bool(re.search(pattern, text))

    except Exception as e:
        print(f"Ошибка при обработке PDF: {e}")
        return False

# Пример использования
result = check_student_in_pdf("https://priem.bmstu.ru/lists/upload/registered/registered-first.pdf", "3560638")
print(result)