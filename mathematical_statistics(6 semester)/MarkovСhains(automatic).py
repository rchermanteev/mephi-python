"""
Марковские цепи
Соделирование методами Монте-Карло работы автомата
"""

import random

NUM_TEST_CHAIN = 100  # число испытаний цепи Маркова
NUM_TEST = 1000  # максимальное число испытаний автомата
MAX_NOTE_50 = 100  # максимальное число купюр по 50
p = 0.4  # вероятность получить 50
INITIAL_NOTE_50 = 20


def get50():
    return random.random() < p


class Automatic(object):
    def __init__(self, max_50, init_50, num_tests):
        self.max_50 = max_50
        self.current_test = 0
        self.note_100 = 0
        self.note_50 = init_50
        self.num_tests = num_tests
        self.note50_step5 = 0
        self.note50_step10 = 0
        self.note50_step100 = 0
        self.note100_step5 = 0
        self.note100_step10 = 0
        self.note100_step100 = 0

    def iteration(self):
        #  print("Тест: {} Число купюр 50: {}".format(self.current_test, self.note_50))
        if get50():
            if self.note_50 == self.max_50:
                return False
            else:
                self.note_50 += 1
                self.current_test += 1
                return True
        else:
            if self.note_50 == 0:
                return False
            else:
                self.note_50 -= 1
                self.note_100 += 1
                self.current_test += 1
                return True

    def get_res_work(self):
        counter = self.num_tests
        while self.iteration() and counter != 0:
            counter -= 1
            if counter == 0:
                return self.current_test, self.note_50, self.note_100, self.note50_step5, self.note100_step5, \
               self.note50_step10, self.note100_step10, self.note50_step100, self.note100_step100
            if self.current_test == 5:
                self.note50_step5 = self.note_50
                self.note100_step5 = self.note_100
            if self.current_test == 10:
                self.note50_step10 = self.note_50
                self.note100_step10 = self.note_100
            if self.current_test == 100:
                self.note50_step100 = self.note_50
                self.note100_step100 = self.note_100
        return self.current_test, self.note_50, self.note_100, self.note50_step5, self.note100_step5, \
               self.note50_step10, self.note100_step10, self.note50_step100, self.note100_step100


list_res_work = [Automatic(MAX_NOTE_50, INITIAL_NOTE_50, NUM_TEST).get_res_work() for _ in range(NUM_TEST_CHAIN)]
#  print(list_res_work)


def condition(x, board):
    if x > board:
        return 1
    else:
        return 0


av_test = sum([i[0] for i in list_res_work]) / NUM_TEST_CHAIN
av_note50_test5 = sum([i[3] for i in list_res_work]) / sum([condition(i[0], 4) for i in list_res_work])
av_note100_test5 = sum([i[4] for i in list_res_work]) / sum([condition(i[0], 4) for i in list_res_work])
av_note50_test10 = sum([i[5] for i in list_res_work]) / sum([condition(i[0], 9) for i in list_res_work])
av_note100_test10 = sum([i[6] for i in list_res_work]) / sum([condition(i[0], 9) for i in list_res_work])
av_note50_test100 = sum([i[7] for i in list_res_work]) / sum([condition(i[0], 99) for i in list_res_work])
av_note100_test100 = sum([i[8] for i in list_res_work]) / sum([condition(i[0], 99) for i in list_res_work])

print("Через сколько шагов отключится автомат: {}".format(av_test))
print('Среднее число купюр номиналом 50 на 5-ом шаге: {}'.format(av_note50_test5))
print('Среднее число купюр номиналом 50 на 10-ом шаге: {}'.format(av_note50_test10))
print('Среднее число купюр номиналом 50 на 100-ом шаге: {}'.format(av_note50_test100))
print('Среднее число купюр номиналом 100 на 5-ом шаге: {}'.format(av_note100_test5))
print('Среднее число купюр номиналом 100 на 10-ом шаге: {}'.format(av_note100_test10))
print('Среднее число купюр номиналом 100 на 100-ом шаге: {}'.format(av_note100_test100))
