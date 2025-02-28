import mplfinance as mpf
import pandas as pd


def apply_rule(new_col, value_col, time_col, direction):  # Преобразование, описанное в файле к заданию
    df_new[new_col] = None
    beg, end = (0, len(df_new)) if direction == 1 else (len(df_new) - 1, -1)
    df_new.loc[beg, new_col] = df_new.loc[beg, value_col]
    interval = range(beg + direction, end, direction)
    for i in interval:
        if df_new.loc[i, time_col] == df_new.loc[i - direction, time_col]:
            df_new.loc[i, new_col] = df_new.loc[i - direction, new_col]
        else:
            df_new.loc[i, new_col] = df_new.loc[i, value_col]


df = pd.read_csv('SPFB.RTS-12.18_180901_181231.csv')  # Читаем файл

df_new = df[df['<DATE>'] == '12/09/18'].copy()  # Делаем дубликат с нужными нам столбцами
df_new['HOUR'] = df_new['<TIME>'].str[:2]  # Создаём столбец часов
df_new = df_new.reset_index(drop=True)  # Сбрасываем индексы к нумерации с нуля
apply_rule('OPEN_HOUR', '<OPEN>', 'HOUR', direction=1)  # Создаём столбец 'OPEN_HOUR'
apply_rule('CLOSE_HOUR', '<CLOSE>', 'HOUR', direction=-1)  # По аналогии


df_new = df_new.drop_duplicates(subset=['HOUR'])  # Убираем дубликаты по часам, оставляя только первые вхождения

# Дальнейшие шаги просто ОБЯЗАТЕЛЬНЫЕ по требованиям
df_jap = df_new[['OPEN_HOUR', '<HIGH>', '<LOW>', 'CLOSE_HOUR']].copy()  # Создаём дата фрейм с ТОЛЬКО нужными данными
df_jap = df_jap.set_index(df_new['<TIME>'].apply(pd.to_datetime))  # Приводим индексы к типу datetime(обязательно)
# тут переименовываем столбцы согласно требованию библиотеки mplfinance
df_jap = df_jap.rename(columns={'OPEN_HOUR': 'Open', '<HIGH>': 'High', '<LOW>': 'Low', 'CLOSE_HOUR': 'Close'})

# Следующие 4 строчки - приведение значений к числовому типу согласно требованиям библиотеки mplfinance
df_jap['Open'] = pd.to_numeric(df_jap['Open'])
df_jap['High'] = pd.to_numeric(df_jap['High'])
df_jap['Low'] = pd.to_numeric(df_jap['Low'])
df_jap['Close'] = pd.to_numeric(df_jap['Close'])

print(df_jap)  # Получившийся дата фрейм

mpf.plot(df_jap, type='candle', style='charles')  # Построение японских свечей
