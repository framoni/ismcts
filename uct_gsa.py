from math import exp
import numpy as np
from numpy.random import choice
from pokemon import GameStatus, Pokemon

# start assuming all nodes are simultaneous

# use as rewards the ratio between the sum of HP % of mons beloning to the player and the same sum calculated for the
# mons of the opponent


sor_dict = {}

ETA = .1
EPS = .1

Kr = .1

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


def get_reward(s):
    r1 = Kr + sum([max(0, p.health) / p.max_health for p in s.team1])
    r2 = Kr + sum([max(0, p.health) / p.max_health for p in s.team2])
    return r1, r2


def update_ser(s, is_terminal, **kwargs):
    if s is None:
        return
    if is_terminal:
        r1, r2 = get_reward(s)
    if not is_terminal:
        r1, r2 = kwargs['rewards']
    s.ser[0][s.chosen_actions[0]] += (r1/r2) / s.probs[0][s.chosen_actions[0]]
    s.ser[1][s.chosen_actions[1]] += (r2/r1) / s.probs[1][s.chosen_actions[1]]
    update_ser(s.parent, is_terminal=False, rewards=(r1, r2))


def uct_gsa(s0, max_it):
    it = 1
    while it < max_it:
        it += 1
        s = s0
        while not(s.ended()):
            p0, p1 = get_p(s)
            a0 = choice(s.actions[0], 1, p=p0)
            a1 = choice(s.actions[1], 1, p=p1)
            s.probs = [p0, p1]
            s.chosen_actions = [s.actions[0].index(a0), s.actions[1].index(a1)]
            s1 = s.step([a0[0], a1[0]])
            s = s1
        update_ser(s, is_terminal=True)


if __name__ == "__main__":
    scyther = Pokemon(name="Scyther", item="Eviolite", evs={'atk': 252, 'spe': 252}, nature="Jolly",
                      trait="Technician", moves=["Bug Bite", "Aerial Ace", "Brick Break", "Swords Dance"])
    gengar = Pokemon(name="Gengar", item="Black Sludge", evs={'spa': 252, 'spe': 252}, nature="Timid",
                     trait="Levitate", moves=["Shadow Ball", "Focus Blast", "Sludge Bomb", "Substitute"])
    G = GameStatus([scyther], [gengar], 0, 0)
    uct_gsa(G, 100)
