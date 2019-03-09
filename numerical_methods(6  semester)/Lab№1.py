"""
 Решение уравнение переноса Ut + a*Ux = 0 на отрезке 0<=x<=1 0<=t<=2
 для для трех видов начальных условий : а) гауссовский импульс, б) ступенька, в) прямоугольный импульс.
"""


from math import *
import matplotlib.pyplot as plt


"""
NUMBER_SIGN("negative", "positive") - определяет знак а в уравнении(соответственно направление движения импульса). 
NAME("Gauss", "Step", "SqPulse") - определяет вид импульса(вид начальных условий)
TEMPLATE("2", "4", "9", "15") - определяет разностную схему (2-правый явный уголок, 4-правый неявный уголок), 
9 - "Z-схема", 15 - схема "Кабаре"

 Схема 2: Устойчива при Q <= 1 и a < 0
 Схема 4: Устойчива при Q >= 1 и a > 0
 Схема 9; Устойчива при Q > 0 (В теории абсолютно устойчива)
 Схема 15: Устойчива при -1<=a<0 (a = -1, -0.5 схема точная)
"""


# Данные задачи
NUMBER_SIGN = "negative"
NAME = "Gauss"
TEMPLATE = "15"
# Параметры для гауссовского импульса
X0 = 0.5
DIS = 0.2
# Параметры для Прямоугольного импульса
WIDTH = 0.13

##########################################

a = 1 if NUMBER_SIGN == "positive" else -1
hh = 0.05  # Шаг по координате   0.005
tt = 0.05  # Шаг по времени   0.005
T = 5  # Граница по времени   2
L = 5  # Граница по координате  1

sizeL = int(L / hh) + 1
sizeT = int(T / tt) + 1


def getExactValueGauss(x, t, number_sign):  # для чёт и нечёт
    if number_sign == "negative":
        return exp((-1) * (x - X0 - a * t) ** 2 / DIS / DIS)
    elif number_sign == "positive":
        return exp((-1) * (x - X0 - a * t) ** 2 / DIS / DIS)


def getExactValueStep(x, t, number_sign):
    if number_sign == "negative":
        if x - L >= a*t:
            return 1
        elif x - L < a*t:
            return 0
    elif number_sign == "positive":
        if x <= a*t:
            return 1
        elif x > a*t:
            return 0


def getExactValueSqPulse(x, t, number_sign):
    if number_sign == "negative":
        if (x - a * t - L >= -1 / a * WIDTH) or (x - a * t - L < 1 / a * WIDTH):
            return 0
        elif 1/a*WIDTH <= x-a*t - L < -1/a*WIDTH:
            return 1
    elif number_sign == "positive":
        if (x - a * t < -1 / a * WIDTH) or (x - a * t >= 1 / a * WIDTH):
            return 0
        elif -1/a*WIDTH <= x-a*t < 1/a*WIDTH:
            return 1


def BoundaryCondition(t, name, number_sign):
    if name == "Gauss":
        if number_sign == "negative":
            return exp((-1) * (L - X0 - a * t) ** 2 / DIS / DIS)
        elif number_sign == "positive":
            return exp((-1) * (- X0 - a * t) ** 2 / DIS / DIS)
    elif name == "Step":
        if number_sign == "negative":
            if L - L >= a * t:
                return 1
            elif L - L < a * t:
                return 0
        elif number_sign == "positive":
            if 0 <= a * t:
                return 1
            elif 0 > a * t:
                return 0
    elif name == "SqPulse":
        if number_sign == "negative":
            if (L - a * t - L >= -1 / a * WIDTH) or (L - a * t - L < 1 / a * WIDTH):
                return 0
            elif 1 / a * WIDTH < L - a * t - L <= -1 / a * WIDTH:
                return 1
        elif number_sign == "positive":
            if (0 - a * t <= -1 / a * WIDTH) or (0 - a * t > 1 / a * WIDTH):
                return 0
            elif -1 / a * WIDTH < 0 - a * t <= 1 / a * WIDTH:
                return 1


