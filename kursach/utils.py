import numpy as np


def prepare_matrix(a, p, c, y, m1):
    i, = np.where(y == 0)
    c = np.delete(c, i + m1, axis=0)
    p = np.delete(p, i + m1, axis=0)
    a = np.delete(a, i + m1, axis=0)

    c = c + p.reshape(p.shape[0], 1)

    return a, p, c


def generation_start_pull(pull, m1, m2, a, b):
    Y = np.empty((0, 0))
    origin_sum_a = a[:m1].sum()
    non_build_a = a[m1:]
    while Y.shape[0] < pull / 2:
        Y = np.array(np.random.randint(2, size=(pull, m2)))
        sum_a = origin_sum_a + (non_build_a * Y).sum(axis=1)
        i, = np.where(sum_a < b.sum())
        Y = np.delete(Y, i, axis=0)

    return Y


def unique_rows(a):
    a = np.ascontiguousarray(a)
    unique_a = np.unique(a.view([('', a.dtype)]*a.shape[1]))
    return unique_a.view(a.dtype).reshape((unique_a.shape[0], a.shape[1]))


def validate_input_data():
    pass


def seconds_to_human(sec: int) -> str:
    h = sec // 3600
    m = (sec - h*3600) // 60
    s = sec - m*60 - h*3600
    return f"{h}h {m}m {s}s"
