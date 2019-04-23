"""
Моделирование работы типичной поликлиники
"""


import random as random
from math import *
import time


TimeHardVisitor = 5
TimeMediumVisitor = 15
TimeEasyVisitor = 30

numberDoctors = 1
WorkingHours = 540
MT = 10
AvTimeAppointment = 10
DispTimeAppointment = 2

StartProgramTime = time.time()
ArrayOfTact = []


def just_ask():
    r = random.random()
    if 0 <= r < 0.97:
        return False
    else:
        return True


def type_visitor(cur_time, name):
    r = random.random()
    vis = 0
    if 0 <= cur_time < 180:
        if 0 <= r < 0.1:
            vis = Visitor(TimeHardVisitor, name)
        elif 0.1 <= r < 0.3:
            vis = Visitor(TimeMediumVisitor, name)
        elif 0.3 <= r <= 1.0:
            vis = Visitor(TimeEasyVisitor, name)
    elif 180 <= cur_time < 360:
        if 0 <= r < 0.1:
            vis = Visitor(TimeHardVisitor, name)
        elif 0.1 <= r < 0.6:
            vis = Visitor(TimeMediumVisitor, name)
        elif 0.6 <= r <= 1.0:
            vis = Visitor(TimeEasyVisitor, name)
    elif 360 <= cur_time < 540:
        if 0 <= r < 0.5:
            vis = Visitor(TimeHardVisitor, name)
        elif 0.5 <= r < 0.8:
            vis = Visitor(TimeMediumVisitor, name)
        elif 0.8 <= r <= 1.0:
            vis = Visitor(TimeEasyVisitor, name)
    return vis


class Doctor(object):
    def __init__(self, name):
        self.id = name
        self.counter = 0
        self.status = True
        self.time_appointment = 0
        self.time_current_appointment = 0
        self.servedVisitors = []
        self.current_visitor = 0
        self.distracted = False
        self.counter_distracted = 0

    def appointment(self, cur_visitor, curr_time):
        if self.status is True and (len(cur_visitor) != 0):
            self.current_visitor = cur_visitor.pop(0)
            self.current_visitor.waiting_time = \
                self.current_visitor.max_waiting_time-self.current_visitor.current_waiting_time
            self.status = False
            self.time_appointment = int(random.normalvariate(AvTimeAppointment, DispTimeAppointment))
            self.current_visitor.time_appointment = self.time_appointment
            self.time_current_appointment = self.time_appointment
            # print("Начало приёма пациента {} у доктора {}".format(self.current_visitor.id, self.id))
        elif self.distracted is False and self.time_current_appointment == 0 and self.status is False:
            self.status = True
            self.current_visitor.status = 1
            self.servedVisitors += [self.current_visitor]
            self.counter += 1
            # print("Конец приёма")
        elif self.time_current_appointment == 0 and self.status is False and self.distracted is True:
            self.status = True
            self.distracted = False
            # print("Доктор свободен")
        elif self.status is False:
            self.time_current_appointment -= 1
            # print("Оставшееся время приёма: {}".format(self.time_current_appointment))
        if curr_time == WorkingHours-1 and self.distracted is False:
            if self.time_current_appointment > 10:
                unattendedVisitors.append(self.current_visitor)
            elif self.status is False:
                self.current_visitor.status = 1
                self.servedVisitors += [self.current_visitor]
                self.counter += 1
        if self.status is True:
            if just_ask():
                # print("Отвелекли")
                self.status = False
                self.distracted = True
                self.counter_distracted += 1
                self.time_current_appointment = 2
        elif self.status is False and (type(self.current_visitor) != int):
            if just_ask():
                # print("Отвелекли")
                self.counter_distracted += 1
                self.time_current_appointment += 5
                self.current_visitor.time_appointment += 5


def remove_from_queue(queue):
    for obj in queue:
        if obj.status == -1:
            queue.remove(obj)
            break


class Visitor(object):
    def __init__(self, max_waiting_time, name):
        self.id = name
        self.max_waiting_time = max_waiting_time
        self.current_waiting_time = max_waiting_time
        self.status = 0  # 0-ждёт приёма, 1-обслужен, -1 ушёл, не дождавшись очереди
        self.waiting_time = None
        self.time_appointment = None

    def patience(self, curr_time):
        if self.status == 0:
            if self.current_waiting_time == 0:
                self.status = -1
                self.waiting_time = self.max_waiting_time
                unattendedVisitors.append(self)
            elif curr_time == WorkingHours-1:
                if self.current_waiting_time > 0:
                    unattendedVisitors.append(self)
            else:
                self.current_waiting_time -= 1


