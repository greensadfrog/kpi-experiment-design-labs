import random
from tabulate import tabulate
import math
import numpy as np

variantNumber = 7

Ymax = (30 - variantNumber) * 10
Ymin = (20 - variantNumber) * 10

m = 5
Rcriterion = 2

X1min = -5
X1max = 15
normX1min = 0
normX1max = 1

X2min = -35
X2max = 10
normX2min = 0
normX2max = 1

# -----Матриця планування, середнє значення, дисперсії по рядках------

planningMatrix = [[random.randint(Ymin, Ymax) for y in range(m)] for row in range(3)]
avgYList = [round(sum(planningMatrix[i]) / len(planningMatrix[i]), 1) for i in range(3)]
dispList = [
    [round(sum(((planningMatrix[j][i] - avgYList[j]) ** 2) for i in range(m)) / m, 1)] for j in range(len(avgYList))]

# -----Основне відхилення-----

mainDispersion = round(math.sqrt((2 * (2 * m - 2)) / (m * (m - 4))), 1)

# -----Fvu, θvu, Rvu -----
Fvu1List = [0, 0, 0]
Fvu1List[0] = round(dispList[0][0] / dispList[1][0], 1) if dispList[0][0] >= dispList[1][0] else round(
    dispList[1][0] / dispList[0][0], 1)
Fvu1List[1] = round(dispList[0][0] / dispList[2][0], 1) if dispList[0][0] >= dispList[2][0] else round(
    dispList[2][0] / dispList[0][0], 1)
Fvu1List[2] = round(dispList[2][0] / dispList[1][0], 1) if dispList[2][0] >= dispList[1][0] else round(
    dispList[1][0] / dispList[2][0], 1)

ThetaList = [round(((m - 2) / m) * i, 1) for i in Fvu1List]
RvuList = [round((math.fabs(ThetaList[i] - 1)) / mainDispersion, 1) for i in range(len(ThetaList))]

# -----Розрахунок нормованих коефіцієнтів рівняння регресії-----

mx1 = (normX1min + normX1max + normX1min) / 3
mx2 = (normX2min + normX2min + normX2max) / 3

my = sum(avgYList) / 3

a1 = (normX1min ** 2 + normX1max ** 2 + normX1min ** 2) / 3
a2 = (normX1min * normX2min + normX1max * normX2min + normX1min * normX2max) / 3
a3 = (normX2min ** 2 + normX2min ** 2 + normX2max ** 2) / 3

a11 = (normX1min * avgYList[0] + normX1max * avgYList[1] + normX1min * avgYList[2]) / 3
a22 = (normX2min * avgYList[0] + normX2min * avgYList[1] + normX2max * avgYList[2]) / 3

b0 = np.linalg.det(np.array([[my, mx1, mx2], [a11, a1, a2], [a22, a2, a3]])) / \
     np.linalg.det(np.array([[1, mx1, mx2], [mx1, a1, a2], [mx2, a2, a3]]))

b1 = np.linalg.det(np.array([[1, my, mx2], [mx1, a11, a2], [mx2, a22, a3]])) / \
     np.linalg.det(np.array([[1, mx1, mx2], [mx1, a1, a2], [mx2, a2, a3]]))

b2 = np.linalg.det(np.array([[1, mx1, my], [mx1, a1, a11], [mx2, a2, a22]])) / \
     np.linalg.det(np.array([[1, mx1, mx2], [mx1, a1, a2], [mx2, a2, a3]]))

# -----Натуралізація коефіцієнтів-----
deltaX1 = abs(X1max - X1min) / 2
deltaX2 = abs(X2max - X2min) / 2

x10 = (X1max + X1min) / 2
x20 = (X2max + X2min) / 2

natural_a0 = b0 - b1 * x10 / deltaX1 - b2 * x20 / deltaX2
natural_a1 = b1 / deltaX1
natural_a2 = b2 / deltaX2

# -----Вивід результатів-----

print("\n Матриця планування:")
print(
    tabulate(
        [["X1", "X2", "Y1", "Y2", "Y3", "Y4", "Y5", "Середній Y", "Fvu", "θvu", "Rvu"],
         [normX1min] + [normX2min] + planningMatrix[0] + [avgYList[0]],
         [normX1max] + [normX2min] + planningMatrix[1] + [avgYList[1]],
         [normX1min] + [normX2max] + planningMatrix[2] + [avgYList[2]]],
        headers="firstrow", tablefmt="pretty"))

print("\n Дисперсія по рядках")
print(tabulate(dispList, tablefmt="pretty"))
print("\n Основне відхилення = " + str(mainDispersion))

print("\n Дані для критерію Романовського:")
print(tabulate([
    ["№", "Fvu", "θvu", "Rvu"],
    [1, Fvu1List[0], ThetaList[0], RvuList[0]],
    [2, Fvu1List[1], ThetaList[1], RvuList[1]],
    [3, Fvu1List[2], ThetaList[2], RvuList[2]]],
    headers="firstrow", tablefmt="pretty"))

if max(RvuList) >= Rcriterion:
    print("Дисперсія не однорідна, "
          "потрібно повторити експеримент.")
else:
    print("\n--------------------")
    print("Дисперсія однорідна.")
    print("--------------------\n")

    print("Нормовані коефіцієнти рівняння регресії:")
    print(tabulate([["b0", "b1", "b2"],
                    [round(b0, 1), round(b1, 1), round(b2, 1)]], headers="firstrow", tablefmt="pretty"))

    print("\nНормоване рівняння регресії:")
    print(
        "Y=" + str(round(b0, 1)) + "+" + '(' + str(round(b1, 1)) + ')' + "*x1+" + '(' + str(round(b2, 1)) + ')' + "*x2")

    print("\n Перевірка: ")
    print(tabulate([["Розраховані значення Y", "Середній Y"],
                    [round(b0 + round(b1 * normX1min, 1) + round(b2 * normX2min), 1), avgYList[0]],
                    [round(b0 + round(b1 * normX1max, 1) + round(b2 * normX2min), 1), avgYList[1]],
                    [round(b0 + round(b1 * normX1min, 1) + round(b2 * normX2max), 1), avgYList[2]]],
                   headers="firstrow", tablefmt="pretty"))

    print("\nНатуралізовані коефіцієнти:")
    print(tabulate([["a0", "a1", "a2"],
                    [round(natural_a0, 1), round(natural_a1, 1), round(natural_a2, 1)]], headers="firstrow",
                   tablefmt="pretty"))
    print("\nНатуралізоване рівняння регресії:")
    print(
        "\n Y=" + str(round(natural_a0, 1)) + "+" + '(' + str(round(natural_a1, 1)) + ')' + "*x1+" + '(' + str(
            round(natural_a2, 1)) + ')' + "*x2")

    print("\n Перевірка: ")
    print(tabulate([["Розраховані значення Y", "Середній Y"],
                    [round(natural_a0 + natural_a1 * X1min + natural_a2 * X2min, 1), avgYList[0]],
                    [round(natural_a0 + natural_a1 * X1max + natural_a2 * X2min, 1), avgYList[1]],
                    [round(natural_a0 + natural_a1 * X1min + natural_a2 * X2max, 1), avgYList[2]]],
                   headers="firstrow", tablefmt="pretty"))
