import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.graphics.tsaplots import plot_acf
from math import log10


df = pd.read_csv('HW_6.csv', index_col='TIME')  # Считываем данные
df.columns = ['Real_f']  # Решил переименовать
lags = min(10 * log10(32), 32/4)  # Эмпирическое правило для параметра lags(сдвиги), нужного в функции plot_acf

'''Автокорреляционная функция (ACF) — это математический инструмент, используемый для выявления корреляций между
значениями временного ряда на разных временных лагах (сдвигах). Она измеряет, насколько похожи значения ряда 
на себя, но сдвинутые во времени. Нам она поможет найти кандидатов на период. Голубая площадь - это доверительный
интервал (обычно 95%). Если значения выходят из него, то они считаются статистически значимыми, то есть
корреляция между значениями временного ряда с данным лагом (сдвигом) вероятно не случайна и есть шанс, что это наш
период. Чем выше столбик, тем значимее. Ноль не считаем.'''
plot_acf(df, lags=lags)  # Наиболее вероятные кандидаты - это 1 и 7, но 1 на графике явно не наш период, значит 7.
# plt.plot(df)  # Можно просмотреть на график.


'''(Необязательно, просто для анализа) Зная период, спрогнозируем. Для этого начнём с функции seasonal_decompose,
которая разделит нам временной ряд на составляющие (тренд, сезонность, шум). Так будет удобно в дальнейшем.
По-хорошему, нужно попробовать и мультипликативную модель, и аддитивную модель'''
decomposition = seasonal_decompose(df['Real_f'], model='multiplicative', period=7)
decomposition.plot()  # Выведем её


'''Создает объект модели экспоненциального сглаживания Хольта-Винтерса с аддитивным трендом (trend='add') и
аддитивной сезонностью (seasonal='add') с периодом 7 (seasonal_periods=7). Это означает, что модель будет учитывать
линейный тренд и повторяющуюся сезонность каждые 7 временных шагов.'''
fit1 = ExponentialSmoothing(df, trend='add', seasonal='add', seasonal_periods=7).fit()
fit2 = ExponentialSmoothing(df, trend='mul', seasonal='mul', seasonal_periods=7).fit()


'''(Необязательно, просто чтобы посмотреть на параметры) Создадим дата фрейм, в котором будут 3 параметра
сглаживания (от 0 до 1) для аддитивной модели и 3 параметра сглаживания для мультипликативной модели.'''
results = pd.DataFrame(index=['alpha', 'beta', 'gamma'])
params = ['smoothing_level', 'smoothing_trend', 'smoothing_seasonal']
results['Additive'] = [fit1.params[p] for p in params]
results['Multiplicative'] = [fit2.params[p] for p in params]
# print(results)  # Можно посмотреть


'''Всё ниже просто для красивого графика.'''
ax = df.plot(figsize=(20, 6), color='green', title='Модель Хольта-Винтерса')  # Создадим график временного ряда
ax.set_ylabel('Electricity')
ax.set_xlabel('Time')

'''Делаем прогнозирование на 1 период в аддитивной модели'''
fit1.fittedvalues.rename('Aддитивная (ADD)').plot(ax=ax, style='--', color='blue', legend=True)
fit1.forecast(7).rename('Предсказания ADD').plot(ax=ax, style='--', color='darkblue', legend=True)


'''Делаем прогнозирование на 1 период в мультипликативной модели. fit1.fittedvalues: Получает сглаженные (fitted)
значения, предсказанные моделью экспоненциального сглаживания на основе обучающих данных.
Это значения, которые модель «воспроизвела» для каждого временного шага. 
rename('Aддитивная (ADD)'): Переименовывает столбец сглаженных значений в 'Aддитивная (ADD)' для легенды графика.'''
fit2.fittedvalues.rename('Мультипликативная (MUL)').plot(ax=ax, style='--', color='orange', legend=True)
fit2.forecast(7).rename('Предсказания MUL').plot(ax=ax, style='--', color='red', legend=True)


predict = fit1.forecast(7).apply(lambda x: round(x))  # Я выбрал аддитивную модель и округлил до целых.
print(predict.values)  # Здесь можно увидеть предсказанные значения.
plt.show()
