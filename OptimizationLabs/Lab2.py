"""
Prog:   Lab2.py
Auth:   Oleksii Krutko, IO-z91
Desc:   Optimization and experiment planning. Lab 2. Var 10. 2021
"""
import math

import matplotlib.pyplot as plt
import numpy as np

from Input import InputError
from Input import get_input_source


def create_axs(regression_equation):
    # A4 page
    fig_width_cm = 21
    fig_height_cm = 29.7

    extra_margin_cm = 1
    margin_left_cm = 2 + extra_margin_cm
    margin_right_cm = 1.0
    margin_bottom_cm = 1.0 + extra_margin_cm
    margin_top_cm = 3.0 + extra_margin_cm
    inches_per_cm = 1 / 2.54

    fig_width = fig_width_cm * inches_per_cm  # width in inches
    fig_height = fig_height_cm * inches_per_cm  # height in inches

    margin_left = margin_left_cm * inches_per_cm
    margin_right = margin_right_cm * inches_per_cm
    margin_bottom = margin_bottom_cm * inches_per_cm
    margin_top = margin_top_cm * inches_per_cm

    left_margin = margin_left / fig_width
    right_margin = 1 - margin_right / fig_width
    bottom_margin = margin_bottom / fig_height
    top_margin = 1 - margin_top / fig_height

    fig_size = [fig_width, fig_height]

    plt.rc('figure', figsize=fig_size)

    fig_page1, axs_page1 = plt.subplots(1, 1)
    fig_page1.suptitle("Test", fontsize=16, style='normal')
    fig_page1.suptitle("Normal regression equation: " + regression_equation, fontsize=16, style='normal')

    # fig_page1.suptitle("Normal regression equation: " + regression_equation + "\n" + "Criteria: " + criteria + "\n" +
    #                    "X max = {:.02f}".format(x_max), fontsize=16, style='normal')

    fig_page1.canvas.set_window_title('Lab 2. Two-factor experiment. Var. 10')

    axs_page1.set_title('Experiment plan', fontsize=12, color='gray')

    return axs_page1, fig_page1


