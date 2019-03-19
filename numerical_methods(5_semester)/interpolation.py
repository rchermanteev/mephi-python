import math
import matplotlib.pyplot as plt


def function(x):
    return 5 / (2 + x + math.cos(x) * math.log(1 + x))


def polynomLagrange(x, y, t):
    res = 0
    for i in range(len(y)):
        numerator = 1  # числитель
        denominator = 1  # знаменатель
        for j in range(len(x)):
            if i != j:
                numerator *= (t - x[j])
                denominator *= (x[i] - x[j])
        res += y[i]*(numerator/denominator)
    return res


def Cheb(n, a , b):
    return [math.cos((2*i + 1)/(2*n)*math.pi)*(b - a)/2 + (a + b)/2 for i in range(n)]


def mergeArrEv(a, b):
    c = []
    for i in range(len(a) - 1):
        c += [a[i]]
        c += [b[i]]
    c += [a[-1]]
    return c

def mergeArrCh(a, b):
    c = []
    for i in range(len(a)):
        c += [a[i]]
        c += [b[i]]
    c += [b[-1]]
    return c


aPoint = float(input("Введите начальную точку интервала: "))
bPoint = float(input("Введите конечную точку интервала: "))
n_step = float(input("Введите количество точек в интервале: "))
n = int(input('Введите число корней полинома Чебышева: '))

sizeInter = bPoint - aPoint

step = float(sizeInter/n_step)

sizeAr = sizeInter / step  # размер массива для xValue

xValue = [float(aPoint + step * i) for i in range(0, int(sizeAr) + 1)]  # +1, тк тип float даёт не точное число
yValue = [function(i) for i in xValue]

# Точки для узлов интерполяции с равномерным шагом
xEv = [float(xValue[i] + step/2) for i in range(len(xValue) - 1)]
yEv = [polynomLagrange(xValue, yValue, xEv[i]) for i in range(len(xEv))]


# Точки для узлов интерполяции из полинома Чебышева
xChebNode = Cheb(n, aPoint, bPoint)
yChebNode = [function(i) for i in xChebNode]
xCheb = [float(xChebNode[i] + step/2) for i in range(len(xChebNode) - 1)]
yCheb = [polynomLagrange(xChebNode, yChebNode, xCheb[i]) for i in range(len(xCheb))]


m_xEv = mergeArrEv(xValue, xEv)
m_yEv = mergeArrEv(yValue, yEv)

m_xCheb = mergeArrCh(xCheb, xChebNode)
m_yCheb = mergeArrCh(yCheb, yChebNode)

print(mergeArrCh(xEv, xValue))
print(xValue)
print(xEv)

plt.figure(1)
plt.subplot(1, 3, 1)
plt.plot(xValue, yValue, "-ro")
plt.legend(['Обычный график'])

plt.subplot(1, 3, 2)
plt.plot(m_xEv, m_yEv, "r-")
plt.plot(xValue, yValue, "ro")
plt.legend(['Равномерный шаг'])

plt.subplot(1, 3, 3)
plt.plot(m_xCheb, m_yCheb, "r-")
plt.plot(xCheb, yCheb, "ro")
plt.legend(['Полином Чебышева'])

plt.figure(2)
error = [(abs(function(m_xEv[i]) - m_yEv[i])) for i in range(len(m_xEv))]
plt.plot(m_xEv, error)
plt.legend(['Ошибка'])



plt.show()
