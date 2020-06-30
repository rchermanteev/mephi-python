import cv2
import numpy as np


class MethodSolutionOfTheLaplaceEquation:
    def __init__(self, image, preprocessed_image, base_line):
        self.image = image
        self.preprocessed_image = preprocessed_image
        self.base_line = base_line

    @staticmethod
    def solve_euler(h=0.0001, x_0=-0.1, z_0=0, y_0=0):

        def function(x, y, z, h):
            return (-z * (1 + y ** 2) ** (3 / 2) + y / x * (1 + y ** 2)) * h + y

        x_list = [x_0]
        z_list = [z_0]
        y_list = [y_0]

        y_list.append(function(x_list[0], y_list[0], z_list[0], h))
        z_list.append(z_list[0] + y_list[0] * h)
        x_list.append(x_list[0] + h)
        i = 1

        while y_list[i] >= 0:
            y_list.append(function(x_list[i - 1], y_list[i - 1], z_list[i - 1], h))
            z_list.append(z_list[i - 1] + y_list[i - 1] * h)
            x_list.append(x_list[i - 1] + h)
            i += 1

        return z_list[-1] * 10

    @staticmethod
    def transfer_grad_to_rad(grad):
        return np.pi / 180 * grad

    def search_angle(self, relation, error):
        start = 0
        end = self.transfer_grad_to_rad(90)

        mid = 0
        temp_rel = 0
        while abs(temp_rel - relation) > error and start != end:
            mid = (start + end) / 2
            temp_rel = self.solve_euler(y_0=np.tan(mid))
            if temp_rel < relation:
                start = mid
            else:
                end = mid

        return mid

    def get_result(self, error):
        contours, hierarchy = cv2.findContours(self.preprocessed_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        max_contour = None
        max_elem_in_contour = 0

        for contour in contours:

            if contour.shape[0] > max_elem_in_contour:
                max_elem_in_contour = contour.shape[0]
                max_contour = contour

        contour_drop = []

        for point in max_contour:
            if point[0][1] <= self.base_line - 10:
                contour_drop.append(point[0])

        contour_drop_sort = contour_drop.copy()

        contour_drop_sort.sort(key=lambda x: x[1])

        counter = 0
        max_point = [0, contour_drop_sort[0][1]]

        point_list_to_picture = []

        for point in contour_drop_sort:
            if max_point[1] != point[1]:
                max_point[0] = int(max_point[0] / counter)
                break
            point_list_to_picture.append(point)
            max_point[0] += point[0]
            counter += 1

        contour_drop_sort_x = contour_drop.copy()
        contour_drop_sort_x.sort(key=lambda x: x[0])

        point_with_min_x = contour_drop_sort_x[0]
        point_with_max_x = contour_drop_sort_x[-1]

        r = abs(point_with_max_x[0] - point_with_min_x[0])  # + 2
        h = abs(max_point[1] - self.base_line)  # + 3

        relation = h / r * 2

        angle = self.search_angle(relation, error)

        return angle
