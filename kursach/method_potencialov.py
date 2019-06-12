import numpy as np


def target_function(d, p, c, x, y):
    z = sum(d*y) + sum(sum(c*x)) + sum(p*sum(x.transpose()))
    return z


def potential(a, b, c):
    a, b, c = balance(a, b, c)
    x = dbr(a, b)
    v, u = find_potentials(x, c)
    delta_c = calculate_delta_c(c, v, u)
    optimum = check_optimum(delta_c)
    while not optimum:
        max_i, max_j = find_max_diff(delta_c)
        x[max_i][max_j] = 0
        x_copy = clipping(x)
        loop = find_loop(x_copy, max_i, max_j)
        min_x, min_i, min_j = find_min_x(x, loop)
        try:
            x = new_dbr(x, loop, min_x)
            if not check_degeneracy(x):
                x[min_i][min_j] = -1
            v, u = find_potentials(x, c)
            delta_c = calculate_delta_c(c, v, u)
            optimum = check_optimum(delta_c)
        except:
            optimum = True
    return x


def dbr(a, b):
    x = np.array([[-1 for _ in range(len(b))] for _ in range(len(a))])
    for i in range(len(a)):
        for j in range(len(b)):
            result = min(a[i], b[j])
            a[i] -= result
            b[j] -= result
            if result != 0:
                x[i][j] = result
    return x


def balance(a, b, c):
    sum_a = sum(a)
    sum_b = sum(b)
    diff = abs(sum_a-sum_b)

    if sum_a < sum_b:
        a = np.append(a, diff)
        c = np.append(c, [[0 for _ in range(len(b))]], axis=0)
    elif sum_a > sum_b:
        b = np.append(b, diff)
        c = np.append(c, [[0] for _ in range(len(a))], axis=1)
    return a, b, c


def check_degeneracy(x):
    counter = 0
    for i in range(len(x)):
        for j in range(len(x[0])):
            if x[i][j] >= 0:
                counter += 1
    if counter == (len(x)+len(x[0])-1):
        return True
    else:
        return False


def find_potentials(x, c):
    row = 0
    u = [-1 for _ in range(len(x)-1)]
    u.insert(0, 0)
    v = [-1 for _ in range(len(x[0]))]
    v, u = go_row(x, c, v, u, row)
    return v, u


def go_row(x, c, v, u, i):
    for j in range(len(x[0])):
        if x[i][j] > 0 and v[j] == -1:
            v[j] = c[i][j] - u[i]
            v, u = go_column(x, c, v, u, j)
    return v, u


def go_column(x, c, v, u, j):
    for i in range(len(x)):
        if x[i][j] > 0 and u[i] == -1:
            u[i] = c[i][j] - v[j]
            v, u = go_row(x, c, v, u, i)
    return v, u


def calculate_delta_c(c, v, u):
    delta_c = np.array([[0 for _ in range(len(c[0]))] for _ in range(len(c))])
    for i in range(len(c)):
        for j in range(len(c[0])):
            delta_c[i][j] = c[i][j] - u[i] - v[j]
    return delta_c


def check_optimum(delta_c):
    for i in range(len(delta_c)):
        for j in range(len(delta_c[0])):
            if delta_c[i][j] < 0:
                return False
    return True


def find_max_diff(delta_c):
    max_diff = 0
    max_i = 0
    max_j = 0
    for i in range(len(delta_c)):
        for j in range(len(delta_c[0])):
            if delta_c[i][j] < 0 and max_diff > delta_c[i][j]:
                max_diff = delta_c[i][j]
                max_i = i
                max_j = j
    return max_i,  max_j


def find_loop(x, max_i, max_j):
    loop = []
    loop = go_row_loop(x, loop, max_i, max_j)
    return loop


def clipping(x):
    x_copy = x.copy()
    flag = True
    while flag:
        flag = False
        for i in range(len(x)):
            counter = 0
            for j in range(len(x[0])):
                if x_copy[i][j] >= 0:
                    counter += 1
            if counter == 1:
                for j in range(len(x[0])):
                    x_copy[i][j] = -1
                flag = True

        for j in range(len(x[0])):
            counter = 0
            for i in range(len(x)):
                if x_copy[i][j] >= 0:
                    counter += 1
            if counter == 1:
                for i in range(len(x)):
                    x_copy[i][j] = -1
                flag = True
    return x_copy


def go_row_loop(x1, loop, i, k):
    x = x1.copy()
    for j in range(len(x[0])):
        if x[i][j] >= 0 and j != k:
            x[i][j] = -1
            go_column_loop(x, loop, i, j)
            loop.append((i, j))
    return loop


def go_column_loop(x1, loop, k, j):
    x = x1.copy()
    for i in range(len(x)):
        if x[i][j] >= 0 and i != k:
            x[i][j] = -1
            go_row_loop(x, loop, i, j)
            loop.append((i, j))
    return loop


def find_min_x(x, loop):
    min_x = 1000000000
    min_i = 0
    min_j = 0
    for k in range(1, len(loop), 2):
        i, j = loop[k]
        if x[i][j] < min_x:
            min_x = x[i][j]
            min_i = i
            min_j = j
    return min_x, min_i, min_j


def new_dbr(x, loop, min_x):
    i, j = loop[0]
    x[i][j] = min_x
    for k in range(1, len(loop), 2):
        i, j = loop[k]
        x[i][j] -= min_x
    for k in range(2, len(loop), 2):
        i, j = loop[k]
        x[i][j] += min_x
    return x


def evaluating(a, b, c, d, p, y):
    x = potential(a, b, c)
    new_x = np.array([[0 for _ in range(len(b))] for _ in range(len(a))])
    for i in range(len(a)):
        for j in range(len(b)):
            if x[i][j] > 0:
                new_x[i][j] = x[i][j]
    x = new_x
    result = target_function(d, p, c, x, y)
    return result
