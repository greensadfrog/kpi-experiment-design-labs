from tabulate import tabulate
import random, math
import numpy as np
from scipy.stats import f  # ось використовується scipy
from scipy.stats import t

# Variant 207

listOfXmin = [-5, -35, -35]
listOfXmax = [15, 10, -10]

x1List = (-5, -5, 15, 15)
x2List = (-35, 10, -35, 10)
x3List = (-35, -10, -10, -35)

norm_listOfXmin = [-1, -1, -1]
norm_listOfXmax = [1, 1, 1]

normValuesOfX0 = [1, 1, 1, 1]
normValuesOfX1 = [-1, -1, 1, 1]
normValuesOfX2 = [-1, 1, -1, 1]
normValuesOfX3 = [-1, 1, 1, -1]

Ymax = 200 + sum(listOfXmax) / 3
Ymin = 200 + sum(listOfXmin) / 3

m = 3
N = 4

# generation Y - experiment result
listY = [[random.randint(Ymin, Ymax) for y in range(m)] for row in range(N)]
avgYList = [round(sum(listY[i]) / len(listY[i]), 1) for i in range(len(listY))]

mx = [0, 0, 0]
#             x11                 x12            13               x14
mx[0] = (listOfXmin[0] + listOfXmin[0] + listOfXmax[0] + listOfXmax[0]) / N
mx[1] = (listOfXmin[1] + listOfXmax[1] + listOfXmin[1] + listOfXmax[1]) / N
mx[2] = (listOfXmin[2] + listOfXmax[2] + listOfXmax[2] + listOfXmin[2]) / N

my = sum(avgYList) / 4

a1 = (listOfXmin[0] * avgYList[0] + listOfXmin[0] * avgYList[1] + listOfXmax[0] * avgYList[2] + listOfXmax[0] *
      avgYList[3]) / N
a2 = (listOfXmin[1] * avgYList[0] + listOfXmax[1] * avgYList[1] + listOfXmin[1] * avgYList[2] + listOfXmax[1] *
      avgYList[3]) / N
a3 = (listOfXmin[2] * avgYList[0] + listOfXmax[2] * avgYList[1] + listOfXmax[2] * avgYList[2] + listOfXmin[2] *
      avgYList[3]) / N

a11 = (listOfXmin[0] ** 2 + listOfXmin[0] ** 2 + listOfXmax[0] ** 2 + listOfXmax[0] ** 2) / N
a22 = (listOfXmin[1] ** 2 + listOfXmax[1] ** 2 + listOfXmin[1] ** 2 + listOfXmax[1] ** 2) / N
a33 = (listOfXmin[2] ** 2 + listOfXmax[2] ** 2 + listOfXmax[2] ** 2 + listOfXmin[2] ** 2) / N

a12 = (listOfXmin[0] * listOfXmin[1] + listOfXmin[0] * listOfXmax[1] + listOfXmax[0] * listOfXmin[1] + listOfXmax[0] *
       listOfXmax[1]) / N
a13 = (listOfXmin[0] * listOfXmin[2] + listOfXmin[0] * listOfXmax[2] + listOfXmax[0] * listOfXmax[2] + listOfXmax[0] *
       listOfXmin[2]) / N
a23 = (listOfXmin[1] * listOfXmin[2] + listOfXmax[1] * listOfXmax[2] + listOfXmin[1] * listOfXmax[2] + listOfXmax[1] *
       listOfXmin[2]) / N

a21, a31, a32 = a12, a13, a23

bList = []

b0 = round(np.linalg.det(np.array([[my, mx[0], mx[1], mx[2]],
                                   [a1, a11, a12, a13],
                                   [a2, a12, a22, a32],
                                   [a3, a13, a23, a33]])) / np.linalg.det(np.array([[1, mx[0], mx[1], mx[2]],
                                                                                    [mx[0], a11, a12, a13],
                                                                                    [mx[1], a12, a22, a32],
                                                                                    [mx[2], a13, a23, a33]])), 1)
b1 = round(np.linalg.det(np.array([[1, my, mx[1], mx[2]],
                                   [mx[0], a1, a12, a13],
                                   [mx[1], a2, a22, a32],
                                   [mx[2], a3, a23, a33]])) / np.linalg.det(np.array([[1, mx[0], mx[1], mx[2]],
                                                                                      [mx[0], a11, a12, a13],
                                                                                      [mx[1], a12, a22, a32],
                                                                                      [mx[2], a13, a23, a33]])), 1)
b2 = round(np.linalg.det(np.array([[1, mx[1], my, mx[2]],
                                   [mx[0], a11, a1, a13],
                                   [mx[1], a12, a2, a32],
                                   [mx[2], a13, a3, a33]])) / np.linalg.det(np.array([[1, mx[0], mx[1], mx[2]],
                                                                                      [mx[0], a11, a12, a13],
                                                                                      [mx[1], a12, a22, a32],
                                                                                      [mx[2], a13, a23, a33]])), 2)
b3 = round(np.linalg.det(np.array([[1, mx[1], mx[2], my],
                                   [mx[0], a11, a12, a1],
                                   [mx[1], a12, a22, a2],
                                   [mx[2], a13, a23, a3]])) / np.linalg.det(np.array([[1, mx[0], mx[1], mx[2]],
                                                                                      [mx[0], a11, a12, a13],
                                                                                      [mx[1], a12, a22, a32],
                                                                                      [mx[2], a13, a23, a33]])), 2)
