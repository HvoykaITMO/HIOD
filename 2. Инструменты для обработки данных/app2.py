import pandas as pd


# Читаем файл
df = pd.read_csv('task2_112737.csv', encoding='utf8', sep=',')

# Пункты 1 и 2
df["Price"] = df[['<OPEN>', '<HIGH>', '<LOW>', '<CLOSE>']].mean(axis=1)
df["Total"] = df['Price'] * df["<VOL>"]
df_19_11_2020 = df[(df['<DATE>'] == '09.11.2020') & (df['<TIME>'] == '19:02:00')]  # # Ответы

# Пункт 3 (суммарный оборот по совершенным сделкам за 15.10.2020.)
df_15_10_2020 = df[df['<DATE>'] == '15.10.2020']
summary_15_10_2020 = df_15_10_2020['Total'].sum()  # Ответ

# Пункт 4(Вычислите количество минутных интервалов за 13.11.2020, когда цена открытия была строго больше цены закрытия)
df_1 = df[(df['<DATE>'] == '13.11.2020') & (df['<OPEN>'] > df['<CLOSE>'])]
intervals_amount = len(df_1)  # Ответ

# Последний пункт (четверги сентября)
df_september_thurs = df[df['<DATE>'].str.match(r'^\d{2}\.09\.2020')]  # Побочный дата фрейм
thursday_datas = [f"{el}.09.2020".rjust(10, '0') for el in range(3, 30, 7)]  # создаём список с датами
df_september_thurs = df_september_thurs[df_september_thurs['<DATE>'].str.contains('|'.join(thursday_datas))]  # четверги
average_amount_thurs = df_september_thurs['Total'].mean()  # Ответ

print('Пункты 1 и 2:\n', df_19_11_2020)
print('Пункт 3:', summary_15_10_2020)
print('Пункт 4:', intervals_amount)
print('Пункт 5:', average_amount_thurs)
