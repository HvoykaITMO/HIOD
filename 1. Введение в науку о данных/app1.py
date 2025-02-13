import pandas as pd
import numpy as np
import datetime


def round_time(t):  # функция округления timedelta объекта
    return datetime.timedelta(seconds=int(t.total_seconds()))


# Читаем файл
df = pd.read_csv("task1_v3_2_514811.csv", encoding='utf8', sep=',', index_col=0)

# Находим нужный столбец и создаём побочный дата фрейм
interesting_column = df.columns[df.isin(['00:00:00']).any()][0]
df_part = df.iloc[np.where(df[interesting_column].isin(['00:00:00']))]

# Расширяем побочный дата фрейм и приводим к типу timedelta
index_part = df_part.index.to_list()
min_index = df.index.get_loc(index_part[0]) - 1
max_index = df.index.get_loc(index_part[-1]) + 1
df_part = df.iloc[min_index:max_index + 1]
df_part = df_part.apply(pd.to_timedelta)

# Создаём столбец с длительностью прохождения интервалов на других рейсах
columns_to_diff = df.columns.to_list()
columns_to_diff.remove(interesting_column)
df_part[[f'Длительно прохождения интервалов {col}' for col in columns_to_diff]] = df_part[columns_to_diff].diff()

# Создаём столбец со средней длительностью прохождения интервалов на других рейсах
df_part['Среднее время прохождения'] = df_part.iloc[:, 4:6 + 1].mean(axis=1)

# Считаем общую длину интервалов на нашем рейсе, среднюю общую длину интервалов на нашем рейсе, нужный коэффициент
interval = df_part[interesting_column].diff(periods=6).iloc[-1]
average_interval = df_part['Среднее время прохождения'].sum()
cuff = interval / average_interval

# Создаём столбец с предполагаемой длительностью каждого интервала
df_part['Предполагаемая длительность'] = df_part['Среднее время прохождения'] * cuff

# Меняем значение Nan на известную длительность, чтобы использовать функцию накопления суммы
df_part.loc['22-23-Я ЛИНИИ', 'Предполагаемая длительность'] = df_part.loc['22-23-Я ЛИНИИ', interesting_column]
df_part[interesting_column] = df_part['Предполагаемая длительность'].cumsum()

# Округляем до целого числа путём перевода timedelta объекта в секунды
df_part[interesting_column] = df_part[interesting_column].apply(lambda x: round_time(x))

print(df_part[interesting_column])
