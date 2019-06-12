import numpy as np

from kursach.method_potencialov import evaluating
from kursach.utils import prepare_matrix, unique_rows, generation_start_pull


def calculate_deviations(d, c, m1, p):
    non_build_c = c[m1:]
    non_build_p = p[m1:]

    d_average = d.mean()
    p_average = non_build_p.mean()
    ci_average = non_build_c.mean(axis=1).mean()
    cj_average = non_build_c.mean(axis=0)

    d_eval = (d - d_average)/d_average
    p_eval = (non_build_p - p_average)/p_average
    ci_eval = (non_build_c.mean(axis=1) - ci_average)/ci_average
    cj_eval = ((non_build_c - cj_average) / cj_average).sum(axis=1)

    deviations = d_eval+p_eval+ci_eval+cj_eval

    return deviations


def evaluating_method(a, b, c, d, p, m1, m2, pull, repeats, k):
    non_build_a = a[m1:]
    default_a_sum = a[:m1].sum()

    Y = generation_start_pull(pull, m1, m2, a, b)

    deviations = calculate_deviations(d, c, m1, p)

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

        Y = np.delete(Y, ind, axis=0)

        for y in Y:
            local_pull = np.empty((0, m2), int)
            local_deviations = np.empty((0, 0), int)
            for i in range(len(y)):
                new_y = y.copy()
                if y[i] == 0:
                    new_y[i] = 1
                elif y[i] == 1:
                    new_y[i] = 0
                sum_a = default_a_sum + (non_build_a * new_y).sum()
                if sum_a >= b.sum():
                    local_pull = np.append(local_pull, [new_y], axis=0)
                    deviation = (new_y*deviations).sum()
                    local_deviations = np.append(local_deviations, deviation)
            ind = local_deviations.argsort()[int(m2/2):]
            local_pull = np.delete(local_pull, ind, axis=0)
            Y = np.append(Y, local_pull, axis=0)

        Y = unique_rows(Y)
        # print(repeat)
        repeat += 1

    return record, record_layout[0], target_range
