import numpy as np
import cv2
from collections import Counter


def auto_canny(img, sigma=0.33):
    v = np.median(img)

    lower = int(max(0, (1 - sigma) * v))
    upper = int(min(255, (1 + sigma) * v))
    edged = cv2.Canny(img, lower, upper)

    return edged


def inter_prepare_img(img, base_line):
    for i in range(len(img)):  # TODO: Вынести в функцию utils/prepare_img

        if 0 < i < 400 or base_line - 5 < i < len(img):
            for j in range(len(img[0])):
                img[i, j] = -1

        for j in range(0, 200):
            img[i, j] = -1

        for j in range(len(img[0]) - 200, len(img[0])):
            img[i, j] = -1

    return img


def prepare_img(img, threshold=None):
    # TODO: Не все действия вынесены в функцию
    thr = threshold or np.median(img) / 2
    bl_wh_img = cv2.inRange(img, (thr, thr, thr), (255, 255, 255))
    return cv2.copyMakeBorder(
        bl_wh_img, 0, 1000, 0, 0, cv2.BORDER_CONSTANT, value=(0, 0, 0)
    )


def find_and_draw_contours(
    temp_img, draw_img
):  # Есть артефакты (Нужна для дебага и второго способа решения)
    contours, hierarchy = cv2.findContours(
        temp_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
    )
    contour_ind = 0

    max_len = len(contours[0])
    for ind, contour in enumerate(contours):
        if len(contour) > max_len:
            max_len = len(contour)
            contour_ind = ind

    cv2.drawContours(
        draw_img, contours, contour_ind, (255, 0, 0), 3, cv2.LINE_AA, hierarchy, 1
    )


def find_horizontal_line(img):  # TODO: Переделать через Хафа
    list_point = []

    for j in range(len(img[0])):
        i = 0
        while img[i][j] != 255 and i < len(img) - 1:
            i += 1
        list_point.append(i)

    c = Counter(list_point).most_common(1)
    line_cord = c[0][0]

    return line_cord


