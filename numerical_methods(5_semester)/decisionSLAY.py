import numpy as np
from sympy import Symbol, diff


# Задаём порядок производной
K = 2

# Задаём количество точек
M = 3


###########################


N = M - 1

h = 2

x0 = 1

xp = (M // 2) * h + x0  # точка для средней разности

x = Symbol('x')

V = np.zeros(N + 1)
for i in range(N + 1):
    V[i] = diff(x**i, x, K).subs(x, xp)

print(V)


# M1 = [[0] * (N + 1) for i in range(M)]
M1 = np.zeros((N+1, M))

for i in range(N + 1):
    for j in range(M):
        M1[i][j] = ((x + h*j).subs(x, x0))**i


print(M1)

arr = np.linalg.solve(M1, V)

print(arr * h**K)
