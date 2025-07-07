import matplotlib.pyplot as plt
import pandas as pd


def run_anal1(file_path='parsed_ps_search_results.csv'):
    # Загрузка данных
    try:
        df = pd.read_csv(file_path, encoding='utf-8')
    except FileNotFoundError:
        return f"Файл {file_path} не найден. Проверьте путь к файлу.", None
    except UnicodeDecodeError:
        df = pd.read_csv(file_path, encoding='windows-1251')

    # Фильтрация записей с приоритетами 1–25
    valid_priorities = df[df['Приоритет'].isin(range(1, 26))]

    # Подсчет количества заявлений по приоритетам
    priority_counts = valid_priorities['Приоритет'].value_counts().sort_index()

    # Формирование текстового вывода
    output = ["Количество заявлений по приоритетам:"]
    for priority in range(1, 26):
        count = priority_counts.get(priority, 0)
        output.append(f"Приоритет {priority}: {count} заявлений")

    # Создание инфографики
    plt.figure(figsize=(10, 6))
    priority_counts.plot(kind='bar', color='skyblue', edgecolor='black')
    plt.title('Распределение заявлений по приоритетам')
    plt.xlabel('Приоритет')
    plt.ylabel('Количество заявлений')
    plt.xticks(rotation=0)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Сохранение графика
    image_path = 'priority_distribution.png'
    plt.savefig(image_path, dpi=300, bbox_inches='tight')
    plt.close()

    return "\n".join(output), image_path
