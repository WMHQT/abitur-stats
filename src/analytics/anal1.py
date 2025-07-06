import pandas as pd
import matplotlib.pyplot as plt

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

# Фильтрация записей с приоритетами 1–25
valid_priorities = df[df['Приоритет'].isin(range(1, 30))]

# Подсчет количества заявлений по приоритетам
priority_counts = valid_priorities['Приоритет'].value_counts().sort_index()

# Вывод результатов
print("\nКоличество заявлений по приоритетам:")
for priority in range(1, 30):
    count = priority_counts.get(priority, 0)
    print(f"Приоритет {priority}: {count} заявлений")

# Создание инфографики
plt.figure(figsize=(10, 6))
priority_counts.plot(kind='bar', color='skyblue', edgecolor='black')
plt.title('Распределение заявлений по приоритетам')
plt.xlabel('Приоритет')
plt.ylabel('Количество заявлений')
plt.xticks(rotation=0)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Сохранение графика в PNG
plt.savefig('priority_distribution.png', dpi=300, bbox_inches='tight')
print("\nИнфографика сохранена в 'priority_distribution.png'")

# Показать график (опционально, можно закомментировать)
plt.show()
