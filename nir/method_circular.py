import numpy as np
import cv2
from sympy import Symbol, solve


class MethodCircular:
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
            if point[0][1] <= self.base_line - 20:
                contour_drop.append(point[0])

        point_to_circle = contour_drop[10:-10:(len(contour_drop) - 20) // 4][1:-1]

        if len(point_to_circle) < 3:
            point_to_circle = contour_drop[10:-10:(len(contour_drop) - 20) // 5][2:-1]

        if len(point_to_circle) < 3:
            point_to_circle = contour_drop[10:-10:(len(contour_drop) - 20) // 5][1:-1]


        print(point_to_circle)

        def reestablish_circle(*three_points_array):
            p1, p2, p3 = three_points_array
            x1, y1 = p1
            x2, y2 = p2
            x3, y3 = p3

            x0 = Symbol('x0')
            y0 = Symbol('y0')
            r = Symbol('r')

            f1 = (x1 - x0) ** 2 + (y1 - y0) ** 2 - r ** 2
            f2 = (x2 - x0) ** 2 + (y2 - y0) ** 2 - r ** 2
            f3 = (x3 - x0) ** 2 + (y3 - y0) ** 2 - r ** 2

            results = solve((f1, f2, f3), (x0, y0, r))

            params_to_circle = None

            for result in results:
                flag = True
                for value in result:
                    if value < 0:
                        flag = False

                if flag:
                    params_to_circle = result
                    break

            x0 = params_to_circle[0].evalf()
            y0 = params_to_circle[1].evalf()
            r = params_to_circle[2].evalf()

            return (x0, y0), r

        circle_center, radius = reestablish_circle(*point_to_circle)

        for point in point_to_circle:
            cv2.circle(self.image, tuple(point), 3, (0, 255, 255), 0)

        cv2.circle(self.image, circle_center, radius, (0, 0, 255), 0)

        return self.image, radius, circle_center

    def find_tilt_angle(self, rad: float, cord_centre: tuple):
        a = abs(cord_centre[1] - self.base_line)
        res_tilt_angle = np.pi / 2 - np.arcsin(float(a / rad))

        return res_tilt_angle

    def draw_tangent(self, angle, radius, centre_point, img=None):
        if img is None:
            img = self.image

        point_tang = (
            int(centre_point[0] + (radius ** 2 - abs(centre_point[1] - self.base_line) ** 2) ** 0.5),
            self.base_line,
        )

        tang = np.tan(angle)

        temp_point = (int(point_tang[0] - 200), int(-tang * 200 + point_tang[1]))
        cv2.line(img, point_tang, temp_point, (255, 0, 0), 2)

    def draw_result_text(self, angle, radius, centre):  # TODO: Уточнить вывод
        ang = f"Tangent angle: {angle * 180 / np.pi}"
        koef = f"Wetting coefficient: {np.cos(angle)}"
        cent = f"Coordinates of the center of the circle: (x: {centre[0]}, y: {centre[1]})"
        rad = f"Circle radius: {int(radius)} pix"

        text = [ang, koef, cent, rad]

        cord_y = 50
        for word in text:
            cv2.putText(
                self.image, word, (30, cord_y), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0), 1
            )
            cord_y += 30