bList.append(b0)
bList.append(b1)
bList.append(b2)
bList.append(b3)

print(tabulate([["X1", "X2", "X3", "Y1", "Y2", "Y3", "Avg Y"],
                listOfXmin + listY[0] + [avgYList[0]],
                [listOfXmin[0]] + listOfXmax[1:] + listY[1] + [avgYList[1]],
                [listOfXmax[0]] + [listOfXmin[1]] + [listOfXmax[2]] + listY[2] + [avgYList[2]],
                listOfXmax[0:2] + [listOfXmin[2]] + listY[3] + [avgYList[3]]],
               headers="firstrow", tablefmt="pretty"))
print(tabulate([["MX1", "MX2", "MX3"], mx],
               headers="firstrow", tablefmt="pretty"))
print(tabulate([["b0", "b1", "b2", "b3"],
                [b0] + [b1] + [b2] + [b3]],
               headers="firstrow", tablefmt="pretty"))
print("y = " + str(b0) + '+ (' + str(b1) + ") * x1 + (" + str(b2) + ") * x2 + (" + str(b3) + ") * x3")

print("Перевірка:")
print("b0+x1min*b1+x2min*b2+x3min*b3 = ", round(b0 + listOfXmin[0] * b1 + listOfXmin[1] * b2 + listOfXmin[2] * b3, 2))
print("b0+x1min*b1+x2max*b2+x3max*b3 = ", round(b0 + listOfXmin[0] * b1 + listOfXmax[1] * b2 + listOfXmax[2] * b3, 2))
print("b0+x1max*b1+x2min*b2+x3max*b3 = ", round(b0 + listOfXmax[0] * b1 + listOfXmin[1] * b2 + listOfXmax[2] * b3, 2))
print("b0+x1max*b1+x2max*b2+x3min*b3 = ", round(b0 + listOfXmax[0] * b1 + listOfXmax[1] * b2 + listOfXmin[2] * b3, 2))

print(tabulate([["X1", "X2", "X3", "Y1", "Y2", "Y3", "Avg Y"],
                norm_listOfXmin + listY[0] + [avgYList[0]],
                [norm_listOfXmin[0]] + norm_listOfXmax[1:] + listY[1] + [avgYList[1]],
                [norm_listOfXmax[0]] + [norm_listOfXmin[1]] + [norm_listOfXmax[2]] + listY[2] + [avgYList[2]],
                norm_listOfXmax[0:2] + [norm_listOfXmin[2]] + listY[3] + [avgYList[3]]],
               headers="firstrow", tablefmt="pretty"))
# Критерій Кохрена
# дисперсії по рядках
print("=================Критерій Кохрена=================")
syList = [0, 0, 0, 0]
syList[0] = ((listY[0][0] - avgYList[0]) ** 2 + (listY[0][1] - avgYList[0]) ** 2 + (listY[0][2] - avgYList[0]) ** 2) / 3
syList[1] = ((listY[1][0] - avgYList[1]) ** 2 + (listY[1][1] - avgYList[1]) ** 2 + (listY[1][2] - avgYList[1]) ** 2) / 3
syList[2] = ((listY[2][0] - avgYList[2]) ** 2 + (listY[2][1] - avgYList[2]) ** 2 + (listY[2][2] - avgYList[2]) ** 2) / 3
syList[3] = ((listY[3][0] - avgYList[3]) ** 2 + (listY[3][1] - avgYList[3]) ** 2 + (listY[3][2] - avgYList[3]) ** 2) / 3

syList = [round(i, 2) for i in syList]

Gp = max(syList) / sum(syList)
f1 = m - 1
f2 = N
Gt = 0.7679

if Gp < Gt:
    print("Дисперсія однорідна")
else:
    print("Дисперсія неоднрідна, потрібно повторити екмперимент.")

# Критерій Стьюдента
print("=================Критерій Стьюдента=================")
f3 = f1 * f2
d = 4

Sb = sum(syList) / N
S = math.sqrt(Sb / (N * m))

bettaList = [sum([syList[i] * normValuesOfX0[i] for i in range(N)]) / N,
             sum([syList[i] * normValuesOfX1[i] for i in range(N)]) / N,
             sum([syList[i] * normValuesOfX2[i] for i in range(N)]) / N,
             sum([syList[i] * normValuesOfX3[i] for i in range(N)]) / N]
bettaList = [round(i, 2) for i in bettaList]

tList = [bettaList[i] * S for i in range(N)]

for i in range(N):
    if tList[i] < t.ppf(q=0.975, df=f3):  # ось тут
        bList[i] = 0
        d -= 1
        print('Виключаємо з рівняння коефіціент b' + str(i))

print("y = " + str(bList[0]) + ' + (' + str(bList[1]) + ") * x1 + (" + str(bList[2]) + ") * x2 + (" + str(
    bList[3]) + ") * x3")

# Критерій Фішера
print("=================Критерій Фішера=================")
f4 = N - d
S_ad = (m * sum(
    [(bList[0] + bList[1] * x1List[i] + bList[2] * x2List[i] + bList[3] * x3List[i] - avgYList[i]) ** 2 for i in
     range(N)]) / f4)
Fp = S_ad / Sb

if Fp > f.ppf(q=0.95, dfn=f4, dfd=f3):  # і ось тут
    print('Рівняння регресії неадекватно оригіналу при рівні значимості 0.05')
else:
    print('Рівняння регресії адекватно оригіналу при рівні значимості 0.05')
