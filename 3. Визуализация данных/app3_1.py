import matplotlib.pyplot as plt
import pandas as pd


df = pd.read_excel('var123719.xlsx')  # Читаем весь файл

# Задание 1.1
df_1 = df[['Choice_1']]  # Выбираем нужный столбец (двойные скобки для сохранения структуры дата фрейма
df_1 = df_1.dropna()  # Избавимся от None
counts = df_1['Choice_1'].value_counts()  # Считаем всевозможные значения строк
df_1['Amount'] = df_1['Choice_1'].map(counts)  # Создаём столбец с количеством выборов каждого варианта
df_1.drop_duplicates(keep='first', inplace=True)  # Избавляемся от дубликатов
df_1 = df_1.sort_values(by=['Choice_1'])  # Сортируем, чтобы получить столбчатую диаграмму, как в примерах
df_1.reset_index(drop=True, inplace=True)  # Делаем нормальную нумерацию для индексов
new_indices = list(range(2, 10)) + [0, 1]  # Новый порядок индексов (в примерах первые 2 строки должны быть последними)
df_1 = df_1.reindex(new_indices)  # Новая индексация

plt.bar(df_1['Choice_1'], df_1['Amount'])  # Строим столбчатую диаграмму

print(df_1)  # Получившийся дата фрейм

plt.show()  # Наша столбчатая диаграмма


# Задание 1.2
# df = df.dropna() - Не в коем случае! Удалятся ПОЛНОСТЬЮ строки, где есть None
df_s = df.stack().value_counts()  # Создадим серию, где индексы - элементы дата фрейма, а значения - кол-во каждого.

print(df_s)  # Получившаяся серия

df_s.plot.pie(autopct='%1.1f%%')  # Строим круговую диаграмму с процентами

plt.show()  # Наша круговая диаграмма
