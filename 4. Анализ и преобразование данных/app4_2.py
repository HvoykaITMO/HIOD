import pandas as pd
import numpy as np


# Для Артёма: Norm(STOP_COUNT) + Norm(DISTANCE) + Norm(COST) + 0.2 * Norm(FITNESS) – 0.4 * Norm(INTERNET)
# Для Анны: Norm(STOP_COUNT) + Norm(DISTANCE) + Norm(COST) - 0.1 * Norm(INTERNET) - 0.3 * DOG_WALKING

# Функция, которая к каждому столбцу применяет
def exp_normalization(vector: pd.Series):
    return 1 - np.exp(1 - vector/vector.min())


def lin_normalization(vector: pd.Series):
    return (vector - vector.min()) / (vector.max() - vector.min())


def is_dogging(el: str):
    return int((any(substr in el for substr in ['площадк', 'выгул']) and
            any(substr in el for substr in ['питом', 'собак', 'четвероног', 'выгул']))) if el is not np.nan else 0


df = pd.read_csv('task4_1_939291.csv', encoding='utf8', delimiter=';')


artem_df = df.loc[:, ['STOP_COUNT', 'DISTANCE', 'COST', 'FITNESS', 'INTERNET']]
artem_df = artem_df[artem_df['INTERNET'] != 0]
artem_df.index += 1
artem_df = artem_df.apply(exp_normalization)
artem_df['AIM_FUNC'] = (artem_df['STOP_COUNT'] + artem_df['DISTANCE'] + artem_df['COST']
                        + 0.2 * artem_df['FITNESS'] - 0.4 * artem_df['INTERNET'])

artem_df = artem_df.sort_values(by='AIM_FUNC', ascending=True)
print(artem_df)


anna_col = ['STOP_COUNT', 'DISTANCE', 'COST', 'INTERNET', 'ADDITIONAL_INFO']
anna_df = df.loc[:, anna_col]
anna_df.index += 1
anna_df['DOG_WALKING'] = anna_df['ADDITIONAL_INFO'].map(lambda x: is_dogging(x))
anna_df[anna_col[:-1]] = anna_df[anna_col[:-1]].apply(lin_normalization)
anna_df['AIM_FUNC'] = (anna_df['STOP_COUNT'] + anna_df['DISTANCE'] + anna_df['COST']
                       - 0.1 * anna_df['INTERNET'] - 0.3 * anna_df['DOG_WALKING'])
anna_df = anna_df.sort_values(by='AIM_FUNC', ascending=True)
print(anna_df)