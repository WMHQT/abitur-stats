import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def run_anal4(file_path='parsed_ps_search_results.csv'):
    # Загрузка данных
    try:
        df = pd.read_csv(file_path, encoding='utf-8')
    except FileNotFoundError:
        return f"Файл {file_path} не найден. Проверьте путь к файлу.", None
    except UnicodeDecodeError:
        df = pd.read_csv(file_path, encoding='windows-1251')

    # Фильтрация записей с приоритетами 1 и 2
    valid_priorities = df[df['Приоритет'].isin([1, 2])]

    # Группировка по приоритетам и необходимости общежития
    counts = valid_priorities.groupby(['Приоритет', 'Общежитие']).size().unstack(fill_value=0)

    # Формирование текстового вывода
    output = ["Разбивка заявлений по приоритетам и необходимости общежития:", str(counts)]
    for priority in [1, 2]:
        output.append(f"\nПриоритет {priority}:")
        for dorm_status in ['нужд.', 'не нужд.']:
            count = counts.get(dorm_status, pd.Series(0)).get(priority, 0)
            output.append(f"  {dorm_status}: {count} заявлений")

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

    return "\n".join(output), image_path
