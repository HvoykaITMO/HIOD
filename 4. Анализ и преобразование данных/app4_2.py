import pandas as pd
import numpy as np
import re


# Для Артёма: Norm(STOP_COUNT) + Norm(DISTANCE) + Norm(COST) + 0.2 * Norm(FITNESS) – 0.4 * Norm(INTERNET)
# Для Анны: Norm(STOP_COUNT) + Norm(DISTANCE) + Norm(COST) - 0.1 * Norm(INTERNET) - 0.3 * DOG_WALKING

# Функция, которая к каждому столбцу применяет экспоненциальную нормализацию
def exp_normalization(vector: pd.Series):
    return 1 - np.exp(1 - vector/vector.min())


# Функция, которая к каждому столбцу применяет линейную нормализацию
def lin_normalization(vector: pd.Series):
    return (vector - vector.min()) / (vector.max() - vector.min())


# Функция поиска по ключевым словам (можно использовать и библиотеку re вместо этой функции)
def is_dogging(el: str):
    return int((any(substr in el for substr in ['площадк', 'выгул']) and
            any(substr in el for substr in ['питом', 'собак', 'четвероног', 'выгул']))) if el is not np.nan else 0


df = pd.read_csv('task4_1_939291.csv', encoding='utf8', delimiter=';') # Создаём исходный дата фрейм
df = df[df['INTERNET'] != 0] # Убираем квартиры, где нет провайдеров, они не нужны обоим людям
df.index += 1 # Индексы идут с нуля, добавим 1 и тогда они будут совпадать с номерами квартир


artem_df = df.loc[:, ['STOP_COUNT', 'DISTANCE', 'COST', 'FITNESS', 'INTERNET']] # Дата фрейм с параметрами Артёма
artem_df = artem_df.apply(exp_normalization) # Применяем к ним нужную нормализацию

# Создаём столбец с результатом целевой функции
artem_df['AIM_FUNC'] = (artem_df['STOP_COUNT'] + artem_df['DISTANCE'] + artem_df['COST']
                        + 0.2 * artem_df['FITNESS'] - 0.4 * artem_df['INTERNET'])
artem_df = artem_df.sort_values(by='AIM_FUNC', ascending=True) # Сортируем по возрастанию для поиска минимальных

print(artem_df) # Результат


anna_col = ['STOP_COUNT', 'DISTANCE', 'COST', 'INTERNET', 'PETS_ALLOWED', 'ADDITIONAL_INFO'] # Параметры для Анны
anna_df = df.loc[:, anna_col] # Создаём дата фрейм с нужными параметрами
anna_df = anna_df[anna_df['PETS_ALLOWED'] == 'Да'] # Оставляем только квартиры с разрешением на питомцев

# Создаём столбец, который покажет, есть ли место для выгула собак
anna_df['DOG_WALKING'] = anna_df['ADDITIONAL_INFO'].map(lambda x: is_dogging(x))

anna_df = anna_df.drop(['ADDITIONAL_INFO', 'PETS_ALLOWED'], axis=1) # Убираем уже ненужные параметры
anna_df = anna_df.apply(lin_normalization) # Применяем нормализацию

# Создаём столбец с результатом применения целевой функции к квартирам
anna_df['AIM_FUNC'] = (anna_df['STOP_COUNT'] + anna_df['DISTANCE'] + anna_df['COST']
                       - 0.1 * anna_df['INTERNET'] - 0.3 * anna_df['DOG_WALKING'])
anna_df = anna_df.sort_values(by='AIM_FUNC', ascending=True) # Сортируем для поиска минимальных

print(anna_df) # Результат