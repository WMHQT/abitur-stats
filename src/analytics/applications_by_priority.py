import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO

from utils.load_csv import load_csv


def save_infographic() -> BytesIO:
    """Saves infographic in binary format to buffer."""

    buff = BytesIO()
    plt.savefig(buff, format='png', dpi=300, bbox_inches='tight')
    plt.close()
    buff.seek(0)
    return buff


def infographic_output(priority_counts: pd.DataFrame) -> None:
    """Creates infrographic from data."""
    
    plt.figure(figsize=(10, 6))
    priority_counts.plot(kind='bar', color='skyblue', edgecolor='black')
    plt.title('Распределение заявлений по приоритетам')
    plt.xlabel('Приоритет')
    plt.ylabel('Количество заявлений')
    plt.xticks(rotation=0)
    plt.grid(axis='y', linestyle='--', alpha=0.7)


def save_image(image_buffer, file_path: str) -> None:
    image_buffer.seek(0)
    with open(file_path, 'wb') as f:
        f.write(image_buffer.getvalue()) 


def text_output(priority_counts: pd.DataFrame) -> str:
    """Creates text table from data."""
    
    output = []
    output.append(f"{'Приоритет':<12} {'Количество заявлений':<20}")  # Header
    output.append("-" * 32)  # Separator line

    for priority in range(1, 26):
        count = priority_counts.get(priority, 0)
        output.append(f"{priority:<12} {count:<20}")  # Formatted row

    return "\n".join(output)


def analyze_priority(file_path: str) -> pd.DataFrame:
    df = load_csv(file_path)

    # Фильтрация записей с приоритетами 1–25
    valid_priorities = df[df['Приоритет'].isin(range(1, 26))]

    # Подсчет количества заявлений по приоритетам
    priority_counts = valid_priorities['Приоритет'].value_counts().sort_index()

    return priority_counts


def run_analysis(file_path: str) -> tuple[str, BytesIO]:
    priority_counts = analyze_priority(file_path)
    
    text = text_output(priority_counts)
    infographic_output(priority_counts)
    image_buffer = save_infographic()

    return text, image_buffer