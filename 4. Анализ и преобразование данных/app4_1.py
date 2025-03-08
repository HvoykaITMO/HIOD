import numpy as np


# (x - x_min) / (x_max - x_min) - Линейная нормировка

# Зададим массив array
vector = np.array([78, 85, 95, 44, 53, 24, 98, 45, 57, 66], dtype=np.float32)
vector = np.round((vector - np.min(vector)) / (np.max(vector) - np.min(vector)), 2)  # Нормировка по формуле
print(vector)  # Ответ