def main():
    print("Lab 2. Two-factor experiment. Var. 10")

    # input_source = get_input_source("lab1")
    # try:
    #     n = input_source.read_var("n", int, 3, 15)
    #     x_max = input_source.read_var("x_max", float, float("-inf"), float("inf"))
    #
    #     a = []
    #     for i in range(4):
    #         a.append(input_source.read_var("a[{}]".format(i), float, float("-inf"), float("inf")))
    #
    # except InputError as ir:
    #     print("Error wile reading data from file: ", ir)
    #     return

    k = 2
    n = 3
    m = 5

    # v10 input
    x1_min = -25.0
    x1_max = -5.0
    x2_min = -30.0
    x2_max = 45.0

    y_min = (20.0 - 10.0) * 10.0
    y_max = (30.0 - 10.0) * 10.0

    # Fill experiment plan
    x1_0 = (x1_min + x1_max) / 2
    x2_0 = (x2_min + x2_max) / 2

    x1_dx = x1_0 - x1_min
    x2_dx = x2_0 - x2_min

    x1 = (x1_min, x1_max, x1_min)
    x2 = (x2_min, x2_min, x2_max)

    x1_norm = [(x - x1_0) / x1_dx for x in x1]
    x2_norm = [(x - x2_0) / x2_dx for x in x2]

    y = [y_min + np.random.random(m) * math.fabs((y_max - y_min)) for i in range(n)]

    # Check Romanovsky criteria
    y_avr = [sum(y[i]) / m for i in range(n)]
    dispersion = []
    for i in range(n):
        S = 0.0
        for j in range(m):
            S = S + (y[i][j] - y_avr[i]) ** 2

        dispersion.append(S / m)

    standard_deviation = math.sqrt((2 * (2 * m - 2)) / (m * (m - 4)))

    Fuv = []

    if dispersion[0] > dispersion[1]:
        Fuv.append(dispersion[0] / dispersion[1])
    else:
        Fuv.append(dispersion[1] / dispersion[0])

    if dispersion[2] > dispersion[0]:
        Fuv.append(dispersion[2] / dispersion[0])
    else:
        Fuv.append(dispersion[0] / dispersion[2])

    if dispersion[2] > dispersion[1]:
        Fuv.append(dispersion[2] / dispersion[1])
    else:
        Fuv.append(dispersion[1] / dispersion[2])

    Eta_uv = [((m - 2) / m) * Fuv[i] for i in range(n)]
    Rub = [math.fabs(Eta_uv[i] - 1) / standard_deviation for i in range(n)]

    R_check_90 = {
        2: 1.68,
        6: 2.0,
        8: 2.17,
        10: 2.29,
        12: 2.39,
        15: 2.49,
        20: 2.62,
    }

    next_m = next(x for x in R_check_90.keys() if x >= m)

    for i in range(n):
        if Rub[i] > R_check_90[next_m]:
            print("Romanovsky criteria was not met. Please run again or increase m.")
            return

    print("Romanovsky criteria is met.")

    # Calculate regression equation coefficients
    m_x_1 = sum(x1_norm) / n
    m_x_2 = sum(x2_norm) / n
    m_y_avr = sum(y_avr) / n
    a1 = sum(x ** 2 for x in x1_norm) / 3
    a2 = (x1_norm[0] * x2_norm[0] + x1_norm[1] * x2_norm[1] + x1_norm[2] * x2_norm[2]) / 3
    a3 = sum(x ** 2 for x in x2_norm) / 3

    a11 = sum(x1_norm[i] * y_avr[i] for i in range(n)) / 3
    a22 = sum(x2_norm[i] * y_avr[i] for i in range(n)) / 3

    b0 = np.linalg.det(np.array([[m_y_avr, m_x_1, m_x_2], [a11, a1, a2], [a22, a2, a3]])) \
         / np.linalg.det(np.array([[1.0, m_x_1, m_x_2], [m_x_1, a1, a2], [m_x_2, a2, a3]]))
    b1 = np.linalg.det(np.array([[1.0, m_y_avr, m_x_2], [m_x_1, a11, a2], [m_x_2, a22, a3]])) \
         / np.linalg.det(np.array([[1.0, m_x_1, m_x_2], [m_x_1, a1, a2], [m_x_2, a2, a3]]))
    b2 = np.linalg.det(np.array([[1.0, m_x_1, m_y_avr], [m_x_1, a1, a11], [m_x_2, a2, a22]])) \
         / np.linalg.det(np.array([[1.0, m_x_1, m_x_2], [m_x_1, a1, a2], [m_x_2, a2, a3]]))

    regression_equation = "Y = {:+.2f} {:+.2f}X1 {:+.2f}X2".format(b0, b1, b2)

    # Check
    for i in range(n):
        y_reg = b0 + b1 * x1_norm[i] + b2 * x2_norm[i]
        if math.fabs(y_reg - y_avr[i]) > 1e-6:
            print("Regression equation is wrong!.")
            return

    print("Regression equation check passed.")

    # Naturalization check
    delta_x1 = math.fabs(x1_max - x1_min) / 2
    delta_x2 = math.fabs(x2_max - x2_min) / 2

    a0 = b0 - b1 * (x1_0 / delta_x1) - b2 * (x2_0 / delta_x2)
    a1 = b1 / delta_x1
    a2 = b2 / delta_x2

    for i in range(n):
        y_natural = a0 + a1 * x1[i] + a2 * x2[i]
        if math.fabs(y_natural - y_avr[i]) > 1e-6:
            print("Natural regression equation is wrong!.")
            return

    print("Naturalized regression equation check passed.")

    axs_page1, fig_page1 = create_axs(regression_equation)

    # draw table
    table_data = [["" for j in range(7)] for i in range(n)]

    for i in range(n):
        table_data[i][0] = "{:.2f}".format(x1_norm[i])
        table_data[i][1] = "{:.2f}".format(x2_norm[i])

        for j in range(m):
            table_data[i][j + 2] = "{:.2f}".format(y[i][j])

    axs_page1.axis('off')
    col_label = (r'$X1$', r'$X2$', r'$Y1$', r'$Y2$', r'$Y3$', r'$Y4$', r'$Y5$')
    the_table = axs_page1.table(cellText=table_data, colLabels=col_label, loc='best')
    the_table.set_fontsize(20)
    the_table.scale(1.0, 4.0)

    plt.show()

    fig_page1.savefig("./input_files/Lab2_img_png")


main()
