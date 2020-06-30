import numpy as np
import cv2
from sympy import Symbol, solve


class MethodElliptic:
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

        point_to_ellipse = contour_drop[20:-10:(len(contour_drop) - 20) // 8][1:-1]

        def reestablish_ellipse(*six_points_array):
            p1, p2, p3, p4, p5, p6 = six_points_array
            x1, y1 = p1
            x2, y2 = p2
            x3, y3 = p3
            x4, y4 = p4
            x5, y5 = p5
            x6, y6 = p6

            x0 = Symbol('x0')
            y0 = Symbol('y0')
            a = Symbol('a')
            b = Symbol('b')

            f1 = ((x2 - x0) ** 2) / a ** 2 + ((y2 - y0) ** 2) / b ** 2 - 1
            f2 = ((x3 - x0) ** 2) / a ** 2 + ((y3 - y0) ** 2) / b ** 2 - 1
            f3 = ((x4 - x0) ** 2) / a ** 2 + ((y4 - y0) ** 2) / b ** 2 - 1
            f4 = ((x5 - x0) ** 2) / a ** 2 + ((y5 - y0) ** 2) / b ** 2 - 1

            results = solve((f1, f2, f3, f4), (x0, y0, a, b))

            params_to_ellipse = None
            for result in results:
                flag = True
                for value in result:
                    if value < 0:
                        flag = False

                if flag:
                    params_to_ellipse = result
                    break

            x0, y0, a, b = params_to_ellipse

            x0 = x0.evalf()
            y0 = y0.evalf()
            a = a.evalf()
            b = b.evalf()

            return (x0, y0), (a, b)

        centre_ellipse, half_shafts = reestablish_ellipse(*point_to_ellipse)

        for point in point_to_ellipse:
            cv2.circle(self.image, tuple(point), 3, (0, 255, 255), 0)

        cv2.ellipse(self.image, centre_ellipse, half_shafts, 0, 0, 360, (0, 0, 255), 0)

        return self.image, half_shafts, centre_ellipse

    def get_angle_and_draw_tangent(self, centre, half_shafts):
        x0 = float(centre[0])
        y0 = float(centre[1])
        a = float(half_shafts[0])
        b = float(half_shafts[1])
        py = self.base_line

        px = np.sqrt((1 - ((py - y0) ** 2) / b ** 2) * a ** 2) + x0

        tan = (px - x0) * b ** 2 / (py - y0) / a ** 2

        angle = np.arctan(tan)

        px1 = px - 200
        py1 = 200 * tan + py

        cv2.line(self.image, (int(px), int(py)), (int(px1), int(py1)), (255, 0, 0), 3)

        return angle

    def draw_result_text(self, angle, centre, half_shafts):
        ang = f"Tangent angle: {angle * 180 / np.pi}"
        koef = f"Wetting coefficient: {np.cos(angle)}"
        cent = f"Coordinates of the center of the circle: (x: {centre[0]}, y: {centre[1]})"
        hs = f"Ellipse half_shafts: a = {int(half_shafts[0])} pix, b = {int(half_shafts[1])} pix"

        text = [ang, koef, cent, hs]

        cord_y = 50
        for word in text:
            cv2.putText(
                self.image, word, (30, cord_y), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0), 1
            )
            cord_y += 30
