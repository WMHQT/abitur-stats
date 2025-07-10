import matplotlib.pyplot as plt
import numpy as np
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


def infographic_output(counts: pd.DataFrame, specialization: str) -> None:
    """Creates infographic with four-color coded bars."""
    # Extract data
    priorities = [1, 2]
    
    # Access values using .xs() for MultiIndex columns
    budget_needed = counts.xs(('Бюджетная', 'нужд.'), axis=1)[priorities].values
    budget_not = counts.xs(('Бюджетная', 'не нужд.'), axis=1)[priorities].values
    paid_needed = counts.xs(('Платная', 'нужд.'), axis=1)[priorities].values
    paid_not = counts.xs(('Платная', 'не нужд.'), axis=1)[priorities].values
    
    x = np.arange(len(priorities))
    bar_width = 0.2
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Plot bars with different styles
    budget_needed_bars = ax.bar(x - 1.5*bar_width, budget_needed, bar_width, 
                               label='Бюджет, нуждается', color='skyblue', edgecolor='black')
    budget_not_bars = ax.bar(x - 0.5*bar_width, budget_not, bar_width,
                            label='Бюджет, не нуждается', color='skyblue', 
                            edgecolor='black', hatch='//')
    paid_needed_bars = ax.bar(x + 0.5*bar_width, paid_needed, bar_width,
                             label='Платная, нуждается', color='salmon', 
                             edgecolor='black')
    paid_not_bars = ax.bar(x + 1.5*bar_width, paid_not, bar_width,
                          label='Платная, не нуждается', color='salmon', 
                          edgecolor='black', hatch='//')
    
    # Customize plot
    ax.set_xlabel('Приоритет')
    ax.set_ylabel('Количество заявлений')
    ax.set_title(f'Разбивка заявлений по приоритетам и форме обучения для направления {specialization}')
    ax.set_xticks(x)
    ax.set_xticklabels([f'Приоритет {p}' for p in priorities])
    ax.legend()
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Add value labels
    for bars in [budget_needed_bars, budget_not_bars, paid_needed_bars, paid_not_bars]:
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax.text(bar.get_x() + bar.get_width()/2, height, 
                       f'{int(height)}', ha='center', va='bottom', fontsize=8)


def analyze_dormitory(file_path: str) -> pd.DataFrame:
    df = load_csv(file_path)
    
    # Map numeric codes to text labels
    df['Основа обучения'] = df['Основа обучения'].map({0: 'Платная', 1: 'Бюджетная'})
    # df['Общежитие'] = df['Общежитие'].map({0: 'не нужд.', 1: 'нужд.'})
    
    # Enforce categorical types to ensure all combinations are present
    df['Основа обучения'] = pd.Categorical(df['Основа обучения'], categories=['Бюджетная', 'Платная'])
    df['Общежитие'] = pd.Categorical(df['Общежитие'], categories=['нужд.', 'не нужд.'])
    
    # Filter valid priorities
    valid_priorities = df[df['Приоритет'].isin(range(1, 26))]
    
    # Count applications by priority, funding type, and dorm need
    priority_counts = pd.crosstab(
        index=valid_priorities['Приоритет'],
        columns=[
            valid_priorities['Основа обучения'],
            valid_priorities['Общежитие']
        ],
        margins=False,
        dropna=False
    )
    
    # Ensure all priorities 1-25 are present
    full_index = pd.Index(range(1, 26), name='Приоритет')
    priority_counts = priority_counts.reindex(full_index, fill_value=0)
    
    return priority_counts


def text_output(counts: pd.DataFrame) -> str:
    """Creates text table from data."""
    output = []

    priorities = [1, 2]

    # Extract values for each category using .xs()
    budget_needed = counts.xs(('Бюджетная', 'нужд.'), axis=1)[priorities].values
    budget_not = counts.xs(('Бюджетная', 'не нужд.'), axis=1)[priorities].values
    paid_needed = counts.xs(('Платная', 'нужд.'), axis=1)[priorities].values
    paid_not = counts.xs(('Платная', 'не нужд.'), axis=1)[priorities].values

    for idx, priority in enumerate(priorities):
        output.append(f"Приоритет: {priority}")
        output.append(f"бюджет, нужд.: {int(budget_needed[idx])}")
        output.append(f"бюджет, не нужд.: {int(budget_not[idx])}")
        output.append(f"платная, нужд.: {int(paid_needed[idx])}")
        output.append(f"платная, не нужд.: {int(paid_not[idx])}")
        output.append("—" * 12)

    return "\n".join(output)


def run_analysis(file_path: str, specialization: str) -> tuple[str, BytesIO]:
    counts = analyze_dormitory(file_path)
    
    text = text_output(counts)
    infographic_output(counts, specialization)
    image_buffer = save_infographic()

    return text, image_buffer