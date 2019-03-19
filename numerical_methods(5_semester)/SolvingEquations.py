import math as m

A_POINT = 0
B_POINT = 10
EXACT_VALUE = 0

def getFunction(x):
    return x**5 - x**4 - x**2 - 1


def getSolving(accuracy, a, b):
    if getFunction(a) * getFunction(b) < 0:
        solv = []

        for i in range(m.ceil(m.log((b - a) / accuracy, 2))):
            solv += [a + (b - a) / 2]
            if getFunction(solv[i]) * getFunction(b) < 0:
                a = solv[i]
            elif getFunction(solv[i]) * getFunction(a) < 0:
                b = solv[i]
            elif getFunction(solv[i]) == 0:
                return solv
        print("Количество итераций", i)
        return solv


def getdFunction(x):
    return 5*x**4 - 4*x**3 - 2*x


def getd2Function(x):
    return 20*x**3 - 12*x**2 - 2


def getNewtonMethod(accuracy, a, b):
    xn = []
    if getdFunction(a) * getdFunction(b) > 0:
        return
    else:
        if getdFunction(a) * getd2Function(a) > 0:
            x0 = a
        elif getdFunction(b) * getd2Function(b) > 0:
            x0 = b
        xn += [x0 - getFunction(x0)/getdFunction(x0)]
        i = 0
        while getFunction(xn[i]) > accuracy:
            x0 = xn[i]
            xn += [x0 - getFunction(x0) / getdFunction(x0)]
            i += 1
        print("Количество итераций", i)

        return xn


#########################
e3 = 10 ** -3
e6 = 10 ** -6
e9 = 10 ** -9
e = 10 ** -16

print("\nМетод Дихотомии")
print("Решение х= ", getSolving(e3, A_POINT, B_POINT)[-1])
print("Решение х= ", getSolving(e6, A_POINT, B_POINT)[-1])
print("Решение х= ", getSolving(e9, A_POINT, B_POINT)[-1])
print("Точное решение х= ", getSolving(e, A_POINT, B_POINT)[-1])
print("\nМетод Ньютона")
print("Решение х= ", getNewtonMethod(e3, A_POINT, B_POINT)[-1])
print("Решение х= ", getNewtonMethod(e6, A_POINT, B_POINT)[-1])
print("Решение х= ", getNewtonMethod(e9, A_POINT, B_POINT)[-1])
print("Точное решение х= ", getSolving(e, A_POINT, B_POINT)[-1])


# Скорость сходимости

xValueDichotomy = getSolving(e3, A_POINT, B_POINT)
xValueNewton = getNewtonMethod(e6, A_POINT, B_POINT)


xExactValue = getSolving(e, A_POINT, B_POINT)[-1]

rateOfConvergenceD = (m.log(abs(xValueDichotomy[-1] - xExactValue)) - m.log(abs(xValueDichotomy[2] - xExactValue))) / \
                    (m.log(abs(xValueDichotomy[-2] - xExactValue)) - m.log(abs(xValueDichotomy[1] - xExactValue)))

rateOfConvergenceN = (m.log(abs(xValueNewton[-1] - xExactValue)) - m.log(abs(xValueNewton[2] - xExactValue))) / \
                    (m.log(abs(xValueNewton[-2] - xExactValue)) - m.log(abs(xValueNewton[1] - xExactValue)))

print('Скорость сходимости метода Дихотомии: ', rateOfConvergenceD)
print('Скорость сходимости метода Ньютона: ', rateOfConvergenceN)


