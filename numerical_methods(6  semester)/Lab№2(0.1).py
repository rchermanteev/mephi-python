"""
Решение уравнения теплопроводности Ut = a * Uxx + f(x,t)  0<t<=2  0<x<1
для 4х вариантов схем:
    1) Cхема Кранка-Никольсона (g=0.5)
    2) Схема «ромб» (схема Дюфорта-Франкела)
    3) Схема Алена-Чена
    4) Cхема Саульева
"""


from math import *


hh = 0.01  # Шаг по координате
tt = 0.01  # Шаг по времени
T = 2  # Граница по времени
L = 1  # Граница по координате

sizeL = int(L / hh) + 1
sizeT = int(T / tt) + 1

# Ut = a * Uxx + f(x,t)    0<t<=T     0<x<L
# a1 * Ux(0,t) + b1 * U(0,t) = c1
# a2 * Ux(L,t) + b2 * U(L,t) = c2
# U(x,0) = d1


a1 = 0; b1 = 1
a2 = 1; b2 = 0


a = 1  # a^2
g = 0.5  # Сигма из схемы с весами


def getExactValue(x, t):
    return 3*x+2-t*t*cos(4*x)


def d1(x):
    return 3*x+2


def c1(t):
    return 2-t*t


def c2(t):
    return 3+t*t*4*sin(4)


def f(x, t):
    return -cos(4*x)*(2*t+16*t*t)


def FillxValue(sizeL, hh):
    return [0 + hh * i for i in range(sizeL)]


def FilltValue(sizeT, tt):
    return [0 + tt * i for i in range(sizeT)]


def ArrayOfSolving():
    r = 0
    mas = []
    for i in range(sizeT):
        mas.append([])
        for j in range(sizeL):
            mas[i].append(r)
    return mas


def viewArray(arr, sX, sT):
    for i in range(sT):
        for j in range(sX):
            print(arr[i][j], end=' | ')
        print()


def FirstLayer_X(x):
    return d1(x)


def FillExactArray(arr, arr_x, arr_t):
    for j in range(len(arr)):
        for i in range(len(arr[j])):
            arr[j][i] = getExactValue(arr_x[i], arr_t[j])


def FillErArray(arr1, arr2, arr):
    for j in range(len(arr)):
        for i in range(len(arr[j])):
            arr[j][i] = abs(arr1[j][i] - arr2[j][i])


def maxValue(arr):
    _max = arr[0][0]
    for j in range(len(arr)):
        if max(arr[j]) >= _max:
            _max = max(arr[j])
    return _max


############ Коэффициенты для метода прогонки #############
######## Разностная апроксимация с первой точностью #######


ak = a*g/hh/hh
bk = -2*a*g/hh/hh - 1/tt
ck = a*g/hh/hh


def bN(accuracy):
    if accuracy == 'O1':
        return a2/hh + b2
    elif accuracy == 'O2':
        return 1/tt+2*a*g/hh/hh+2*b2*a*g/a2/hh


def aN(accuracy):
    if accuracy == 'O1':
        return -a2/hh
    elif accuracy == 'O2':
        return -2*a*g/hh/hh


def b0(accuracy):
    if accuracy == 'O1':
        return b1 - a1/hh
    elif accuracy == 'O2':
        return 1/tt+2*a*g/hh/hh-2*b1*a*g/a1/hh


def c0(accuracy):
    if accuracy == 'O1':
        return a1/hh
    elif accuracy == 'O2':
        return -2*a*g/hh/hh


def f0(arr, arr_x, arr_t, t, accuracy):
    if accuracy == 'O1':
        return c1(arr_t[t])
    elif accuracy == 'O2':
        return arr[t][0]*(1/tt-2*(1-g)*a/hh/hh+2*(1-g)*a*b1/hh/a1)+arr[t][1]*(a*2*(1-g)/hh/hh)-c1(arr_t[t+1])*2*a*g/hh/a1-c1(arr_t[t])*2*a*(1-g)/a1/hh+f(arr_x[0], arr_t[t]+tt/2)


def fN(arr, arr_x, arr_t, t, accuracy):
    if accuracy == 'O1':
        return c2(arr_t[t])
    elif accuracy == 'O2':
        return arr[t][-1]*(1/tt-2*a*(1-g)/hh/a2*b2-2*a*(1-g)/hh/hh)+arr[t][-2]*(2*a*(1-g)/hh/hh)+c2(arr_t[t])*2*(1-g)*a/a2/hh+c2(arr_t[t+1])*2*a*g/a2/hh+f(arr_x[-1], arr_t[t]+tt/2)


def fk(i, j, arr, arr_x, arr_t):
    return -arr[j][i]/tt-f(arr_x[i], arr_t[j] + tt/2)-a*(1-g)*(arr[j][i+1]-2*arr[j][i]+arr[j][i-1])/hh/hh


def SweepMethod(arr, arr_x, arr_t, tLayer, accuracy):
    A = [-c0(accuracy)/b0(accuracy)]
    B = [f0(arr, arr_x, arr_t, tLayer-1, accuracy)/b0(accuracy)]

    for i in range(1, len(arr_x) - 1):  # Без первой и последней точки, так как в них считаются коэффициенты отдельно
        y = bk + ak * A[i-1]
        A += [-ck / y]
        B += [(fk(i, tLayer - 1, arr, arr_x, arr_t)-ak*B[i-1])/y]

    Res = [(fN(arr, arr_x, arr_t, tLayer-1, accuracy) - B[-1] * aN(accuracy)) / (aN(accuracy)*A[-1] + bN(accuracy))]

    for i in range(1, len(arr_x)):
        Res += [B[-i] + A[-i] * Res[i-1]]

    for i in range(len(Res)):
        arr[tLayer][i] = Res[::-1][i]

    # if(tLayer == 2):
    #     print(Res)
    #     print()
    #     print('A: ', A)
    #     print()
    #     print('B: ', B)
    #     print()


def FillArray(arr, arr_x, arr_t, accuracy):
    for i in range(len(arr_x)):
        arr[0][i] = FirstLayer_X(arr_x[i])
    for i in range(1, len(arr_t)):
        SweepMethod(arr, arr_x, arr_t, i, accuracy)


##########################################################


U_O1 = ArrayOfSolving()
#U_O2 = ArrayOfSolving()
exactU = ArrayOfSolving()
erU_O1 = ArrayOfSolving()
#erU_O2 = ArrayOfSolving()

xValue = FillxValue(sizeL, hh)
tValue = FilltValue(sizeT, tt)

FillArray(U_O1, xValue, tValue, 'O1')
#FillArray(U_O2, xValue, tValue, 'O2')
FillExactArray(exactU, xValue, tValue)
FillErArray(U_O1, exactU, erU_O1)
#FillErArray(U_O2, exactU, erU_O2)


print('Первая точность: ', maxValue(erU_O1))
#print('Вторая точность: ', maxValue(erU_O2))