"""
Решение СЛАУ, возникающей при разностном аппроксимации задачи Дирихле для двумерного уравнения 
Пуассона в прямоугольнике, методом наименьшей погрешности (Метод минимальных поправок)

Uт(х) = 4*(3*x+2*y)*sin(5*x+2*y)+x*x*y, 0<=x<=2, 0<=y<=1

Описание метода можно найти в книге: Самарский, Гулин "Численные методы" стр 118

Кратко:
Неявный итерационный метод:
 x_k+1 = x_k - t_k+1 * inv(B) * r_k,

где:
 r_k = A * x_k - f

 t_k+1 = (A * w_k, w_k) / (inv(B) * A * w_k, A * w_k)

 w_k = inv(B) * r_k

Матрица B - симметричная, положительно определённая матрица (В данной работе B = E)
"""

# Импорты
from sympy import diff, Symbol, sin, simplify, cos
import numpy as np
import matplotlib.pylab as plt


# Функции
def get_error(_x, _y):
    return max(abs(_x.reshape(1, -1)[0] - _y.reshape(1, -1)[0]))


def scalar_multiply(_x, _y):
    return _x.reshape(1, -1)[0] @ _y.reshape(1, -1)[0]


# Посчитаем значение f в уравнении (Uxx + Uyy + f = 0), зная его точное решение
x = Symbol("x")
y = Symbol("y")

u_precise = simplify(4*(3*x+2*y)*sin(5*x+2*y)+x*x*y)

print(f"Точное решение: {u_precise}")

d2x = diff(u_precise, x, 2)
d2y = diff(u_precise, y, 2)

_f = simplify(d2x + d2y)

print(f"Выражение для неоднородности в уравнении (f): {_f}")

# Определим шаги по x, y и объявим матрицы, которые нужны для решения

N = 51  # Точек по оси x
M = 26  # Точек по оси y

h_x = (2 - 0) / (N - 1)
h_y = (1 - 0) / (M - 1)

A = np.zeros((M, M), dtype=np.ndarray)  # Итоговая размерность (M*N x M*N)

for i in range(len(A)):
    for j in range(len(A[0])):
        A[i, j] = np.zeros((N, N))

f = np.zeros(M, dtype=np.ndarray)  # Итоговая размерность (M*N x 1)


# Определим матриы A и f

A[0, 0] = np.eye(N, dtype=float)
A[len(A) - 1, len(A) - 1] = np.eye(N, dtype=float)

matrix = np.eye(N, dtype=float)
matrix[0, 0] = 0
matrix[-1, -1] = 0
matrix *= 1 / h_y / h_y

diag_matrix = np.eye(N, dtype=float)
for i in range(1, len(diag_matrix) - 1):
    diag_matrix[i, i] *= -2*(1/h_x/h_x + 1/h_y/h_y)
    diag_matrix[i, i + 1] = 1 / h_x / h_x
    diag_matrix[i, i - 1] = 1 / h_x / h_x

for i in range(1, len(A) - 1):
    A[i, i-1] = matrix
    A[i, i+1] = matrix
    A[i, i] = diag_matrix


for i in range(M):
    vector = np.ones((N, 1))
    for j in range(N):
        if j == 0 or i == 0 or j == N - 1 or i == M - 1:
            vector[j] = u_precise.subs({x: j * h_x, y: i * h_y}).n()
        else:
            vector[j] = _f.subs({x: j * h_x, y: i * h_y}).n()
    f[i] = vector

_A = np.zeros(len(A), dtype=np.ndarray)
for i in range(len(A)):
    _A[i] = np.concatenate(A.T[i])

A = np.concatenate(_A, axis=1)
f = np.concatenate(f)

x_0 = np.zeros(M, dtype=np.ndarray)  # Итоговая размерность (M*N x 1)

for i in range(M):
    vector = np.zeros((N, 1))
    for j in range(N):
        if j == 0 or i == 0 or j == N - 1 or i == M - 1:
            vector[j] = u_precise.subs({x: j * h_x, y: i * h_y}).n()
    x_0[i] = vector

x_0 = np.concatenate(x_0)

# Наше решение
x_k1 = np.ones((M * N), dtype=float)

print(f"Число обусловленности: {np.linalg.cond(A)}")


# Реализация метода

B = np.eye(N*M)  # B = E
eps = 0.01
x_k = x_0
count = 0

while get_error(x_k, x_k1) >= eps:
    if count:
        x_k = x_k1
    r_k = A.dot(x_k) - f
    w_k = np.linalg.solve(B, r_k)
    A__w_k = A.dot(w_k)
    t_k1 = scalar_multiply(A__w_k, w_k) / scalar_multiply(np.linalg.solve(B, A__w_k), A__w_k)
    x_k1 = x_k - t_k1 * w_k
    count += 1

print(f"Число итераций метода минимальных поправок: {count}")

# Анализ результата

x_precise = np.zeros(M, dtype=np.ndarray)  # Итоговая размерность (M*N x 1)
for i in range(M):
    vector = np.zeros((N, 1))
    for j in range(N):
        vector[j] = u_precise.subs({x: j * h_x, y: i * h_y}).n()
    x_precise[i] = vector

x_precise = np.concatenate(x_precise)

# x_num = np.linalg.inv(A).dot(f)  # Итоговая размерность (M*N x 1)
x_num = np.linalg.solve(A, f)

print(f"Ошибка точное/метод минимальных поправок: {get_error(x_precise, x_k1)}")
print(f"Ошибка точное/численное решение, другой способ: {get_error(x_precise, x_num)}")

# Отрисовка
x_grid = np.arange(0, 2+h_x, h_x)
y_grid = np.arange(0, 1+h_y, h_y)

fig1 = plt.figure("Точное")
plt.title("Точное")
im1 = plt.contourf(x_grid, y_grid, x_precise.reshape(M, -1))
fig1.colorbar(im1)
fig2 = plt.figure("Метод минимальных поправок")
plt.title("Метод минимальных поправок")
im2 = plt.contourf(x_grid, y_grid, x_k1.reshape(M, -1))
fig2.colorbar(im2)
fig3 = plt.figure("Численное, другой способ")
plt.title("Численное, другой способ")
im3 = plt.contourf(x_grid, y_grid, x_num.reshape(M, -1))
fig3.colorbar(im3)

plt.show()
