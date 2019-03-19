import math as m

#  U'' + (th(x/2)) * U' - cos(x) * U = - sin(x) - 1/2 * sin(2x)
#  U(0) = 0       U'(0) = 3/2

def getExactValue(x):
    return m.sin(x) + m.tanh(x/2)


def getFunction(x,y1,y2):
    return -m.sin(x) - 1/2 * m.sin(x*2) + m.cos(x) * y1 - m.tanh(x/2) * y2


def getEulerMethod(x):
    y10 = [0.0]  # y1(0) = 0
    y20 = [1.5]  # y2(0) = 3/2

    h = x[1] - x[0]

    for i in range(len(x) - 1):
        y1 = y10[i] + h * y20[i]
        y2 = y20[i] + h * getFunction(x[i], y10[i], y20[i])
        y10 += [y1]
        y20 += [y2]
    return y10


def getRungeKuttaMethod(x):
    y10 = [0.0]  # y1(0) = 0
    y20 = [1.5]  # y2(0) = 3/2

    h = x[1] - x[0]

    for i in range(len(x) - 1):

        k11 = y20[i]
        k21 = getFunction(x[i], y10[i], y20[i])

        k12 = y20[i] + h/2 * k21
        k22 = getFunction(x[i] + h / 2, y10[i] + h / 2 * k11, y20[i] + h / 2 * k21)

        k13 = y20[i] + h/2 * k22
        k23 = getFunction(x[i] + h / 2, y10[i] + h / 2 * k12, y20[i] + h / 2 * k22)

        k14 = y20[i] + h * k23
        k24 = getFunction(x[i] + h, y10[i] + h * k13, y20[i] + h * k23)

        k10 = (1/6) * (k11 + 2 * k12 + 2 * k13 + k14)

        y1 = y10[i] + h * k10

        k20 = (1/6) * (k21 + 2 * k22 + 2 * k23 + k24)

        y2 = y20[i] + h * k20

        y10 += [y1]
        y20 += [y2]

    return y10


def getAdamsMethod(x):
    y10 = [0.0]  # y1(0) = 0
    y20 = [1.5]  # y2(0) = 3/2

    h = x[1] - x[0]

    for i in range(3):

        k11 = y20[i]
        k21 = getFunction(x[i], y10[i], y20[i])

        k12 = y20[i] + h / 2 * k21
        k22 = getFunction(x[i] + h / 2, y10[i] + h / 2 * k11, y20[i] + h / 2 * k21)

        k13 = y20[i] + h / 2 * k22
        k23 = getFunction(x[i] + h / 2, y10[i] + h / 2 * k12, y20[i] + h / 2 * k22)

        k14 = y20[i] + h * k23
        k24 = getFunction(x[i] + h, y10[i] + h * k13, y20[i] + h * k23)

        k10 = (1 / 6) * (k11 + 2 * k12 + 2 * k13 + k14)

        y1 = y10[i] + h * k10

        k20 = (1 / 6) * (k21 + 2 * k22 + 2 * k23 + k24)

        y2 = y20[i] + h * k20

        y10 += [y1]
        y20 += [y2]
    for i in range(3, len(x) - 1):
        y10 += [y10[i] + h * (55/24 * y20[i] - 59/24 * y20[i-1] + 37/24 * y20[i-2] - 9/24 * y20[i-3])]
        y20 += [y20[i] + h * (55/24 * getFunction(x[i], y10[i], y20[i]) -
                              59/24 * getFunction(x[i-1], y10[i-1], y20[i-1]) +
                              37/24 * getFunction(x[i-2], y10[i-2], y20[i-2]) -
                              9/24 * getFunction(x[i-3], y10[i-3], y20[i-3]))]

    return  y10


STEP = 0.05
A_POINT = 0
B_POINT = 1


###########################################################


xValue = [(A_POINT + STEP * i) for i in range(int((B_POINT - A_POINT) / STEP) + 1)]
yExactValue = [getExactValue(xValue[i]) for i in range(len(xValue))]
print('\n')
print('Точное значение: ', yExactValue, '\n')
print('Метод Эйлера: ', getEulerMethod(xValue), '\n')
print('Метод Рунге-Кутта: ', getRungeKuttaMethod(xValue), '\n')
print('Метод Адамса: ', getAdamsMethod(xValue), '\n')


# Оценка порядка точности для метода Рунге-Кутта О(р^4)

xValueRunge = [(A_POINT + STEP*2 * i) for i in range(int((B_POINT - A_POINT) / (STEP*2)) + 1)]
yExactValueRunge = [getExactValue(xValue[i]) for i in range(len(xValue))]

yStep = getRungeKuttaMethod(xValue)  # Значения на сетке с шагом 0.05
y2Step = getRungeKuttaMethod(xValueRunge)  # Значения на сетке с шагом 0.10

# print(yStep)
# print(y2Step)

p = []  # Порядок точности
for i in range(1, len(xValueRunge)):  # Первое значение точный 0
    p += [m.log(((yStep[2*i] - y2Step[i]) / (yExactValueRunge[i] - yStep[2*i]) + 1), 2)]

print(p, '\n')
print('Ожидаемый порядок точности', STEP**4, '\n')

_p = 4
O5 = []
for i in range(0, len(xValueRunge)):  # Первое значение точный 0
    O5 += [pow(abs((yExactValueRunge[2*i] - yStep[2*i]-(yStep[2*i] - y2Step[i])/(2**_p - 1))),1/5)]


errEulerMethod = []
errRungeKuttaMethod = []
errAdamsMethod = []

for i in range(len(yExactValue)):
    errEulerMethod += [pow(abs(getEulerMethod(xValue)[i]-yExactValue[i]),1/2)]
    errRungeKuttaMethod += [pow(abs(getRungeKuttaMethod(xValue)[i]-yExactValue[i]),1/4)]
    errAdamsMethod += [pow(abs(getAdamsMethod(xValue)[i]-yExactValue[i]),1/3)]

print('Ошибка Метода Эйлера: ', errEulerMethod, '\n')
print('Ошибка Метода Рунге-Кутта: ', errRungeKuttaMethod, '\n')
print('Ошибка Метода Адамса: ', errAdamsMethod, '\n')
print('Поправка Рунге: ', O5, '\n')




