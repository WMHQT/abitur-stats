from collections import Counter
import requests


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


def count_applications_by_direction(direction_prefix: str) -> dict:
    """
    Получает количество заявлений по направлениям,
    соответствующим префиксу (например, '13.'), через API МАДИ.
    """
    url = f"https://pk.madi.ru/results/api.php?action=search&q={direction_prefix}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if not data.get("success") or not data.get("data", {}).get("groups"):
            return {}

        direction_counts = Counter()

        for group in data["data"]["groups"]:
            code = group.get("code", "")
            parts = code.split("_")
            if len(parts) >= 4:
                full_direction = parts[1]
                applications_count = int(group.get("applications_count", 0))
                direction_counts[full_direction] += applications_count

        return dict(direction_counts)

    except Exception as e:
        print(f"Ошибка при получении данных: {e}")
        return {}


def group_directions_by_prefix(direction_counts: dict, prefix: str) -> tuple[dict, int]:
    """Группирует направления по префиксу и считает общее количество заявлений."""
    
    filtered = {k: v for k, v in direction_counts.items() if k.startswith(prefix)}
    total = sum(filtered.values())
    return filtered, total


def generate_group_output(group_name: str, directions: dict, total: int) -> list[str]:
    """Формирует текстовый отчет для группы направлений."""
    
    output = [f"Группа направлений: {group_name}"]

    for direction, count in sorted(directions.items()):
        if direction in FACULTY_CODES_SHORT:
            output.append(f"\nКод направления: {direction}")
            output.append(f"Количество заявлений: {count}")
    if len(output) == 1:
        output.append("\nНет аналогичных направлений.") 
    # output.append(f"\nВсего заявлений: {total}")
    output.append("—" * 12)

    return output


def run_analysis() -> str:
    """Основной метод анализа заявок через API МАДИ."""
    
    groups = ["01", "13", "15", "23", "54"]
    output = []

    for group in groups:
        direction_counts = count_applications_by_direction(f"{group}.")
        directions, total = group_directions_by_prefix(direction_counts, group)
        print(directions, total)
        output.extend(generate_group_output(group, directions, total))

    return "\n".join(output)