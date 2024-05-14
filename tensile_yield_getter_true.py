# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor




# 最小二乗法で数式を計算する関数
def calculate_least_squares(x_points, y_points):
    A = np.vstack([x_points, np.ones(len(x_points))]).T
    m, c = np.linalg.lstsq(A, y_points, rcond=None)[0]
    return m, c

# 最小二乗法で計算した直線を描写する関数
def draw_least_squares_line(ax, m, c, x_range):
    x_vals = np.array(x_range)
    y_vals = m * x_vals + c
    ax.plot(x_vals, y_vals, 'b-', label=f'y = {m:.2f}x + {c:.2f}')
    ax.legend()



# 2つの直線の傾き(m1, m2)と切片(c1, c2)を受け取り、交点を計算する関数
def calculate_intersection(m1, c1, m2, c2):
    # 両方の直線が同じ傾きを持つ場合、交点は存在しません
    if m1 == m2:
        print("直線は平行であり、交点は存在しません。")
        return None
    # 交点のx座標を計算
    x_intersect = (c2 - c1) / (m1 - m2)
    # 交点のy座標を計算
    y_intersect = m1 * x_intersect + c1
    return (x_intersect, y_intersect)




# クリックイベントの処理
class ClickHandler:
    def __init__(self, figure, ax, line):
        self.figure = figure
        self.ax = ax
        self.line = line
        self.xs = list(line.get_xdata())
        self.ys = list(line.get_ydata())
        self.selected_x = []
        self.line_eq = []

    def __call__(self, event):
        if event.inaxes != self.line.axes: return
        x = event.xdata
        self.selected_x.append(x)
        if len(self.selected_x) == 2:            
            x_min, x_max = sorted(self.selected_x)
            x_range = [x for x in self.xs if x_min <= x <= x_max]
            y_range = [y for x, y in zip(self.xs, self.ys) if x_min <= x <= x_max]
            m, c = calculate_least_squares(np.array(x_range), np.array(y_range))
            self.line_eq.append([m,c])
            
            equation = f'y = {m:.2f}x + {c:.2f}'
            print('Calculated equation:', equation)
            #tk.messagebox.showinfo('Result', f'The calculated linear equation is:\n{equation}')
            
            #self.ax.plot(x_range, y_range, 'blue')
            draw_least_squares_line(self.line.axes, m, c, x_range)
            self.figure.canvas.draw()
            
            self.selected_x = []
            
            intersection = calculate_intersection(*self.line_eq[0], *self.line_eq[-1])
            if intersection != None:
                print(f"交点の座標: {intersection}")
                self.ax.plot(intersection[0], intersection[1], '*', c="green", label=intersection)
            self.ax.legend()
            self.figure.canvas.draw()





# CSVファイルをNumPy配列として読み込む
data = np.genfromtxt("./test_result1.csv", delimiter=',', skip_header=1, encoding="utf-8")
# 1列目と2列目を抽出
x = data[:, 0]
y = data[:, 1]

#公称応力-公称ひずみから真応力-真ひずみに変換
#x = np.log(1 + x)
#y = y*(1 + np.log(1 + x))


# プロットの初期化
fig, ax = plt.subplots()
ax.plot(x, y, 'red', alpha=0.5)

# カーソルの追加
cursor = Cursor(ax, useblit=True, color='red', linewidth=1)

# クリックハンドラーの追加
click_handler = ClickHandler(fig, ax, ax.lines[0])
fig.canvas.mpl_connect('button_press_event', click_handler)

plt.show()
