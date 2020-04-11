from math import sqrt
def sqroot(a, b, c):
    D = b ** 2 - 4 * a * c  # вычисляют дискриминант по формуле
    print("Дискриминант D = ", D)

    if D > 0:
        x1 = (-b - sqrt(D)) / (2 * a)
        x2 = (-b + sqrt(D)) / (2 * a)
    print('x1 =', x1, '\nx2 =', x2)

    if D == 0:
        x = -b / (2 * a)
    print('x=', x)

    if D < 0:
        print("Korney net")