def InitialCondition(x, name, number_sign):
    if name == "Gauss":
        if number_sign == "negative":
            return exp((-1) * (x - X0) ** 2 / DIS / DIS)
        elif number_sign == "positive":
            return exp((-1) * (x - X0) ** 2 / DIS / DIS)
    elif name == "Step":
        if number_sign == "negative":
            if x - L >= 0:
                return 1
            elif x - L < 0:
                return 0
        elif number_sign == "positive":
            if x <= 0:
                return 1
            elif x > 0:
                return 0
    elif name == "SqPulse":
        if number_sign == "negative":
            if (x - a * 0 - L >= -1 / a * WIDTH) or (x - a * 0 - L < 1 / a * WIDTH):
                return 0
            elif 1 / a * WIDTH < x - a * 0 - L <= -1 / a * WIDTH:
                return 1
        elif number_sign == "positive":
            if (x - a * 0 <= -1 / a * WIDTH) or (x - a * 0 > 1 / a * WIDTH):
                return 0
            elif -1 / a * WIDTH < x - a * 0 <= 1 / a * WIDTH:
                return 1


def FillxValue(sizeL, hh):
    return [0 + hh * i for i in range(sizeL)]


def FilltValue(sizeT, tt):
    return [0 + tt * i for i in range(sizeT)]


def viewArray(arr):
    for i in range(len(arr)):
        for j in range(len(arr[0])):
            print(arr[i][j], end=' | ')
        print()


def FillExactArray(arr, arr_x, arr_t, name, number_sign):
    for j in range(len(arr)):
        for i in range(len(arr[j])):
            if name == "Gauss":
                arr[j][i] = getExactValueGauss(arr_x[i], arr_t[j], number_sign)
            elif name == "Step":
                arr[j][i] = getExactValueStep(arr_x[i], arr_t[j], number_sign)
            elif name == "SqPulse":
                arr[j][i] = getExactValueSqPulse(arr_x[i], arr_t[j], number_sign)


def ArrayOfSolving():
    r = 0
    mas = []
    for i in range(sizeT):
        mas.append([])
        for j in range(sizeL):
            mas[i].append(r)
    return mas


"""
 Схема 2: Устойчива при Q <= 1 и a < 0
 Схема 4: Устойчива при Q >= 1 и a > 0
 Схема 9; Устойчива при Q > 0 (В теории абсолютно устойчива)
 Схема 15: Устойчива при -1<=a<0 (a = -1, -0.5 схема точная)
"""


