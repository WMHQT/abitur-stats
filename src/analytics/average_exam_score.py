from utils.load_csv import load_csv


def text_output(data: list[tuple[int, float]]) -> str:
    """Creates text table from data."""

    output = []
    output.append(f"{'Приоритет':<12} {'Средний балл ЕГЭ':<20} {'Количество заявлений':<20}")  # Header
    output.append("-" * 52)  # Separator line

    for i, (count, average_score) in enumerate(data, start=1):
        output.append(f"{i:<12} {average_score:<20.2f} {count:<20}")  # Formatted row

    return "\n".join(output)


def analyze_exam_score(file_path: str) -> list[tuple[int, float]]:
    df = load_csv(file_path)

    # Фильтрация записей с приоритетами 1 и 2
    priority_1 = df[df['Приоритет'] == 1]
    priority_2 = df[df['Приоритет'] == 2]

    # Вычисление среднего балла ЕГЭ и количества заявлений
    mean_score_1 = priority_1['Суммабаллов попредметам'].mean()
    count_1 = priority_1['Суммабаллов попредметам'].count()
    
    mean_score_2 = priority_2['Суммабаллов попредметам'].mean()
    count_2 = priority_2['Суммабаллов попредметам'].count()

    return [(count_1, mean_score_1), (count_2, mean_score_2)]


if __name__ == "__main__":
    data = analyze_exam_score('data/csv/mpu/01.03.02.csv')
    text = text_output(data)
    print(text)