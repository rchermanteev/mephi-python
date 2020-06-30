import numpy as np
import cv2
from glob import glob
import os

from method_hafa import MethodHafa
from method_half_angle import MethodHalfAngle
from method_circular import MethodCircular
from method_elliptic import MethodElliptic
from method_solve_laplace import MethodSolutionOfTheLaplaceEquation

from preprocessing import (
    prepare_img,
    auto_canny,
    find_horizontal_line,
    inter_prepare_img
)


WRITE_IMG = False
WRITE_LOG = True
WRITE_IMG_WITH_CONTOURS = False
SHOW_IMG = False

PROJECT_DIR = "C:/Users/Rammi/PycharmProjects/NIR/"


def get_result_by_img_set(series, method):
    if WRITE_IMG:
        path_dir_to_res_img = PROJECT_DIR + f"res_image_data/res_img({method})/img_res({series})"
        os.mkdir(path_dir_to_res_img)

    if WRITE_IMG_WITH_CONTOURS:
        path_dir_to_res_img_with_contours = PROJECT_DIR + f"contours_img/img_contours({series})"
        os.mkdir(path_dir_to_res_img_with_contours)

    if WRITE_LOG:
        path_to_log = PROJECT_DIR + f"logs/log({method})/log({series}).csv"
        with open(path_to_log, mode="a") as log:
            log.write("Файл,Угол\n")

    list_image = [
        img
        for img in glob(
            f"image_data/img_drop({series})/*.bmp"
        )
    ]

    for path_img in list_image:
        try:
            file = path_img.split("\\")[-1]
            print(file)
            color_img = cv2.imread(path_img)

            contour_img = color_img.copy()
            resize_img = prepare_img(color_img)
            my_auto_canny = auto_canny(resize_img)
            cord_line_y = find_horizontal_line(my_auto_canny)

            if method == "method_hafa":
                my_auto_canny = inter_prepare_img(my_auto_canny, cord_line_y)
                method_hafa = MethodHafa(color_img, my_auto_canny, cord_line_y)
                res_img, radius, centre = method_hafa.find_drop()
                angle = method_hafa.find_tilt_angle(radius, centre)
                method_hafa.draw_tangent(angle, radius, centre)
                method_hafa.draw_result_text(angle, radius, centre)

            if method == "method_half_angle":
                method_half_angle = MethodHalfAngle(color_img, my_auto_canny, cord_line_y)
                res_img, angle = method_half_angle.get_result()
                method_half_angle.draw_result_text(angle)

            if method == "method_solve_laplace":
                error = 0.0001
                method_half_angle = MethodSolutionOfTheLaplaceEquation(color_img, my_auto_canny, cord_line_y)
                angle = method_half_angle.get_result(error)

            if method == "method_circular":
                method_circular = MethodCircular(color_img, my_auto_canny, cord_line_y)
                res_img, radius, centre = method_circular.get_result()
                angle = method_circular.find_tilt_angle(radius, centre)
                method_circular.draw_tangent(angle, radius, centre)
                method_circular.draw_result_text(angle, radius, centre)

            if method == "method_elliptic":
                method_elliptic = MethodElliptic(color_img, my_auto_canny, cord_line_y)
                res_img, hs, centre = method_elliptic.get_result()
                angle = method_elliptic.get_angle_and_draw_tangent(centre, hs)
                method_elliptic.draw_result_text(angle, centre, hs)

            if SHOW_IMG:
                cv2.imshow("result", res_img)
                cv2.waitKey()

            if WRITE_IMG:
                cv2.imwrite(os.path.join(path_dir_to_res_img, file), res_img)

            if WRITE_LOG:
                with open(path_to_log, mode="a") as log:
                    log.write(
                        f"{file},{angle * 180 / np.pi}\n"
                    )
        except BaseException:
            print(f"file is bad")


series_list = ["G4", "G6", "G07", "G08", "G10", "G11", "G35", "G36", "G43"]
# series_list = ["G4"]

for series in series_list:
    print(f"Обрабатывается серия: {series}")
    # # print("method_hafa")
    # # get_result_by_img_set(series, "method_hafa")
    # print("method_half_angle")
    # get_result_by_img_set(series, "method_half_angle")
    # print("method_circular")
    # get_result_by_img_set(series, "method_circular")
    # print("method_elliptic")
    # get_result_by_img_set(series, "method_elliptic")
    print("method_solve_laplace")
    get_result_by_img_set(series, "method_solve_laplace")
