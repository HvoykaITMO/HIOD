import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np


df = pd.read_csv('task5_614605.csv')  # Считываем данные
df.index += 1  # Чтобы индексы шли C 1


# Реализация экспоненциального сглаживания

'''Применяем экспоненциальное сглаживание. Параметр alpha взят из задания. Параметр adjust = False использует
ненормированные веса, которые не суммируются в единицу. Расчет EWMA в этом случае соответствует рекурсивной формуле'''
df_exp = df.ewm(alpha=0.19, adjust=False).mean()
print(df_exp.loc[56, 'y'])  # Смотрим ответ (end добавлено для красоты
print(df_exp.loc[100, 'y'])  # Смотрим ответ (end добавлено для красоты

plt.plot(df, label='Real function')  # Построим график исходной функции
plt.plot(df_exp, label='Exponent smoothing')  # Построим график экспоненциально сглаженной функции


# Построение линейного тренда

def lin_func(x, k, c):  # Линейная функция
    return k * x + c


def create_linear_trend(x, y):  # Нахождение параметров линейной функции
    params = curve_fit(lin_func, x, y)
    p1, p2 = params[0]  # Коэффициенты a и b
    print('parameter a:', p1)  # Ответ
    return lin_func(x, p1, p2), (p1, p2)


def get_determ_cof(y, f):  # Функция, которая считает коэффициент детерминации по формуле
    y_mean = np.mean(y)
    ssr = np.sum((y - y_mean) ** 2)
    sse = np.sum((y - f) ** 2)
    return 1 - sse/ssr


lin_f, (a, b) = create_linear_trend(df.index, df['y'])  # Наш тренд
plt.plot(lin_f, label='Linear smoothing')  # Отобразим получившуюся линейную функцию

R = get_determ_cof(df['y'], lin_f)  # Наш коэффициент детерминации
print('R^2:', R)
print(lin_func(101, a, b))  # Прогнозируем 101 значение ряда


# Подпишем и выведем все наши графики
plt.legend()
plt.grid(True)
plt.show()
