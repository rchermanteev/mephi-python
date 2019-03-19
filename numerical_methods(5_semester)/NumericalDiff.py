import math as m
import matplotlib.pyplot as plt


def my_function(x):
    return m.cosh(m.sin(x))  # -1.5 <= x <= 1.5


def my_diff1(x):
    return m.cos(x) * m.sinh(m.sin(x))


def my_diff2(x):
    return (m.cos(x)**2) * m.cosh(m.sin(x)) - m.sinh(m.sin(x)) * m.sin(x)


def first_diff(k, f1, f2, f3, h):  # k -- kind;
    if k == 'c2':
        return (f2 - f1)/(h*2)  # (f(l+1) - f(l-1))/(2*h)
    elif k == 'r1':
        return (f2 - f1)/h  # (f(l+1) - f(l))/h
    elif k == 'l1':
        return (f1 - f2)/h  # (f(l) - f(l-1))/h
    elif k == 'r2':
        return (-3*f1 + 4*f2 - f3)/(h*2)  # (-3*f(l) + 4*f(l+1) - f(l+2))/(2*h)
    elif k == 'l2':
        return (3*f1 - 4*f2 + f3)/(h*2)  # (3*f(l) - 4*f(l-1) + f(l-2))/(2*h)


def second_diff(k, f1, f2, f3, f4, f5, h):
    if k == 'c2':
        return (f1 - 2*f2 + f3)/(h**2)  # (f(l+1) - 2*f(l) + f(l-1))/(h**2)
    elif k == 'r2':
        return (2*f1 - 5*f2 + 4*f3 - f4)/(h**2)  # (2*f(l) - 5*f(l+1) + 4*f(l+2) - f(l+3))/(h**2)
    elif k == 'l2':
        return (2*f1 - 5*f2 + 4*f3 - f4)/(h**2)  # (2*f(l) - 5*f(l-1) - 4*f(l-2) - f(l-3))/(h**2)
    if k == 'c4':
        return (-f1 + 16*f2 - 30*f3 + 16*f4 - f5)/(h**2 * 12)  # (-f(l-2)+16*f(l-1)-30*f(l)+16*f(l+1)-f(l+2))/(12*h**2)


A_POINT = -1.5
B_POINT = 1.5

##############################

erFirstDiff_01 = []
erFirstDiff_02 = []
erSecondDiff_02 = []
erSecondDiff_04 = []

erStep = []


for n_step in range(10, 1000):

        sizeInter = B_POINT - A_POINT

        step = float(sizeInter/n_step)

        sizeAr = sizeInter / step  # размер массива для xValue

        xValue = [float(A_POINT + step * i) for i in range(0, int(sizeAr) + 1)]  # +1, тк тип float даёт не точное число
        yValue = [my_function(i) for i in xValue]
        y_my_diff1 = [my_diff1(i) for i in xValue]
        y_my_diff2 = [my_diff2(i) for i in xValue]

        erStep += [abs(step)]

        # Считаем первую производнцю с точностью h

        yFirstDiff_o1 = [first_diff('r1', yValue[i], yValue[i + 1], 0, step) for i in range(len(yValue) - 1)]
        yFirstDiff_o1 += [first_diff('l1', yValue[-1], yValue[-2], 0, step)]

        # Считаем первую производную с точностью h^2

        yFirstDiff_o2 = [first_diff('r2', yValue[i], yValue[i + 1], yValue[i + 2], step) for i in range(len(yValue) - 2)]
        yFirstDiff_o2 += [first_diff('l2', yValue[-2], yValue[-3], yValue[-4], step)]
        yFirstDiff_o2 += [first_diff('l2', yValue[-1], yValue[-2], yValue[-3], step)]

        # Считаем вторую производную с точностью h^2

        ySecondDiff_o2 = [second_diff('r2', yValue[i], yValue[i + 1], yValue[i + 2], yValue[i + 3], 0, step) for i in
                          range(len(yValue) - 3)]
        ySecondDiff_o2 += [second_diff('l2', yValue[-3], yValue[-4], yValue[-5], yValue[-6], 0, step)]
        ySecondDiff_o2 += [second_diff('l2', yValue[-2], yValue[-3], yValue[-4], yValue[-5], 0, step)]
        ySecondDiff_o2 += [second_diff('l2', yValue[-1], yValue[-2], yValue[-3], yValue[-4], 0, step)]

        # Считаем вторую производную с точностью h^4

        ySecondDiff_o4 = [second_diff('c4', yValue[i], yValue[i + 1], yValue[i + 2], yValue[i + 3], yValue[i + 4], step) for
                          i in range(len(yValue) - 4)]
        ySecondDiff_o4.insert(0, second_diff('c4', my_function(A_POINT - step), yValue[0], yValue[1], yValue[2], yValue[3],
                                             step))
        ySecondDiff_o4.insert(0, second_diff('c4', my_function(A_POINT - 2 * step), my_function(A_POINT - step), yValue[0],
                                             yValue[1], yValue[2], step))
        ySecondDiff_o4.append(
            second_diff('c4', yValue[-4], yValue[-3], yValue[-2], yValue[-1], my_function(xValue[-1] + step), step))
        ySecondDiff_o4.append(second_diff('c4', yValue[-3], yValue[-2], yValue[-1], my_function(xValue[-1] + step),
                                          my_function(xValue[-1] + 2 * step), step))

        ###############################################

        d_firstDiff_01 = [(abs(yFirstDiff_o1[i] - y_my_diff1[i])) for i in range(len(yValue))]
        erFirstDiff_01 += [max(d_firstDiff_01)]

        d_firstDiff_02 = [(abs(yFirstDiff_o2[i] - y_my_diff1[i])) for i in range(len(yValue))]
        erFirstDiff_02 += [max(d_firstDiff_02)]

        d_secondDiff_02 = [(abs(ySecondDiff_o2[i] - y_my_diff2[i])) for i in range(len(yValue))]
        erSecondDiff_02 += [max(d_secondDiff_02)]

        d_secondDiff_04 = [(abs(ySecondDiff_o4[i] - y_my_diff2[i])) for i in range(len(yValue))]
        erSecondDiff_04 += [max(d_secondDiff_04)]

