import random

# matrix generation from the results of the experiment
experimentMatrix = [[random.randint(0, 20) for _ in range(3)] for _ in range(8)]

print("---Результати експерименту---")
print('\n'.join([''.join(['{:8}'.format(item) for item in row]) for row in experimentMatrix]))

# the central moment of the experiment (x0) and factor change interval (Dx)
x0List = list()
DxList = list()

for i in range(len(experimentMatrix) - (len(experimentMatrix) - len(experimentMatrix[0]))):
    column = [row[i] for row in experimentMatrix]
    x0List.append((max(column) - min(column)) / 2)
    DxList.append(((max(column) - min(column)) / 2) - min(column))

print("\n---Центральні моменти експерименту---")
print("X0: ", x0List)
print("\n---Інтервали зміни фактора---")
print("Dx: ", DxList)

# generation of coefficients (a0, a1, a2, a3)
coeffList = [random.randint(0, 20) for _ in range(4)]

print("\n---Коефіцієнти:---")
print('a0 =', coeffList[0], '\na1 =', coeffList[1], '\na2 =', coeffList[2], '\na3 =', coeffList[3])

# feedback function (Y)
y = list()
for expResultList in experimentMatrix:
    y.append(coeffList[0] + sum([i * j for i, j in zip(expResultList, coeffList[1:])]))

print("\n---Функуція відгуків для кожної точки---")
print('Y:', y)

# matrix of normalized values
normalizedMatrix = list()
for i in range(len(experimentMatrix) - 1):
    normalizedMatrix.append([round((x - x0) / dx, 2) for x0, dx, x in zip(x0List, DxList, experimentMatrix[i])])

print("\n---Матриця нормалізованих значень---")
print('\n'.join([''.join(['{:8}'.format(item) for item in row]) for row in normalizedMatrix]))

# feedback function in the center of experiment (Yet)
Yet = coeffList[0] + sum([i * j for i, j in zip(x0List, coeffList[1:])])

print("\n---Функуція відгуків для еталонних точок---")
print("Yет =", Yet)

# Variant 207:  (--> Yет)
supplementedY = y.copy()
supplementedY.append(Yet)
supplementedY.sort()

print("\nВаріант 207: Критерій вибору -->Yет")
print("-->Yет =", supplementedY.pop(supplementedY.index(Yet) - 1))