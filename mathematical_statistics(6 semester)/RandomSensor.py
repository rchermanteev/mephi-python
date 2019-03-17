"""
В данной программе проводится расчёт значения статистики Пирсона для 4х тестов 
(В качестве датчика берётся массив полученный в программе FrequencyAnalysis.py)
"""

import FrequencyAnalysis as FA


def PearsonStatistics(sensor, num_test):  # Вычисление статистики Пирсона для различных тестов
  N = len(sensor)
  N1 = N / 2
  N2 = N / 2
  N3 = int(N / 3)
  w = 0

  if num_test == "1":
    d = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in sensor:
      d[i] += 1
    for i in d:
      w += (i - N / 10) ** 2 / (N / 10)
    return w

  elif num_test == "2":
    d = [0, 0]
    for i in range(0, N, 2):
      if sensor[i] * 10 + sensor[i + 1] < 50:
        d[0] += 1
      else:
        d[1] += 1
    for i in d:
      w += (i - N1 / 2) ** 2 / (N1 / 2)
    return w

  elif num_test == "3":
    d = [0, 0, 0, 0]
    for i in range(0, N, 2):
      if sensor[i] * 10 + sensor[i + 1] < 25:
        d[0] += 1
      elif  sensor[i] * 10 + sensor[i + 1] < 50:
        d[1] += 1
      elif sensor[i] * 10 + sensor[i + 1] < 75:
        d[2] += 1
      else:
        d[3] += 1
    for i in d:
      w += (i - N2 / 4) ** 2 / (N2 / 4)
    return w

  elif num_test == "4":
    d = [0, 0]
    for i in range(0, N - 2, 3):
      if sensor[i] * 100 + sensor[i + 1] * 10 + sensor[i + 2] < 500:
        d[0] += 1
      else:
        d[1] += 1
    for i in d:
      w += (i - N3 / 2) ** 2 / (N3 / 2)
    return w


print('Статистика Пирсона(для датчика из {} элементов):'.format(len(FA.bad_sensor_100)))
print("Тест1: W = {}".format(PearsonStatistics(FA.bad_sensor_100, "1")))
print("Тест2: W = {}".format(PearsonStatistics(FA.bad_sensor_100, "2")))
print("Тест3: W = {}".format(PearsonStatistics(FA.bad_sensor_100, "3")))
print("Тест4: W = {}".format(PearsonStatistics(FA.bad_sensor_100, "4")))

print()

print('Статистика Пирсона(для датчика из {} элементов):'.format(len(FA.bad_sensor_200)))
print("Тест1: W = {}".format(PearsonStatistics(FA.bad_sensor_200, "1")))
print("Тест2: W = {}".format(PearsonStatistics(FA.bad_sensor_200, "2")))
print("Тест3: W = {}".format(PearsonStatistics(FA.bad_sensor_200, "3")))
print("Тест4: W = {}".format(PearsonStatistics(FA.bad_sensor_200, "4")))
