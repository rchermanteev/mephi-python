import math as m
import matplotlib.pyplot as plt


A_POINT = 2
B_POINT = 4
EXACT_VALUE = (m.log(15) - m.log(255))/4


def my_function(x):
    return x**3 / (1 - x**4)  # 2 <= x <= 4


def getRectangleMethod1(h, y):
    return sum([y[i] * h for i in range(0, len(y) - 2, 2)])


def getRectangleMethod2(h, y):
    return sum([y[i+2] * h for i in range(0, len(y) - 2, 2)])


def getRectangleMethod3(h, x):
    return sum([my_function((x[i+2] + x[i])/2) * h for i in range(0, len(x) - 2, 2)])


def getTrapeziumMethod(h, y):
    return sum([((y[i] + y[i+2]) / 2) * h for i in range(0, len(y) - 2, 2)])


def getSimpsonsMethod(h, y):
    return sum([(y[i-1] + 4 * y[i] + y[i+1]) * h/3 for i in range(1, len(y) - 1, 2)])


def getGaussMethod(x):
    w = [1, 1]
    xw = [-3 ** -0.5, 3 ** -0.5]
    I = 0
    for i in range(0, len(x) - 2, 2):
        for j in range(2):
            I += (x[i + 2] - x[i])/2 * w[j] * my_function((x[i + 2] + x[i])/2 + (x[i + 2] - x[i])/2 * xw[j])
    return I

##################


er_rectangleMethod1 = []
er_rectangleMethod2 = []
er_rectangleMethod3 = []
er_trapeziumMethod = []
er_simpsonMethod = []
er_gaussMethod = []
erStep = []

for n_step in range(10, 1000):

    sizeInter = B_POINT - A_POINT
    step = float(sizeInter/(n_step - 1.0))  # шаг разбиения
    sizeAr = sizeInter / (step*0.5)
    xValue = [float(A_POINT + step/2 * i) for i in range(0, (int(sizeAr) + 1))]

    if xValue[-1] != B_POINT: continue

    yValue = [my_function(i) for i in xValue]

    rectangleMethod1 = getRectangleMethod1(step, yValue)
    rectangleMethod2 = getRectangleMethod2(step, yValue)
    rectangleMethod3 = getRectangleMethod3(step, xValue)
    trapeziumMethod = getTrapeziumMethod(step, yValue)
    simpsonMethod = getSimpsonsMethod(step/2, yValue)
    gaussMethod = getGaussMethod(xValue)

    erStep += [abs(step)]

    d_rectangleMethod1 = abs(rectangleMethod1 - EXACT_VALUE)
    er_rectangleMethod1 += [d_rectangleMethod1]

    d_rectangleMethod2 = abs(rectangleMethod2 - EXACT_VALUE)
    er_rectangleMethod2 += [d_rectangleMethod2]

    d_rectangleMethod3 = abs(rectangleMethod3 - EXACT_VALUE)
    er_rectangleMethod3 += [d_rectangleMethod3]

    d_trapeziumMethod = abs(trapeziumMethod - EXACT_VALUE)
    er_trapeziumMethod += [d_trapeziumMethod]

    d_simpsonMethod = abs(simpsonMethod - EXACT_VALUE)
    er_simpsonMethod += [d_simpsonMethod]

    d_gaussMethod = abs(gaussMethod - EXACT_VALUE)
    er_gaussMethod += [d_gaussMethod]

print("точное значение", EXACT_VALUE)
# Зависимость ошибки от шага для интеграла посчитанного соответствующим методом


plt.figure("Зависимость ошибки от шага")
plt.subplot(3, 2, 1)
plt.plot(erStep, er_rectangleMethod1)
plt.legend(['Левый метод прямоугольников'])
plt.subplot(3, 2, 2)
plt.plot(erStep, er_rectangleMethod2)
plt.legend(['Правый метод прямоугольников'])
plt.subplot(3, 2, 3)
plt.plot(erStep, er_rectangleMethod3)
plt.legend(['Средний метод прямоугольников'])
plt.subplot(3, 2, 4)
plt.plot(erStep, er_trapeziumMethod)
plt.legend(['Метод трапеций'])
plt.subplot(3, 2, 5)
plt.plot(erStep, er_simpsonMethod)
plt.legend(['Метод Симпсона'])
plt.subplot(3, 2, 6)
plt.plot(erStep, er_gaussMethod)
plt.legend(['Метод Гаусса'])


# Логарифмическая зависимость ошибки от шага для интеграла посчитанного соответствующим методом

plt.figure("Логарифмическая зависимость ошибки от шага")
plt.subplot(3, 2, 1)
plt.loglog(erStep, er_rectangleMethod1)
plt.legend(['Левый метод прямоугольников'])
plt.subplot(3, 2, 2)
plt.loglog(erStep, er_rectangleMethod2)
plt.legend(['Правый метод прямоугольников'])
plt.subplot(3, 2, 3)
plt.loglog(erStep, er_rectangleMethod3)
plt.legend(['Средний метод прямоугольников'])
plt.subplot(3, 2, 4)
plt.loglog(erStep, er_trapeziumMethod)
plt.legend(['Метод трапеций'])
plt.subplot(3, 2, 5)
plt.loglog(erStep, er_simpsonMethod)
plt.legend(['Метод Симпсона'])
plt.subplot(3, 2, 6)
plt.loglog(erStep, er_gaussMethod)
plt.legend(['Метод Гаусса'])

plt.show()
