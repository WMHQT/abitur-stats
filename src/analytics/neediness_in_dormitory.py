import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from utils.load_csv import load_csv


def infographic_output(counts):
    # Подготовка данных для инфографики
    labels = ['Приоритет 1', 'Приоритет 2']
    dorm_needed = counts.get('нужд.', pd.Series(0))[[1, 2]].values
    dorm_not_needed = counts.get('не нужд.', pd.Series(0))[[1, 2]].values

    # Настройка гистограммы
    x = np.arange(len(labels))
    width = 0.35

    fig, ax = plt.subplots(figsize=(8, 6))
    bars1 = ax.bar(x - width/2, dorm_needed, width, label='Нуждаются в общежитии', color='skyblue')
    bars2 = ax.bar(x + width/2, dorm_not_needed, width, label='Не нуждаются в общежитии', color='lightcoral')

    # Настройка осей и заголовка
    ax.set_xlabel('Приоритет')
    ax.set_ylabel('Количество заявлений')
    ax.set_title('Разбивка заявлений по приоритетам и необходимости общежития')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    # Добавление значений над столбцами
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height, f'{int(height)}',
                    ha='center', va='bottom')

    # Сохранение графика
    image_path = 'dorm_priority_distribution.png'
    plt.savefig(image_path, dpi=300, bbox_inches='tight')
    plt.close()


def text_output(counts: pd.DataFrame) -> str:
    """Creates text table from data."""
    
    output = []
    output.append(f"{'Приоритет':<12} {'Нуждаются':<20} {'Не нуждаются':<20}")  # Header
    output.append("-" * 52)  # Separator line

    for priority in [1, 2]:
        needed_count = counts.get('нужд.', pd.Series(0)).get(priority, 0)
        not_needed_count = counts.get('не нужд.', pd.Series(0)).get(priority, 0)
        output.append(f"{priority:<12} {needed_count:<20} {not_needed_count:<20}")

    return "\n".join(output)


def analyze_dormitory(file_path: str) -> pd.DataFrame:
    df = load_csv(file_path)

    # Фильтрация записей с приоритетами 1 и 2
    valid_priorities = df[df['Приоритет'].isin([1, 2])]

    # Группировка по приоритетам и необходимости общежития
    counts = valid_priorities.groupby(['Приоритет', 'Общежитие']).size().unstack(fill_value=0)
    
    return counts


if __name__ == "__main__":
    counts = analyze_dormitory('data/csv/mpu/01.03.02.csv')
    infographic_output(counts)
    text = text_output(counts)
    print(text)
