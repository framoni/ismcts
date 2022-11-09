import numpy as np
from uct_exp3 import get_p

from itertools import combinations

class S:
    def __init__(self):
        self.actions = [[1, 2], [1, 2]]
        self.ser = [
            np.array([0] * len(self.actions[0]), dtype=float),
            np.array([0] * len(self.actions[1]), dtype=float)
        ]


s = S()


def main():
    for c in combinations(np.linspace(0, 1, 11), 2):
        ETA = c[0]
        EPS = c[1]
        # for f in np.linspace(0, 2, 20):
        s.ser = [
            np.array([3.06, 1.96, 2.07, 2.02], dtype=float),
            np.array([0, 1], dtype=float)
        ]
        print('ETA: {}, EPS: {}'.format(ETA, EPS))
        print('SER: {}'.format(s.ser[0]))
        print(get_p(s, ETA, EPS)[0])


if __name__ == "__main__":
    main()
