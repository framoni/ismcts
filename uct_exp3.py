from math import exp
import numpy as np
from numpy.random import choice
from pokemon import Node

from pokemon_showdown import PSBattle

# start assuming all nodes are simultaneous

# use as rewards the ratio between the sum of HP % of mons belonging to the player and the same sum calculated for the
# mons of the opponent


sor_dict = {}

ETA = .2
EPS = .8

Kr = .1


def exp_ser(ser, EPS):
    return np.array([exp(EPS * x) for x in ser])


def get_p(s, ETA, EPS):
    sum_exp_0 = np.sum(exp_ser(s.ser[0], EPS))
    C1 = sum_exp_0 / (1 - len(s.ser[0]) * ETA)  # TODO: handle division by zero cases
    sum_exp_1 = np.sum(exp_ser(s.ser[1], EPS))
    C2 = sum_exp_1 / (1 - len(s.ser[1]) * ETA)
    p1 = ETA + exp_ser(s.ser[0], EPS) / C1
    p2 = ETA + exp_ser(s.ser[1], EPS) / C2
    return p1, p2

# def get_reward(s):
#     r1 = Kr + sum([max(0, p["hp"]) / p["maxhp"] for p in s.teams[0]])
#     r2 = Kr + sum([max(0, p["hp"]) / p["maxhp"] for p in s.teams[1]])
#     return r1 / s.level, r2 / s.level


def get_reward(s):  # TODO: combine healts of both sides in the score
    # r1 = sum([max(0, p["hp"]) / p["maxhp"] for p in s.teams[0]]) / 6 / s.level
    r1 = sum([p["hp"] / p["maxhp"] for p in s.teams[0]]) / len(s.teams[0]) / s.level
    r2 = sum([max(0, p["hp"]) / p["maxhp"] for p in s.teams[1]]) / len(s.teams[1]) / s.level
    return r1, r2


def update_ser(s, is_terminal, **kwargs):
    if s is None:
        return
    if is_terminal:
        r1, r2 = get_reward(s)
    else:
        r1, r2 = kwargs['rewards']
        actions_idx = [s.actions[0].index(s.chosen_actions[0]), s.actions[1].index(s.chosen_actions[1])]
        # s.ser[0][actions_idx[0]] += (r1/r2) / s.probs[0][actions_idx[0]]
        # s.ser[1][actions_idx[1]] += (r2/r1) / s.probs[1][actions_idx[1]]
        s.ser[0][actions_idx[0]] += r1 / s.probs[0][actions_idx[0]]
        s.ser[1][actions_idx[1]] += r2 / s.probs[1][actions_idx[1]]
        # print("Status:", s, "\nser_0: ", dict(zip(s.actions[0], s.ser[0])), "\nser_1: ", dict(zip(s.actions[1], s.ser[1])))
    update_ser(s.parent, is_terminal=False, rewards=(r1, r2))


def uct_gsa(s0, battle, max_it):
    it = 0
    while it < max_it:
        it += 1
        print('Iteration {}'.format(it))
        s = s0
        count = 0
        healths = s.healths
        if it > 1:
            s.write_state()
            battle.unfreeze(s.uuid)
        while not(s.ended()):
            p0, p1 = get_p(s, ETA, EPS)
            a0 = choice(s.actions[0], 1, p=p0)[0]
            a1 = choice(s.actions[1], 1, p=p1)[0]
            s.probs = [p0, p1]
            s.chosen_actions = [a0, a1]
            s.actions_count[0][s.actions[0].index(a0)] += 1
            s.actions_count[1][s.actions[1].index(a1)] += 1
            if s == s0:
                for p in range(2):
                    print("Player:", p, "\nCounts: ", dict(zip(s.actions[p], s0.actions_count[p])))
                    print("Status:", p, "\nProbs: ", dict(zip(s.actions[p], s0.probs[p])))
            battle.step([a0, a1])
            s1 = s.get_child(s.chosen_actions)
            if s1 is None:
                s1 = Node(battle.uuid, battle.state)
                s1.parent_actions = s.chosen_actions
                s1.level = s.level + 1
                s1.parent = s
                s.children.append(s1)
            if s1.healths == healths:
                count += 1
                if count == 10:
                    pass
            healths = s1.healths
            s = s1
        update_ser(s, is_terminal=True)
        print("\nser_0: ", dict(zip(s0.actions[0], s0.ser[0])), "\nser_1: ",
              dict(zip(s0.actions[1], s0.ser[1])))
    return s0.actions[0][s0.actions_count[0].index(max(s0.actions_count[0]))]


if __name__ == "__main__":

    battle = PSBattle(log=True)
    battle.root_uuid = battle.uuid
    node = Node(battle.uuid, battle.state)
    node.level = 0
    uct_gsa(node, battle, 10)
