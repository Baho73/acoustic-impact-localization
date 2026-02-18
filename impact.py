import numpy as np
from scipy.optimize import least_squares
import random
import matplotlib.pyplot as plt

sensors_coords = np.array([[-1.0,-1.0], [-1.0, 1.0], [1.0, 1.0], [1.0, -1.0], [0, -1.0], [0, 1.0]])
v_sound=500
test_impact=(-1.0,0.0)
test_accuracy=0.0 # +- метр

def calculate_time(sensors_coords, v_sound, test_impact, test_accuracy):
    """
    Функция для расчета времени срабатывания датчиков.
    
    Параметры:
    sensors_coords (numpy array): массив координат датчиков размером Nx2, где N - количество датчиков.
    v_sound (float): скорость звука в пластине в метрах в секунду.
    test_impact (tuple): координаты точки удара (x, y).
    
    Возвращает:
    times (numpy array): массив времени срабатывания датчиков размером N.
    """
    x_impact, y_impact = test_impact
    distances = np.sqrt((sensors_coords[:, 0] - x_impact)**2 + (sensors_coords[:, 1] - y_impact)**2)
    print("distances:", distances)

    random_deviations = np.random.uniform(-test_accuracy, test_accuracy, size=distances.shape)
    distances_w_accuracy = distances + random_deviations
    
    print("distances:", distances_w_accuracy)
    times = distances_w_accuracy / v_sound
    times_relative = times - np.min(times)  # вычитаем время срабатывания первого сработавшего датчика
    
    return times_relative    
 




def calculate_impact_point(sensors_coords, times, time_error=0.025):
    """
    Функция для расчета точки удара, точности расчета и скорости звука.
    
    Параметры:
    sensors_coords (numpy array): массив координат датчиков размером Nx2, где N - количество датчиков.
    times (numpy array): массив времени срабатывания датчиков размером N.
    time_error (float): допустимая относительная ошибка измерения времени, по умолчанию равна 2.5% (0.025).
    
    Возвращает:
    impact_point (tuple): координаты точки удара (x, y).
    accuracy (float): точность расчета в метрах.
    sound_speed (float): определенная скорость звука в пластине (м/с).
    """
    def residuals(params, sensors_coords, times):

        x_impact, y_impact, speed, t0 = params
        distances = np.sqrt((sensors_coords[:, 0] - x_impact)**2 + (sensors_coords[:, 1] - y_impact)**2)
        times_expected = distances / speed + t0
        return times_expected - times
    
    # Вычисление центра масс координат датчиков
    x_center = np.mean(sensors_coords[:, 0])
    y_center = np.mean(sensors_coords[:, 1])

    initial_guess = (x_center, y_center, 100, 0)  # начальные значения для x, y, скорости звука и времени удара
    bounds = ((-1, -1, 1, -np.inf), (1, 1, 1000, np.inf))  # ограничения для x, y, скорости звука и времени удара
    # Выполнение оптимизации с использованием метода наименьших квадратов
    result = least_squares(residuals, initial_guess, bounds=bounds, args=(sensors_coords, times))
    
    # Извлечение результатов оптимизации
    impact_point = (result.x[0], result.x[1])
    accuracy = np.max(np.abs(result.fun)) * (1 + time_error)  # учитываем ошибку времени измерения
    sound_speed = result.x[2]  # скорость звука из оптимизации

    return impact_point, accuracy, sound_speed


def plot_impact(sensors_coords, impact_point, accuracy):
    """
    Функция для визуализации точки удара и круга точности на мишени.
    
    Параметры:
    sensors_coords (numpy array): массив координат датчиков размером Nx2, где N - количество датчиков.
    impact_point (tuple): координаты точки удара (x, y).
    accuracy (float): точность расчета в метрах.
    """
    # Создаем фигуру и оси для отображения графика
    fig, ax = plt.subplots()

    # Отображаем датчики на графике
    ax.scatter(sensors_coords[:, 0], sensors_coords[:, 1], c='blue', label='Датчики', zorder=3)

    # Отображаем точку удара на графике
    ax.scatter(impact_point[0], impact_point[1], c='red', label='Точка удара', zorder=2)

    # Отображаем круг точности на графике
    circle = plt.Circle(impact_point, accuracy, color='green', fill=False, label='Точность', zorder=1)
    ax.add_artist(circle)

    # Добавляем легенду и устанавливаем равное масштабирование по осям
    ax.legend()
    ax.set_aspect('equal', adjustable='box')

    # Отображаем график
    plt.show()



# Пример использования функции


print('test_impact:',test_impact)
times = calculate_time(sensors_coords, v_sound, test_impact, test_accuracy)
print("Время срабатывания датчиков:", times)

impact_point, accuracy,sound_speed = calculate_impact_point(sensors_coords, times)

print("Точка удара:", impact_point)
print("Точность расчета:", accuracy, "м")
print("sound_speed:", sound_speed)

a=plot_impact(sensors_coords, impact_point, accuracy)