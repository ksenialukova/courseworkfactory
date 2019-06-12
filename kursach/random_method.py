import numpy as np

from kursach.method_potencialov import evaluating
from kursach.utils import generation_start_pull, prepare_matrix, unique_rows


def random_method(a, b, c, d, p, m1, m2, pull, repeats, k):
    Y = generation_start_pull(pull, m1, m2, a, b)

    origin_sum_a = a[:m1].sum()
    non_build_a = a[m1:]

    repeat = 0
    record = 10000000000000

    target_range = []

    while repeat < repeats:
        prev_record = record

        targets = np.empty((0, 0), int)

        for y in Y:
            plan_a, plan_p, plan_c = prepare_matrix(a, p, c, y, m1)

            target = evaluating(plan_a, b, plan_c, d, plan_p, y)
            targets = np.append(targets, target)

        ind = targets.argsort()[k:]

        record_ind = targets.argsort()[:1]
        record = targets[record_ind]
        target_range.append(record[0])
        if prev_record > record:
            record_layout = Y[record_ind]
            repeat = 0
        else:
            record = prev_record

        # print(record, record_layout)

        Y = np.delete(Y, ind, axis=0)

        for y in Y:
            local_pull = np.empty((0, m2), int)
            for i in range(len(y)):
                new_y = y.copy()
                if y[i] == 0:
                    new_y[i] = 1
                elif y[i] == 1:
                    new_y[i] = 0
                sum_a = origin_sum_a + (non_build_a * new_y).sum()
                if sum_a >= b.sum():
                    local_pull = np.append(local_pull, [new_y], axis=0)
            ind = np.array(np.random.randint(int(pull / 2), size=(int(m2 / 2))))
            local_pull = np.delete(local_pull, ind, axis=0)
            Y = np.append(Y, local_pull, axis=0)

        Y = unique_rows(Y)
        # print(repeat)
        repeat += 1

    return record, record_layout[0], target_range
