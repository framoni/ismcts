from math import exp
import numpy as np
from numpy.random import choice
from pokemon import Node

from pokemon_showdown import RandomBattle

# start assuming all nodes are simultaneous

# use as rewards the ratio between the sum of HP % of mons belonging to the player and the same sum calculated for the
# mons of the opponent


sor_dict = {}

ETA = .2
EPS = .1

Kr = .1


def exp_ser(ser):
    return np.array([exp(EPS * x) for x in ser])


def get_p(s):
    sum_exp_0 = np.sum(exp_ser(s.ser[0]))
    C1 = sum_exp_0 / (1 - len(s.actions[0]) * ETA)  # TODO: handle division by zero cases
    sum_exp_1 = np.sum(exp_ser(s.ser[1]))
    C2 = sum_exp_1 / (1 - len(s.actions[1]) * ETA)
    p1 = ETA + exp_ser(s.ser[0]) / C1
    p2 = ETA + exp_ser(s.ser[1]) / C2
    return p1, p2
 

def get_reward(s):
    r1 = Kr + sum([max(0, p.health) / p.max_health for p in s.team1])
    r2 = Kr + sum([max(0, p.health) / p.max_health for p in s.team2])
    return r1 / s.level, r2 / s.level


def update_ser(s, is_terminal, **kwargs):
    if s is None:
        return
    if is_terminal:
        r1, r2 = get_reward(s)
    if not is_terminal:
        r1, r2 = kwargs['rewards']
    s.ser[0][s.chosen_actions[0]] += (r1/r2) / s.probs[0][s.chosen_actions[0]]
    s.ser[1][s.chosen_actions[1]] += (r2/r1) / s.probs[1][s.chosen_actions[1]]
    print("Status:", s, "\nser_0: ", dict(zip(s.actions[0], s.ser[0])), "\nser_1: ", dict(zip(s.actions[1], s.ser[1])))
    update_ser(s.parent, is_terminal=False, rewards=(r1, r2))


def uct_gsa(s0, max_it):
    it = 1
    while it < max_it:
        it += 1
        s = s0
        count = 0
        healths = s.healths
        while not(s.ended()):
            p0, p1 = get_p(s)
            a0 = choice(s.actions[0], 1, p=p0)[0]
            a1 = choice(s.actions[1], 1, p=p1)[0]
            s.probs = [p0, p1]
            # s.chosen_actions = [s.actions[0].index(a0), s.actions[1].index(a1)]
            s.chosen_actions = [a0, a1]
            # s.actions_count[0][s.chosen_actions[0]] += 1
            # s.actions_count[1][s.chosen_actions[1]] += 1
            s.actions_count[0][s.actions[0].index(a0)] += 1
            s.actions_count[1][s.actions[1].index(a1)] += 1
            if s == s0:
                print("Status:", s, "\nCount: ", dict(zip(s.actions[0], s0.actions_count[0])))
                print("Status:", s, "\nProbs 0: ", dict(zip(s.actions[0], s0.probs[0])))
            battle.step([a0, a1])
            s1 = Node(battle.uuid, battle.state)
            if s1.healths == healths:
                count += 1
                healths = s1.healths
                if count == 10:
                    raise Exception('Simulation is stuck')
            # s1 = s.step([a0, a1])
            s = s1
        update_ser(s, is_terminal=True)
    return s0.actions[0][s0.actions_count[0].index(max(s0.actions_count[0]))]


if __name__ == "__main__":

    battle = RandomBattle(log=True)

    # scyther = Pokemon(name="Scyther", item="Eviolite", evs={'atk': 252, 'spe': 252}, nature="Jolly",
    #                   trait="Technician", moves=["Bug Bite", "Aerial Ace", "Brick Break", "Swords Dance"])
    # gengar = Pokemon(name="Gengar", item="Black Sludge", evs={'spa': 252, 'spe': 252}, nature="Timid",
    #                  trait="Levitate", moves=["Shadow Ball", "Focus Blast", "Sludge Bomb", "Substitute"])
    # G = GameStatus([scyther], [gengar], 0, 0)
    node = Node(battle.uuid, battle.state)
    node.level = 0
    uct_gsa(node, 100)

    B = RandomBattle()
    uct_gsa(B, 100)

    # implement debug mode
