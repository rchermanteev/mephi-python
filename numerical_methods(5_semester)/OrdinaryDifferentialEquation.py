import math as m
import matplotlib.pyplot as plt

#   U'' + (th(x/2)) * U' - cos(x) * U = - sin(x) - 1/2 * sin(2x)
#   U(0) - U'(0) = -1.5       U'(1) = 0.9335
#
#   U'' + p(x) * U' + q(x) * U = f(x)
#   a1*U'(0) + b1*U(0) = c1
#   a2*U'(0) + b2*U(0) = c2


def p(x):
    return m.tanh(x/2)


def q(x):
    return -m.cos(x)


def f(x):
    return - m.sin(x) - 1/2 * m.sin(2*x)


def getExactValue(x):
    return m.sin(x) + m.tanh(x/2)


def get_factor(x, h, name):  # xi : i = 1 .. N-1
    if name == 'a':
        return 1/(h**2) - (m.tanh(x/2))/(2*h)
    elif name == 'b':
        return -2/(h**2) - m.cos(x)
    elif name == 'c':
        return 1/(h**2) + (m.tanh(x/2))/(2*h)
    elif name == 'f':
        return -m.sin(x) - 0.5 * m.sin(2*x)


A_POINT = 0
B_POINT = 1

c1 = -1.5
c2 = 0.9335261723511035
a1 = -1
a2 = 1
b1 = 1
b2 = 0

###########################################################

erO1 = []
erO2 = []
erStep = []

for N_STEP in range(10, 1000):

    h = 1 / N_STEP

    xValue = [(A_POINT + h * i) for i in range(int((B_POINT - A_POINT) / h) + 1)]
    yExactValue = [getExactValue(xValue[i]) for i in range(len(xValue))]

    if xValue[-1] != B_POINT:
        continue

    erStep += [abs(h)]

    A = []
    B = []

    A += [-((-1/h) / ((1/h) + 1))]
    B += [c1 / ((1/h) + 1)]

    for i in range(1, len(xValue) - 1):  # Без первой и последней точки, так как в них считаются коэффициенты отдельно
        y = get_factor(xValue[i], h, 'b') + get_factor(xValue[i], h, 'a') * A[i-1]
        A += [-get_factor(xValue[i], h, 'c') / y]
        B += [(get_factor(xValue[i], h, 'f') - get_factor(xValue[i], h, 'a') * B[i-1]) / y]

    Res = []

    Res += [(c2 - B[-1] * (-1/h)) / ((-1/h)*A[-1] + (1/h))]
    for i in range(1, len(xValue)):
        Res += [B[-i] + A[-i] * Res[i-1]]

    err = [abs(Res[::-1][i] - yExactValue[i]) for i in range(len(Res))]

    ##########################################################

    A2 = []
    B2 = []

    A2 += [-((2/h/h) / (-2/h/h + q(0) + 2*b1/h/a1 - p(0)*b1/a1))]
    B2 += [(f(0) + 2*c1/h/a1 - p(0)*c1/a1) / (-2/h/h + q(0) + 2*b1/h/a1 - p(0)*b1/a1)]

    for i in range(1, len(xValue) - 1):  # Без первой и последней точки, так как в них считаются коэффициенты отдельно
        y = get_factor(xValue[i], h, 'b') + get_factor(xValue[i], h, 'a') * A2[i - 1]
        A2 += [-get_factor(xValue[i], h, 'c') / y]
        B2 += [(get_factor(xValue[i], h, 'f') - get_factor(xValue[i], h, 'a') * B2[i - 1]) / y]

    Res2 = []

    Res2 += [((f(1) - c2*2/a2/h - p(1)*c2/a2) - B2[-1]*(2/h/h))/(A2[-1]*(2/h/h) - 2/h/h + q(1) - 2*b2/a2/h - p(1)*b2/a2)]

    for i in range(1, len(xValue)):
        Res2 += [B2[-i] + A2[-i] * Res2[i - 1]]

    err2 = [abs(Res2[::-1][i] - yExactValue[i]) for i in range(len(Res2))]

    erO1 += [max(err)]
    erO2 += [max(err2)]


tgO1 = (m.log(erO1[-1]) - m.log(erO1[0])) / (m.log(erStep[-1]) - m.log(erStep[0]))
tgO2 = (m.log(erO2[1]) - m.log(erO2[0])) / (m.log(erStep[1]) - m.log(erStep[0]))

print(tgO1, "  ", tgO2)

plt.figure(1)
plt.subplot(2, 1, 1)
plt.loglog(erStep, erO1)
plt.legend(['O1'])
plt.subplot(2, 1, 2)
plt.loglog(erStep, erO2)
plt.legend(['O2'])

plt.show()



#print(m.cos(1)+1/m.cosh(1/2)/m.cosh(1/2)/2)