import numpy as np
from sklearn.neural_network import MLPRegressor

# Инициализация нейросетевого регулятора
nn_controller = MLPRegressor(hidden_layer_sizes=(10,), max_iter=1000, learning_rate_init=0.01)

# Задаем начальные данные (исторические данные для обучения нейросети)
# Эти данные должны быть собраны в процессе работы системы.
# temperature_data - входные данные (температура)
# power_data - выходные данные (управляющий сигнал, например, мощность нагревателя)

temperature_data = np.array([[20], [22], [24], [26], [28]])  # Пример данных температуры
power_data = np.array([10, 12, 14, 16, 18])  # Пример данных мощности нагревателя

# Обучение нейронной сети
nn_controller.fit(temperature_data, power_data)

# Функция для получения управляющего сигнала от нейросети
def get_control_signal(current_temperature):
    control_signal = nn_controller.predict([[current_temperature]])
    return control_signal[0]

# Пример использования регулятора
current_temperature = 25  # Текущая измеренная температура
control_signal = get_control_signal(current_temperature)

print(f"Управляющий сигнал для текущей температуры {current_temperature}°C: {control_signal}")
