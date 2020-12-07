from math import exp
import numpy as np
from numpy.random import choice
from pokemon import GameStatus, Pokemon

# start assuming all nodes are simultaneous

sor_dict = {}

ETA = .1
EPS = .1


def exp_ser(ser):
    return np.array([exp(EPS * x) for x in ser])


def get_p(s):
    sum_exp_0 = np.sum(exp_ser(s.ser[0]))
    C1 = sum_exp_0 / (1 - len(s.actions[0]) * ETA)
    sum_exp_1 = np.sum(exp_ser(s.ser[1]))
    C2 = sum_exp_1 / (1 - len(s.actions[1]) * ETA)
    p1 = ETA + exp_ser(s.ser[0]) / C1
    p2 = ETA + exp_ser(s.ser[1]) / C2
    return p1, p2


def uct_gsa(s0, max_it):
    it = 0
    while it < max_it:
        it += 1
        s = s0
        while not(s.ended()):
            p0, p1 = get_p(s)
            a0 = choice(s.actions[0], 1, p=p0)
            a1 = choice(s.actions[1], 1, p=p1)
            s1 = s.step([a0[0], a1[0]])


if __name__ == "__main__":
    scyther = Pokemon(name="Scyther", item="Eviolite", evs={'atk': 252, 'spe': 252}, nature="Jolly",
                      trait="Technician", moves=["Bug Bite", "Aerial Ace", "Brick Break", "Swords Dance"])
    gengar = Pokemon(name="Gengar", item="Black Sludge", evs={'spa': 252, 'spe': 252}, nature="Timid",
                     trait="Levitate", moves=["Shadow Ball", "Focus Blast", "Sludge Bomb", "Substitute"])
    G = GameStatus([scyther], [gengar], 0, 0)
    uct_gsa(G, 100)
