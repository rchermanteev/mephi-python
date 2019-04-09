"""
Метод Монте-Карло для приближённого вычисления интеграла
"""



from math import *
import random

exInt = -0.084411
N = 100
a = 1
b = 1000
I, I1, I2, D, D1, D2 = 0, 0, 0, 0, 0, 0

counter = 0
counter1 = 0
counter2 = 0

for _ in range(1000):

    RN = [random.random() for _ in range(0, N)]

    """
    Метод симметризации подинтегральной функции 
    """

    def MCintegral(n):
        s = 0
        for i in range(n):
            s += cos(1 / (1 - RN[i])) + cos(b + a - a - b + (a + b - 1)/(RN[i]*(b-1)+1))/(b+a-1)
        I = s / n / 2
        return I


    def MCdisp(n):
        s = 0
        s1 = 0
        for i in range(n):
            s += (cos(1 / (1 - RN[i]))) ** 2 + (cos(b + a - a - b + (a + b - 1)/(RN[i]*(b-1)+1))/(b+a-1)) ** 2
            s1 += (cos(1 / (1 - RN[i])) + cos(b + a - a - b + (a + b - 1)/(RN[i]*(b-1)+1))/(b+a-1)) ** 2
        D = s / n / 2 - s1 / 4 / n / n
        return D


    """
    Метод включения особенности подинтегральной функции в плотность 
    """

# p = 1/x^2

    def MCintegral1(n):
        s = 0
        for i in range(n):
            s += cos(1 / (1 - RN[i]))
        I = s / n
        return I



    def MCdisp1(n):
        s = 0
        for i in range(n):
            s += (cos(1 / (1 - RN[i])) - I1) ** 2
        D = s / n
        return D

# p = 1/x^(3/2)

    def MCintegral2(n):
        s = 0
        for i in range(n):
            s += 2*cos(1/(1-RN[i])**2)/sqrt(1/(1-RN[i])**2)
        I = s / n
        return I


    def MCdisp2(n):
        s = 0
        for i in range(n):
            s += (2*cos(1/(1-RN[i])**2)/sqrt((1/(1-RN[i]))**2) - I2) ** 2
        D = s / n
        return D


    I = MCintegral(N)
    D = MCdisp(N)
    I1 = MCintegral1(N)
    D1 = MCdisp1(N)
    I2 = MCintegral2(N)
    D2 = MCdisp2(N)

    err = sqrt(D/N)*3
    ERR = abs(exInt - I)
    err1 = sqrt(D1/N)*3
    ERR1 = abs(exInt - I1)
    err2 = sqrt(D2/N)*3
    ERR2 = abs(exInt - I2)

    if ERR < err: counter += 1
    if ERR1 < err1: counter1 += 1
    if ERR2 < err2: counter2 += 1


print("Метод симметризации подинтегральной функции ")
print("Значение интеграла: {}".format(I))
print("Значение дисперсии: {}".format(D))
print("Условие на ошибку: {}".format(err))
print("{} ? {}".format(ERR, err))
print(counter)


print("Метод включения особенности подинтегральной функции в плотность(p=1/x^2)")
print("Значение интеграла: {}".format(I1))
print("Значение дисперсии: {}".format(D1))
print("Условие на ошибку: {}".format(err1))
print("{} ? {}".format(ERR1, err1))
print(counter1)


print("Метод включения особенности подинтегральной функции в плотность(p=1/x^(3/2))")
print("Значение интеграла: {}".format(I2))
print("Значение дисперсии: {}".format(D2))
print("Условие на ошибку: {}".format(err2))
print("{} ? {}".format(ERR2, err2))
print(counter2)