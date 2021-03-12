"""
Prog:   Lab3.py
Auth:   Oleksii Krutko, IO-z91
Desc:   Algorithms Lab 3. Var 10. 2021
"""

import matplotlib.pyplot as plt
import numpy as np

from Input import InputError
from Input import get_input_source


def create_axs(reaction_expression, criteria, x_max):
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
    fig_page1.suptitle("Reaction: " + reaction_expression + "\n" + "Criteria: " + criteria + "\n" +
                       "X max = {:.02f}".format(x_max), fontsize=16, style='normal')
    fig_page1.subplots_adjust(left=left_margin, right=right_margin, top=top_margin, bottom=bottom_margin,
                              wspace=0.3, hspace=0.2)
    fig_page1.canvas.set_window_title('Lab 1. Basic principal of experiment planning. Var. 10')

    axs_page1.set_title('Experiment plan', fontsize=12, color='gray')

    return axs_page1, fig_page1


def main():
    print("Lab 1. Base principal. Var. 10")

    input_source = get_input_source("lab1")
    try:
        n = input_source.read_var("n", int, 3, 15)
        x_max = input_source.read_var("x_max", float, float("-inf"), float("inf"))

        a = []
        for i in range(4):
            a.append(input_source.read_var("a[{}]".format(i), float, float("-inf"), float("inf")))

    except InputError as ir:
        print("Error wile reading data from file: ", ir)
        return

    # a = [1.0, 2.0, 3.0, 4.0]
    # n = 8
    # x_max = 20.0

    x1 = np.random.random(n) * x_max
    x2 = np.random.random(n) * x_max
    x3 = np.random.random(n) * x_max

    x1_min = min(x1)
    x2_min = min(x2)
    x3_min = min(x3)
    x1_max = max(x1)
    x2_max = max(x2)
    x3_max = max(x3)
    x1_0 = (x1_min + x1_max) / 2
    x2_0 = (x2_min + x2_max) / 2
    x3_0 = (x3_min + x3_max) / 2
    x1_dx = x1_0 - x1_min
    x2_dx = x2_0 - x2_min
    x3_dx = x3_0 - x3_min

    y = [a[0] + a[1]*x1[i] + a[2]*x2[i] + a[3]*x3[i] for i in range(n)]
    y_0 = a[0] + a[1]*x1_0 + a[2]*x2_0 + a[3]*x3_0

    target_point = y.index(min(y))

    axs_page1, fig_page1 = create_axs("Y = {:.2f} + {:.2f}X1 + {:.2f}X2 + {:.2f}X3"
                                      .format(a[0], a[1], a[2], a[3]), r'$min(Y)$', x_max)

    # draw table
    table_data = [["" for j in range(9)] for i in range(n+2)]
    for i in range(n):
        table_data[i][0] = "{}".format(i)
        table_data[i][1] = "{:.2f}".format(x1[i])
        table_data[i][2] = "{:.2f}".format(x2[i])
        table_data[i][3] = "{:.2f}".format(x3[i])
        table_data[i][4] = "{:.2f}".format(y[i])

        table_data[i][6] = "{:.2f}".format((x1[i] - x1_0) / x1_dx)
        table_data[i][7] = "{:.2f}".format((x2[i] - x2_0) / x2_dx)
        table_data[i][8] = "{:.2f}".format((x3[i] - x3_0) / x3_dx)

    table_data[n][0] = r'$x_{0}$'
    table_data[n][1] = "{:.2f}".format(x1_0)
    table_data[n][2] = "{:.2f}".format(x2_0)
    table_data[n][3] = "{:.2f}".format(x3_0)
    table_data[n][4] = "{:.2f}".format(y_0)

    table_data[n + 1][0] = r'$dx$'
    table_data[n + 1][1] = "{:.2f}".format(x1_dx)
    table_data[n + 1][2] = "{:.2f}".format(x2_dx)
    table_data[n + 1][3] = "{:.2f}".format(x3_dx)

    axs_page1.axis('off')
    col_label = (r'$n$', r'$X_{1}$', r'$X_{2}$', r'$X_{3}$', r'$Y$', '', r'$X_{N1}$', r'$X_{N2}$', r'$X_{N3}$')
    the_table = axs_page1.table(cellText=table_data, colLabels=col_label, loc='best')
    the_table.set_fontsize(20)
    the_table.scale(1.0, 4.0)

    the_table[(target_point + 1, 4)].set_facecolor("#1ac3f5")

    plt.show()

    # fig_page2.savefig("E:\Krut1la\KPI\Grade 2\Part 2\Algorithms\Labs\Lab3\lab3_sin_fig_1.png")
    # fig_page1.savefig("E:\Krut1la\KPI\Grade 2\Part 2\Algorithms\Labs\Lab3\lab3_sin_fig_2.png")


main()