# print(len(erStep), len(erFirstDiff_01))
# print(erStep)
# print(erFirstDiff_01)

# print(ySecondDiff_o2)
# print(ySecondDiff_o4)
# print(y_my_diff2)


print('Первая производная О1 tgx = ', (m.log(erFirstDiff_01[len(yValue)//2 + 1]) - m.log(erFirstDiff_01[len(yValue)//2])) / (m.log(erStep[len(yValue)//2 + 1]) - m.log(erStep[len(yValue)//2])))
print('Первая производная О2 tgx = ', (m.log(erFirstDiff_02[len(yValue)//2 + 1]) - m.log(erFirstDiff_02[len(yValue)//2])) / (m.log(erStep[len(yValue)//2 + 1]) - m.log(erStep[len(yValue)//2])))
print('Вторая производная О2 tgx = ', (m.log(erSecondDiff_02[len(yValue)//2 + 1]) - m.log(erSecondDiff_02[len(yValue)//2])) / (m.log(erStep[len(yValue)//2 + 1]) - m.log(erStep[len(yValue)//2])))
print('Вторая производная О4 tgx = ', (m.log(erSecondDiff_04[len(yValue)//2 + 40]) - m.log(erSecondDiff_04[len(yValue)//2])) / (m.log(erStep[len(yValue)//2 + 40]) - m.log(erStep[len(yValue)//2])))



plt.figure("Зависимость ошибки от шага")
plt.subplot(2, 2, 1)
plt.plot(erStep, erFirstDiff_01)
plt.legend(['Первая производная О1'])
plt.subplot(2, 2, 2)
plt.plot(erStep, erFirstDiff_02)
plt.legend(['Первая производная О2'])
plt.subplot(2, 2, 3)
plt.plot(erStep, erSecondDiff_02)
plt.legend(['Вторая производная О2'])
plt.subplot(2, 2, 4)
plt.plot(erStep, erSecondDiff_04)
plt.legend(['Вторая производная О4'])

plt.figure("Логарифмическая зависимость ошибки от шага")
plt.subplot(2, 2, 1)
plt.loglog(erStep, erFirstDiff_01)
plt.legend(['Первая производная О1'])
plt.subplot(2, 2, 2)
plt.loglog(erStep, erFirstDiff_02)
plt.legend(['Первая производная О2'])
plt.subplot(2, 2, 3)
plt.loglog(erStep, erSecondDiff_02)
plt.legend(['Вторая производная О2'])
plt.subplot(2, 2, 4)
plt.loglog(erStep, erSecondDiff_04)
plt.legend(['Вторая производная О4'])

plt.show()