def Template(num_template, arr, number_sign):
    if num_template == "2":
        if number_sign == "negative":
            for j in range(len(arr) - 1):
                for i in range(len(arr[j]) - 1):
                    arr[j + 1][i] = -a * tt / hh * (arr[j][i + 1] - arr[j][i]) + arr[j][i]
        elif number_sign == "positive":
            for j in range(len(arr) - 1):
                for i in range(len(arr[j]) - 1):
                    arr[j + 1][i] = -a * tt / hh * (arr[j][i + 1] - arr[j][i]) + arr[j][i]

    elif num_template == "4":
        if number_sign == "negative":
             for j in range(len(arr) - 1):
                 for i in range(len(arr[j]) - 1):
                    arr[j+1][i] = (arr[j][i]/tt - a/hh*arr[j+1][i+1])/(1/tt-a/hh)
        elif number_sign == "positive":
            for j in range(len(arr) - 1):
                for i in range(len(arr[j]) - 1):
                    arr[j + 1][i + 1] = -hh / a / tt * (arr[j + 1][i] - arr[j][i]) + arr[j + 1][i]

    elif num_template == "9":  # Доопределяем точки, используя схему "Подкова"
        if number_sign == "negative":  # Вообще, она должна быть абсолютно устойчивой
            for j in range(len(arr) - 1):
                arr[j + 1][-2] = -a * tt / hh * (arr[j][-1] - arr[j][-2]) + arr[j][-2]
                #arr[j+1][-2]=(arr[j+1][-1]-arr[j][-1])*2*hh/a/tt+(arr[j][-1]-arr[j][-2])+arr[j+1][-1]  # Схема подкова
                for i in range(len(arr[j]) - 1, 0, -1):
                    arr[j+1][i-1]=(arr[j+1][i]-arr[j][i])*2*hh/tt/a+(arr[j+1][i]+arr[j][i]-arr[j][i-1])
        elif number_sign == "positive":
            for j in range(len(arr) - 1):
                arr[j + 1][-1] = -hh / a / tt * (arr[j + 1][-2] - arr[j][-2]) + arr[j + 1][-2]
                #arr[j+1][-1]=(arr[j][-1]/tt+a/2/hh*arr[j+1][-2]-a/2/hh*(arr[j][-1]-arr[j][-2]))/(1/tt+a/2/hh)
                for i in range(1, len(arr[j]) - 1):
                    arr[j + 1][i] = (arr[j][i]/tt-a/2/hh*(arr[j][i+1]-arr[j][i])+a/2/hh*arr[j+1][i-1])/(1/tt+a/2/hh)

    elif num_template == "15":  # Второй слой можно посчитать уголком(при a=1, чтобы получить точное решение)
        if number_sign == "negative":  # Устойчива при -1<=a<0 (a = -1, -0.5 схема точная)
            # Первый слой заполняем схемой 2 при а=-1
            for i in range(len(arr[0]) - 1):
                arr[0 + 1][i] = -a * tt / hh * (arr[0][i + 1] - arr[0][i]) + arr[0][i]
            for j in range(1, len(arr) - 1):
                for i in range(len(arr[j])-1, 0, -1):
                    arr[j + 1][i - 1] = -2 * a * tt / hh * (arr[j][i] - arr[j][i - 1]) - (arr[j][i] - arr[j - 1][i]) + \
                                        arr[j][i - 1]
        elif number_sign == "positive":
            # Первый слой заполняем схемой 4 при а=1
            for i in range(len(arr[0]) - 1):
                arr[0 + 1][i + 1] = -hh / a / tt * (arr[0 + 1][i] - arr[0][i]) + arr[0 + 1][i]
            for j in range(1, len(arr) - 1):
                for i in range(1, len(arr[j])):
                    arr[j+1][i-1] = -2*a*tt/hh*(arr[j][i]-arr[j][i-1])-(arr[j][i]-arr[j-1][i])+arr[j][i-1]


def FillArray(arr, arr_x, arr_t, name, number_sign, template):
    for i in range(len(arr_x)):
        arr[0][i] = InitialCondition(arr_x[i], name, number_sign)

    if number_sign == "negative":
        for j in range(len(arr_t)):
            arr[j][-1] = BoundaryCondition(arr_t[j], name, number_sign)
    elif number_sign == "positive":
        for j in range(len(arr_t)):
            arr[j][0] = BoundaryCondition(arr_t[j], name, number_sign)

    Template(template, arr, number_sign)


#########################################################


U_Exact = ArrayOfSolving()
U_Num = ArrayOfSolving()

xValue = FillxValue(sizeL, hh)
tValue = FilltValue(sizeT, tt)

FillExactArray(U_Exact, xValue, tValue, NAME, NUMBER_SIGN)
FillArray(U_Num, xValue, tValue, NAME, NUMBER_SIGN, TEMPLATE)


plt.ion()
for i in range(len(U_Exact)):
    plt.clf()
    plt.plot(xValue, U_Exact[i], 'b')
    plt.plot(xValue, U_Num[i], 'r')
    plt.ylim(-1, 3)
    plt.pause(0.01)
    plt.draw()
plt.ioff()


viewArray(U_Num)
print()
viewArray(U_Exact)
