import math as m

hh = 0.05  # Шаг по координате
tt = 0.05  # Шаг по времени
T = 1  # Граница по времени
L = 1  # Граница по координате
sizeL = int(L / hh) + 1
sizeT = int(T / tt) + 1


# Utt = a * Uxx + f(x,t)    0<t<=T     0<x<L
# a1 * U(0,t) + b1 * Ux(0,t) = c1
# a2 * U(L,t) + b2 * Ux(L,t) = c2
# U(x,0) = d1
# Ut(x,0) = d2


a1 = 0; b1 = 1
a2 = 1; b2 = 0


a = 1/2

d12 = 2  # Вторая производная d1


def getExactValue(x, t):
    return (x - t)**2 + 1/(2*m.cos(x*t))


def d1(x):
    return x*x + 1/2


def d2(x):
    return -2*x


def c1(t):
    return -2*t


def c2(t):
    return (1 - t)*(1 - t) + 1 / (2 * m.cos(t))


def f(x, t):
    return 1 + (2*x*x-t*t)*(1+2*(m.tan(x*t))**2)/(4*m.cos(x*t))


def xValue(sizeL, hh):
    return [0 + hh * i for i in range(sizeL)]


def tValue(sizeT, tt):
    return [0 + tt * i for i in range(sizeT)]


def SecondLayer_X(x, accuracy):
    if accuracy == "O1":
        return tt * d2(x) + d1(x)
    elif accuracy == "O2":
        return d1(x) + d2(x) * tt + tt * tt / 2 * (a * d12 + f(x, 0))


def FirstLayer_T(t, arr, accuracy):
    if accuracy == "O1":
        return (c1(tValue[t]) - b1/hh*arr[t][1])/(a1-b1/hh)  # правая разность
    elif accuracy == "O2":
        return (c1(tValue[t]) + b1 / 2 / hh * arr[t][2] - b1 * 2 / hh * arr[t][1]) / (
                    a1 - 3 * b1 / 2 / hh)  # правая разность


def LastLayer_T(t, arr, accuracy):
    if accuracy == "O1":
        return (c2(tValue[t]) + b2 / hh * arr[t][-2]) / (a2 + b2 / hh)  # левая разность
    elif accuracy == "O2":
        return (c2(tValue[t]) + b2 * 2 / hh * arr[t][-2] - b2 / 2 / hh * arr[t][-3]) / (
                    a2 + b2 * 3 / 2 / hh)  # левая разность


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


def FillArray(arr, sX, arr_x, accuracy):
    for i in range(sX):
        arr[0][i] = d1(arr_x[i])
    for i in range(sX):
        arr[1][i] = SecondLayer_X(arr_x[i], accuracy)
    for j in range(1, len(arr) - 1):
        for i in range(1, len(arr[j]) - 1):
            getCrossScheme(arr, i, j)
        arr[j + 1][0] = FirstLayer_T(j + 1, arr, accuracy)
        arr[j + 1][-1] = LastLayer_T(j + 1, arr, accuracy)


def getCrossScheme(arr, i, j):
    arr[j + 1][i] = a*tt*tt/hh/hh*(arr[j][i+1]-2*arr[j][i]+arr[j][i-1])+tt*tt*f(xValue[i], tValue[j])+2*arr[j][i]-arr[j-1][i]


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


###############################################################


U_O1 = ArrayOfSolving()
U_O2 = ArrayOfSolving()
exactU = ArrayOfSolving()
erU_O1 = ArrayOfSolving()
erU_O2 = ArrayOfSolving()

xValue = xValue(sizeL, hh)
tValue = tValue(sizeT, tt)

FillArray(U_O1, sizeL, xValue, 'O1')
FillArray(U_O2, sizeL, xValue, 'O2')
FillExactArray(exactU, xValue, tValue)

FillErArray(U_O1, exactU, erU_O1)
FillErArray(U_O2, exactU, erU_O2)


print()
print(maxValue(erU_O1))
print(maxValue(erU_O2))