def simulate_work_day(unattended_visitors):
    start_time = time.time()
    appointment = 0
    counter_visitors = 0
    visitors = []
    doctors = [Doctor(i) for i in range(1, numberDoctors + 1)]
    for currentTime in range(0, 540):
        if appointment == 0:
            r = random.random()
            appointment = int(-MT*log(r))
            counter_visitors += 1
            visitor = type_visitor(currentTime, counter_visitors)
            visitors.append(visitor)
        else:
            appointment -= 1

        for doctor in doctors:
            doctor.appointment(visitors, currentTime)

        for _visitor in visitors:
            _visitor.patience(currentTime)

        for _ in range(len(visitors)):
            remove_from_queue(visitors)

    # for doctor in doctors:
    #     print("Число клиентов обслуженных {}-ым доктором: {}".format(doctor.id, doctor.counter))
    #     print("Доктора {} отвлекли {} раз(а)".format(doctor.id, doctor.counter_distracted))
    #     print([obj.id for obj in doctor.servedVisitors])
    #
    # print("Всего клиентов: {}".format(counter_visitors))
    # print('Необслуженные клиенты: {} (число: {})'
    #       .format([obj.id for obj in unattended_visitors], len(unattended_visitors)))

    common_array_visitors = []
    for doctor in doctors:
        common_array_visitors += doctor.servedVisitors
    common_array_visitors += unattended_visitors
    # print([obj.max_waiting_time for obj in common_array_visitors])
    # print([obj.time_appointment for obj in common_array_visitors])
    ArrayOfTact.append(time.time()-start_time)
    return common_array_visitors, unattended_visitors


"""
Блок отвечающий за анализ данных, полученных в результате моделирования процесса 
"""

Test_number = 100

average_missed = 0
max_missed = 0
min_missed = 999
average_hard_visitor = 0
average_medium_visitor = 0
average_easy_visitor = 0
average_visitors = 0
average_waiting_easy_visitor = 0
average_waiting_medium_visitor = 0
average_waiting_hard_visitor = 0
average_time_appointment = 0
dispersion_estimate = 0
evaluation_error = 0
satisfactory_model = 0
work_change = []
deviations = []

for _ in range(Test_number):
    unattendedVisitors = []
    work_day = simulate_work_day(unattendedVisitors)
    work_change.append(work_day)
    average_visitors += len(work_day[0])/Test_number
    average_missed += len(work_day[1])/Test_number
    if len(work_day[1]) > max_missed:
        max_missed = len(work_day[1])
    if len(work_day[1]) < min_missed:
        min_missed = len(work_day[1])
    for visitor in work_day[0]:
        if visitor.max_waiting_time == TimeHardVisitor:
            average_hard_visitor += 1/Test_number
            if visitor.waiting_time is not None:  # Не считаем тех посетителей, которые пришли сишком поздно
                average_waiting_hard_visitor += visitor.waiting_time/Test_number
        elif visitor.max_waiting_time == TimeMediumVisitor:
            average_medium_visitor += 1/Test_number
            if visitor.waiting_time is not None:
                average_waiting_medium_visitor += visitor.waiting_time/Test_number
        elif visitor.max_waiting_time == TimeEasyVisitor:
            average_easy_visitor += 1/Test_number
            if visitor.waiting_time is not None:
                average_waiting_easy_visitor += visitor.waiting_time/Test_number
        if visitor.time_appointment is not None:  # Рассматриваем тоько тех, кто попал на приём
            average_time_appointment += visitor.time_appointment/Test_number


for work_day in work_change:
    dispersion_estimate += (len(work_day[1])-average_missed)**2/Test_number
    deviations.append(abs(len(work_day[1])-average_missed))

evaluation_error = (3*sqrt(dispersion_estimate/Test_number))

for i in range(len(deviations)):
    print('{} < {}'.format(deviations[i], evaluation_error))
    if deviations[i] < evaluation_error:
        satisfactory_model += 1

average_waiting_hard_visitor /= average_hard_visitor
average_waiting_medium_visitor /= average_medium_visitor
average_waiting_easy_visitor /= average_easy_visitor
average_time_appointment /= (average_visitors - average_missed)

EndProgramTime = time.time() - StartProgramTime

print("Среднее число посетителей: {}".format(average_visitors))
print("Среднее время приёма: {}".format(average_time_appointment))
print("Среднее число не дождавшихся посетителей: {}".format(average_missed))
print("Среднее время ожидания торопящихся посетителей: {}".format(average_waiting_hard_visitor))
print("Среднее число торопящихся посетителей: {}".format(average_hard_visitor))
print("Среднее время ожидания обычных посетителей: {}".format(average_waiting_medium_visitor))
print("Среднее число обычных посетителей: {}".format(average_medium_visitor))
print("Среднее время ожидания не торопящихся посетителей: {}".format(average_waiting_easy_visitor))
print("Среднее число не торопящихся посетителей: {}".format(average_easy_visitor))
print("Максимальное количество упущенных клиентов: {}".format(max_missed))
print("Минимальное количество упущенных клиентов: {}".format(min_missed))
print("Дисперсия случайной величины: {}".format(dispersion_estimate))
print(EndProgramTime)
print(ArrayOfTact)
print(satisfactory_model)
print(abs(max_missed - min_missed)/average_visitors*100)
