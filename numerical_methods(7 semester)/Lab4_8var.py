"""
Лабораторная работа N4 (Вариант 8)
Основы метода конечных элементов

Решить численно разностным методом и методом конечных элементов с кусочно-линейными базисными функциями граничную
задачу:

d^2(U)/d(x^2) = f(x), 0 < x < 1, U(0) = 0, U(1) = 0

f(x) = exp(x)

Сравнить результаты решения, полученные двумя методами с точным решением.

Теорию можно найти по ссылке: http://ouek.onu.edu.ua/uploads/courses/varcalculus/%D0%9B%D0%B0%D0%B1%D0%BE%D1%80%D0%B0%D1%82%D0%BE%D1%80%D0%BD%D0%B0%D1%8F%20%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%B0%20%E2%84%961.%20%D0%A3%D0%BA%D0%B0%D0%B7%D0%B0%D0%BD%D0%B8%D1%8F.pdf
Или в лекциях по численным методам (семестр 7)
"""

# Импорты
import numpy as np
import matplotlib.pylab as plt


# Определение констант и функций
N = 101  # Точек по оси x
LEFT_BOUND = 0
RIGHT_BOUND = 1
h = (RIGHT_BOUND - LEFT_BOUND)/(N - 1)  # Шаг по х
x_grid = np.arange(LEFT_BOUND, RIGHT_BOUND+h, h)  # Задаём сетку по x


def f(_x: float) -> float:
    return np.exp(_x)


def get_exact_value(_x: float) -> float:
    return np.exp(_x) + (1 - np.exp(1))*_x - 1


def get_error(_x: np.array, _y: np.array) -> float:
    return max(abs(_x.reshape(1, -1)[0] - _y.reshape(1, -1)[0]))


def get_psi_vector(_x: float, _grid: np.array) -> np.array:
    psi_vector = np.zeros(N-2)
    for i in range(1, len(_grid) - 1):
        if 0 <= _x <= _grid[i - 1]:
            psi_vector[i - 1] = 0
        elif _grid[i - 1] < _x <= _grid[i]:
            psi_vector[i - 1] = 1 / h * (_x - _grid[i - 1])
        elif _grid[i] < _x <= _grid[i + 1]:
            psi_vector[i - 1] = 1 / h * (_grid[i + 1] - _x)
        elif _grid[i + 1] < _x <= 1:
            psi_vector[i - 1] = 0
    return psi_vector


# Точное решение
u_exact = np.array([get_exact_value(x) for x in x_grid])


# Решение разностным методом
u_numeric = None

A_numeric = np.eye(N)

for i in range(1, len(A_numeric) - 1):
    A_numeric[i, i] = -2/h/h
    A_numeric[i, i - 1] = 1/h/h
    A_numeric[i, i + 1] = 1/h/h

f_numeric = np.array([f(x) if x != 0 and x != 1 else 0 for x in x_grid])
u_numeric = np.linalg.inv(A_numeric).dot(f_numeric)

print(f"Ошибка в решении (Точное решение/Решение разностным методом): {get_error(u_exact, u_numeric)}")

# Решение методом конечных элементов
u_ritz = None

A_ritz = np.eye(N-2)

A_ritz[0, 0] = -2/h
A_ritz[0, 1] = 1/h
A_ritz[-1, -1] = -2/h
A_ritz[-1, -2] = 1/h

for i in range(1, len(A_ritz) - 1):
    A_ritz[i, i] = -2/h
    A_ritz[i, i - 1] = 1/h
    A_ritz[i, i + 1] = 1/h

b_ritz = np.zeros(N-2)
for i in range(1, len(x_grid) - 1):
    b_ritz[i - 1] = (1/h*(np.exp(x_grid[i+1]) - np.exp(x_grid[i])*(h+1)) +
                     1/h*(np.exp(x_grid[i])*(h-1) + np.exp(x_grid[i-1])))

c_ritz = np.linalg.inv(A_ritz).dot(b_ritz)
u_ritz = np.zeros(N)

for i in range(1, len(x_grid) - 1):
    u_ritz[i] = c_ritz @ get_psi_vector(x_grid[i], x_grid).T

print(f"Ошибка в решении (Точное решение/Решение методом конечных элементов): {get_error(u_exact, u_ritz)}")

# Отрисовка (перед тестами следует закомментировать)
fig_exact = plt.figure("Точное решение")
plt.title("Точное решение")
plt.plot(x_grid, u_exact)

fig_numeric = plt.figure("Решение разностным методом")
plt.title("Решение разностным методом")
plt.plot(x_grid, u_numeric)

fig_ritz = plt.figure("Решение методом конечных элементов")
plt.title("Решение методом конечных элементов")
plt.plot(x_grid, u_ritz)

plt.show()
