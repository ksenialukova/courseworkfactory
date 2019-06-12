from kursach.method_potencialov import evaluating
from kursach.utils import prepare_matrix


def greedy_algorithm(a, b, c, d, p, m1, m2):
    y = [0 for _ in range(m2)]
    sum_a = a[:-len(d)].sum()
    sum_b = b.sum()
    ind = d.argsort()
    k = 0
    while sum_a < sum_b:
        y[ind[k]] = 1
        sum_a += d[ind[k]]
        k += 1

    a, p, c = prepare_matrix(a, p, c, y, m1)

    result = evaluating(a, b, c, d, p, y)
    return result, y
