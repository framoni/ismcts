from math import exp
import numpy as np
from pokemon import GameStatus, Pokemon

# start assuming all nodes are simultaneous

sor_dict = {}

ETA = 1
EPS = 1


def e(sor):
    return np.array([exp(EPS * x) for x in sor])


def get_p(s):
    p1 = ETA + exp(EPS * s.sor[0]) / c1
    p2 = ETA + exp(EPS * s.sor[1]) / c2
    return p1, p2


def  uct_gsa(s0, max_it):
    it = 0
    while it < max_it:
        it += 1
        s = s0
        while not(s.ended()):
            p1, p2 = get_p(s)
            # pick actions correponding to max probabilities...


if __name__ == "__main__":
    scyther = Pokemon(moves=["Bug Bite", "Aerial Ace", "Brick Break", "Swords Dance"])
    gengar = Pokemon(moves=["Shadow Ball", "Focus Blast", "Sludge Bomb", "Substitute"])
    G = GameStatus([scyther], [gengar], scyther, gengar)
    uct_gsa(G, 100)