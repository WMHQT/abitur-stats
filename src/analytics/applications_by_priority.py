import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO

from utils.load_csv import load_csv

MAX_PRIORITY = 10


def save_infographic() -> BytesIO:
    """Saves infographic in binary format to buffer."""

    buff = BytesIO()
    plt.savefig(buff, format='png', dpi=300, bbox_inches='tight')
    plt.close()
    buff.seek(0)
    return buff


def infographic_output(priority_counts: pd.DataFrame, specialization: str) -> None:
    """Creates infographic from data, with each bar split by study type."""
    
    # Extract budget and paid values using correct column names
    budget_values = priority_counts['Бюджетная']
    paid_values = priority_counts['Платная']

    fig, ax = plt.subplots(figsize=(12, 7))

    # Plot the bottom part of each bar ("Бюджет")
    bars_budget = ax.bar(priority_counts.index, budget_values, color='skyblue', edgecolor='black', label='Бюджет')

    # Plot the top part of each bar ("Платная"), stacked on top
    bars_paid = ax.bar(priority_counts.index, paid_values, bottom=budget_values,
                       color='salmon', edgecolor='black', label='Платная')

    ax.set_title(f'Распределение заявлений по приоритетам и форме обучения для направления {specialization}')
    ax.set_xlabel('Приоритет')
    ax.set_ylabel('Количество заявлений')
    ax.set_xticks(priority_counts.index)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    ax.legend()

    # Attach bar values
    for bar_budget, bar_paid in zip(bars_budget, bars_paid):
        height_budget = bar_budget.get_height()
        height_paid = bar_paid.get_height()
        total_height = height_budget + height_paid

        if height_budget > 0:
            ax.text(bar_budget.get_x() + bar_budget.get_width()/2, height_budget / 2,
                    f'{int(height_budget)}', ha='center', va='center', fontsize=8, color='black')

        if height_paid > 0:
            ax.text(bar_paid.get_x() + bar_paid.get_width()/2, height_budget + height_paid / 2,
                    f'{int(height_paid)}', ha='center', va='center', fontsize=8, color='black')


def save_image(image_buffer, file_path: str) -> None:
    image_buffer.seek(0)
    with open(file_path, 'wb') as f:
        f.write(image_buffer.getvalue()) 


def text_output(priority_counts: pd.DataFrame) -> str:
    """Creates text table from data."""
    
    output = []
    # output.append(f"{'Приоритет':<12} {'Количество заявлений':<20}")  # Header
    # output.append("-" * 32)  # Separator line

    # for priority in range(1, 26):
    #     count = priority_counts.get(priority, 0)
    #     output.append(f"{priority:<12} {count:<20}")  # Formatted row

    output.append(f"Кол-во заявлений: на бюджет — {priority_counts['Бюджетная'].sum()}, на платное — {priority_counts['Платная'].sum()}\n")

    return "\n".join(output)


def analyze_priority(file_path: str) -> pd.DataFrame:
    df = load_csv(file_path)

    # Map numeric codes back to readable form for output
    df['Основа обучения'] = df['Основа обучения'].map({0: 'Платная', 1: 'Бюджетная'})

    # Filter valid priorities (1–25)
    valid_priorities = df[df['Приоритет'].isin(range(1, MAX_PRIORITY))]

    # Count number of applications per priority and education base
    priority_counts = valid_priorities.groupby(['Приоритет', 'Основа обучения'], observed=False).size().unstack(fill_value=0)

    return priority_counts


def run_analysis(file_path: str, specialization: str) -> tuple[str, BytesIO]:
    priority_counts = analyze_priority(file_path)
    
    text = text_output(priority_counts)
    infographic_output(priority_counts, specialization)
    image_buffer = save_infographic()

    return text, image_buffer