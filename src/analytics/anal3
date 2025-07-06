import pandas as pd

# Путь к вашему CSV-файлу
file_path = 'parsed_ps_search_results.csv'  # Укажите полный путь, если файл не в той же папке

# Загрузка данных
try:
    df = pd.read_csv(file_path, encoding='utf-8')
except FileNotFoundError:
    print(f"Файл {file_path} не найден. Проверьте путь к файлу.")
    exit()
except UnicodeDecodeError:
    print("Ошибка кодировки. Пробуем кодировку 'windows-1251'.")
    df = pd.read_csv(file_path, encoding='windows-1251')

# Фильтрация записей с приоритетами 1 и 2
priority_1 = df[df['Приоритет'] == 1]
priority_2 = df[df['Приоритет'] == 2]

# Вычисление среднего балла ЕГЭ и количества заявлений
mean_score_p1 = priority_1['Суммабаллов попредметам'].mean()
count_p1 = priority_1['Суммабаллов попредметам'].count()
mean_score_p2 = priority_2['Суммабаллов попредметам'].mean()
count_p2 = priority_2['Суммабаллов попредметам'].count()

# Вывод результатов
print("\nАнализ среднего балла ЕГЭ по приоритетам:")
print(f"Приоритет 1: Средний балл ЕГЭ = {mean_score_p1:.2f}, Количество заявлений = {count_p1}")
print(f"Приоритет 2: Средний балл ЕГЭ = {mean_score_p2:.2f}, Количество заявлений = {count_p2}")
