from collections import Counter
import re
import requests
import PyPDF2
import io


FACULTY_CODES_SHORT = {
    '01.03.02': 'Прикладная математика и информатика',
    '13.03.02': 'Электроэнергетика и электротехника', 
    '13.03.03': 'Энергетическое машиностроение',
    '15.03.03': 'Прикладная механика',
    '23.03.02': 'Наземные транспортно-технологические комплексы',
    '23.03.03': 'Инжиниринг и эксплуатация транспортных систем',
    '23.05.01': 'Наземные транспортно-технологические средства',
    '54.03.01': 'Транспортный и промышленный дизайн',
}


def count_applications_by_direction(pdf_url: str) -> dict:
    """Извлекает количество заявлений по каждому направлению из PDF."""
    try:
        response = requests.get(pdf_url)
        response.raise_for_status()

        pdf_file = io.BytesIO(response.content)
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()

        # Поиск всех кодов направлений формата XX.XX.XX
        pattern = r'(\d{2}\.\d{2}\.\d{2})\s*\([^)]+\)'
        matches = re.findall(pattern, text)

        direction_counts = Counter(matches)

        return dict(direction_counts)

    except Exception as e:
        print(f"Ошибка при обработке PDF: {e}")
        return {}


def group_directions_by_prefix(direction_counts: dict, prefix: str) -> tuple[dict, int]:
    """Группирует направления по префиксу и считает общее количество заявлений."""
    filtered = {k: v for k, v in direction_counts.items() if k.startswith(prefix)}
    total = sum(filtered.values())
    return filtered, total


def generate_group_output(group_name: str, directions: dict, total: int) -> list[str]:
    """Формирует текстовый отчет для группы направлений."""
    output = [f"Группа направлений: {group_name}",]

    for direction, count in sorted(directions.items()):
        if direction in FACULTY_CODES_SHORT:
            output.append(f"\nКод направления: {direction}")
            output.append(f"Количество заявлений: {count}")

    # output.append(f"\nВсего заявлений: {total}")
    output.append("—" * 12)

    return output


def run_analysis() -> str:
    """Основной метод анализа PDF файла с заявлениями."""

    pdf_url = "https://priem.bmstu.ru/lists/upload/registered/registered-first.pdf"
    direction_counts = count_applications_by_direction(pdf_url)

    # Группы для анализа
    groups = ["01", "13", "15", "23", "54"]

    output = []

    for group in groups:
        directions, total = group_directions_by_prefix(direction_counts, group)
        output.extend(generate_group_output(group, directions, total))

    return "\n".join(output)