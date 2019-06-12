import os
import sys
import time
import numpy as np
import matplotlib.pyplot as plt

ROOT_DIR: str = os.path.dirname(
    os.path.dirname(__file__)
)

sys.path.append(ROOT_DIR)

from kursach.utils import seconds_to_human
from kursach.cli import parse_cli_args
import numpy as np
from kursach.evaluating_method import evaluating_method
from kursach.random_method import random_method
from kursach.greedy_algorithm import greedy_algorithm


PULL = 10
REPEATS = 10  # number of repeats without changes
K = 3


def main():
    parsed_args = parse_cli_args()

    evaluating_type = parsed_args.evaluating_type

    if evaluating_type == 'loop':

        t_g = []
        t_e = []
        t_r = []
        target_g = []
        target_e = []
        target_r = []
        dimension = []

        range_file_path = parsed_args.range_file_path

        with open(range_file_path, 'r') as input_file:
            m2, m1, n = input_file.readline().split()
            a1, b1 = input_file.readline().split()
            a2, b2 = input_file.readline().split()
            a3, b3 = input_file.readline().split()
            a4, b4 = input_file.readline().split()
            a5, b5 = input_file.readline().split()

            m2 = int(m2)
            m1 = int(m1)
            n = int(n)

        for i in range(10):
            A = np.array(np.random.randint(int(a1), int(b1), size=(m1 + m2)))
            B = np.array(np.random.randint(int(a2), int(b2), size=n))
            while A.sum() < B.sum():
                A = np.array(np.random.randint(int(a1), int(b1), size=(m1 + m2)))
                B = np.array(np.random.randint(int(a2), int(b2), size=n))
            C = np.array(np.random.randint(int(a3), int(b3), size=((m1 + m2), n)))
            D = np.array(np.random.randint(int(a4), int(b4), size=m2))
            P = np.array(np.random.randint(int(a5), int(b5), size=(m1 + m2)))

            print('#', i, 'm1:', m1, ' m2:', m2, ' n:', n)

            # print(A, B, C, D, P)

            start_time = time.time()
            result, y = greedy_algorithm(A, B, C, D, P, int(m1), int(m2))
            end_time = time.time()
            total_time = round(end_time - start_time)

            t_g.append(total_time)
            target_g.append(result)

            print('Result Greedy algorithm: ', result, np.array(y))
            print('Time Greedy algorithm: ', seconds_to_human(total_time))
            print('\n')

            start_time = time.time()
            record, record_layout, target_range= evaluating_method(A, B, C, D, P, m1, m2, PULL, REPEATS, K)
            end_time = time.time()
            total_time = round(end_time - start_time)

            t_e.append(total_time)
            target_e.append(record[0])

            print('Result Evaluation method: ', record, record_layout)
            print('Time Evaluation method: ', seconds_to_human(total_time))
            print('\n')

            start_time = time.time()
            record, record_layout, target_range = random_method(A, B, C, D, P, m1, m2, PULL,
                                                  REPEATS, K)
            end_time = time.time()
            total_time = round(end_time - start_time)

            t_r.append(total_time)
            target_r.append(record[0])

            print('Result Random method: ', record, record_layout)
            print('Time Random method: ', seconds_to_human(total_time))
            print('--------------------------------------------------')
            print('\n')

            # m1 = int(1 + m1)
            m2 = int(1 + m2)
            # n = int(1 + n)

            dimension.append(m2)

        plt.figure(figsize=(9, 3))

        plt.subplot(131)
        plt.plot(dimension, t_g, label='greedy')
        plt.plot(dimension, t_e, label='evaluation')
        plt.plot(dimension, t_r, label='random')
        plt.xlabel('dimension')
        plt.ylabel('time')

        plt.subplot(132)
        width = 0.2  # the width of the bars
        ind = np.arange(len(dimension))
        plt.bar(ind-width*1.5, target_g, width, label='greedy')
        plt.bar(ind-width*0.5, target_e, width, label='evaluation')
        plt.bar(ind+width*0.5, target_r, width, label='random')
        plt.xlabel('dimension')
        plt.ylabel('target')

        plt.legend()
        plt.show()

    elif evaluating_type == 'single':
        input_type = parsed_args.input_type

        if input_type == 'range':

            range_file_path = parsed_args.range_file_path

            with open(range_file_path, 'r') as input_file:
                m2, m1, n = input_file.readline().split()

                m2 = int(m2)
                m1 = int(m1)
                n = int(n)

                a, b = input_file.readline().split()
                A = np.array(np.random.randint(a, b, size=(m1 + m2)))

                a, b = input_file.readline().split()
                B = np.array(np.random.randint(a, b, size=n))

                a, b = input_file.readline().split()
                C = np.array(np.random.randint(a, b, size=((m1 + m2), n)))

                a, b = input_file.readline().split()
                D = np.array(np.random.randint(a, b, size=m2))

                a, b = input_file.readline().split()
                P = np.array(np.random.randint(a, b, size=(m1 + m2)))

            print('A:', A)
            print('B:', B)
            print('C:', C)
            print('D:', D)
            print('P:', P)

        elif input_type == 'file':
            input_file_path = parsed_args.file_path

            with open(input_file_path, 'r') as input_file:
                m2, m1, n = input_file.readline().split()

                A = input_file.readline().split()
                B = input_file.readline().split()
                D = input_file.readline().split()
                P = input_file.readline().split()
                C = input_file.read().split()

                m2 = int(m2)
                m1 = int(m1)
                n = int(n)

                A = np.array(A).astype(np.int)
                B = np.array(B).astype(np.int)
                C = np.array(C).astype(np.int).reshape(m1+m2, n)
                D = np.array(D).astype(np.int)
                P = np.array(P).astype(np.int)

                print('A:', A)
                print('B:', B)
                print('C:', C)
                print('D:', D)
                print('P:', P)

        start_time = time.time()
        result = greedy_algorithm(A, B, C, D, P, m1, m2)
        end_time = time.time()
        total_time = round(end_time - start_time)

        print('Result Greedy algorithm: ', result)
        print('Time Greedy algorithm: ', seconds_to_human(total_time))

        plt.figure(figsize=(9, 3))

        start_time = time.time()
        record, record_layout, target_range = evaluating_method(A, B, C, D, P,
                                                                m1, m2, PULL,
                                                                REPEATS, K)
        end_time = time.time()
        total_time = round(end_time - start_time)

        print('Result Evaluation method: ', record, record_layout)
        print('Time Evaluation method: ', seconds_to_human(total_time))
        plt.subplot(131)
        x = np.arange(len(target_range))
        plt.plot(x, target_range, label='evaluation')

        start_time = time.time()
        record, record_layout, target_range = random_method(A, B, C, D, P, m1,
                                                            m2, PULL,
                                                            REPEATS, K)
        end_time = time.time()
        total_time = round(end_time - start_time)

        print('Result Random method: ', record, record_layout)
        print('Time Random method: ', seconds_to_human(total_time))

        plt.subplot(132)
        x = np.arange(len(target_range))
        plt.plot(x, target_range, label='evaluation')

        plt.ylabel('target')

        plt.legend()
        plt.show()


if __name__ == '__main__':
    main()
