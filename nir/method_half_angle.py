import cv2
import numpy as np


class MethodHalfAngle:
    def __init__(self, image, preprocessed_image, base_line):
        self.image = image
        self.preprocessed_image = preprocessed_image
        self.base_line = base_line

    def get_result(self):
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

        cv2.drawContours(self.image, [np.array(contour_drop)], 0, (255, 0, 0), 3)

        r = abs(point_with_max_x[0] - point_with_min_x[0])
        h = abs(max_point[1] - self.base_line)

        angle = 2 * np.arctan(h / (r / 2))

        px = point_with_max_x[0]
        py = point_with_min_x[1]
        tan = - np.tan(angle)

        px1 = px - 200
        py1 = 200 * tan + py

        cv2.line(self.image, (int(px), int(py)), (int(px1), int(py1)), (255, 0, 0), 2)

        return self.image, angle

    def draw_result_text(self, angle):
        ang = f"Tangent angle: {angle * 180 / np.pi}"
        koef = f"Wetting coefficient: {np.cos(angle)}"

        text = [ang, koef]

        cord_y = 50
        for word in text:
            cv2.putText(
                self.image, word, (30, cord_y), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0), 1
            )
            cord_y += 30
