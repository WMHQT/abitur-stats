import pandas as pd

def run_anal3(file_path='parsed_ps_search_results.csv'):
    # Загрузка данных
    try:
        df = pd.read_csv(file_path, encoding='utf-8')
    except FileNotFoundError:
        return f"Файл {file_path} не найден. Проверьте путь к файлу.", None
    except UnicodeDecodeError:
        df = pd.read_csv(file_path, encoding='windows-1251')

    # Фильтрация записей с приоритетами 1 и 2
    priority_1 = df[df['Приоритет'] == 1]
    priority_2 = df[df['Приоритет'] == 2]

    # Вычисление среднего балла ЕГЭ и количества заявлений
    mean_score_p1 = priority_1['Суммабаллов попредметам'].mean()
    count_p1 = priority_1['Суммабаллов попредметам'].count()
    mean_score_p2 = priority_2['Суммабаллов попредметам'].mean()
    count_p2 = priority_2['Суммабаллов попредметам'].count()

    # Формирование текстового вывода
    output = [
        "Анализ среднего балла ЕГЭ по приоритетам:",
        f"Приоритет 1: Средний балл ЕГЭ = {mean_score_p1:.2f}, Количество заявлений = {count_p1}",
        f"Приоритет 2: Средний балл ЕГЭ = {mean_score_p2:.2f}, Количество заявлений = {count_p2}"
    ]

    return "\n".join(output), None  # Нет изображения
