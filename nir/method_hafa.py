import cv2
import numpy as np


class MethodHafa:
    def __init__(self, image, preprocessed_image, base_line):
        self.image = image
        self.preprocessed_image = preprocessed_image
        self.base_line = base_line - 5

    def find_drop(self):
        circles = cv2.HoughCircles(
            image=self.preprocessed_image,
            method=cv2.HOUGH_GRADIENT,
            dp=1,
            minDist=300,
            # param1=50,
            param2=1,
            minRadius=200,
            maxRadius=500,
        )

        print(f"Число Окружностей: {len(circles)}")

        res_img = None
        radius = None
        centre = None

        for circle in circles[0]:  # TODO: Можно доработать под общий случай, без хардкода констант
            if self.base_line < circle[1] < 1100 and 400 < circle[0] < 800 and circle[2] < 450:
                radius = circle[2]
                centre = (circle[0], circle[1])
                res_img = cv2.circle(self.image, centre, 3, (0, 255, 255), -1)
                res_img = cv2.circle(res_img, centre, radius, (0, 0, 255), 1)
                break  # TODO: Такое себе решение, нодо разобраться

        return res_img, radius, centre

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
        ang = f"Tangent angle: {angle*180/np.pi}"
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
