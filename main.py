"""

ISMCTS

Code notation:

[s0]∼1 --> IS_0 (information set for state 0 and player 1)

"""

from math import sqrt, log
import random

det_vec = []  # stores all the determinizations


class Node:

    def __init__(self, data):
        self.actions = None
        self.children = None
        self.incoming_action = None
        self.n = 0
        self.n_1 = 0
        self.r = 0
        self.data = data

    def get_siblings(self):
        return

    def add_child(self, a):
        self.actions.append(a)
        v = self.get_states_from_actions(a)
        self.children.append(v)
        return v

    def print_tree(self):
        print(self.data)


def get_actions(d):
    """ get the set of available actions from a state """
    # compute possible actions depending on the game...
    A = []
    return A


def get_actions_from_IS():
    """ get the set of available actions from a state """


def get_states_from_actions(s, A):
    """ compute the set of possible states given an action """
    return A


def get_state_from_action(d, a):
    """ compute the next state of a determinization given an action """
    return d


def get_U(V, A_d):
    """ compute the set of states in S_d not belonging to children of V """
    return [a for a in A_d if a not in V.actions]


def get_utility(d):
    """ compute the utility for a terminal state """
    return 0


def select(V, d, k):
    A_d = get_actions(d)
    U = get_U(V, A_d)
    while len(A_d) > 0 and len(U) == 0:
        # children of V compatible with the determinization
        d_states = []
        C = []
        for c in V.children:
            if c.incoming_action in A_d:
                C.append(c)
        obj = [c.r / c.n + k * sqrt(log(c.n_1 / c.n)) for c in C]
        v = C[obj.index(max(obj))]
        d = get_state_from_action(d, c.incoming_action)
    return V, d


def expand(V, d):
    A_d = get_actions(d)
    # S_d = get_states_from_actions(d, A_d)
    U = get_U(V, A_d)
    a = random.choice(U)
    v = V.add_child(a)
    return v, get_state_from_action(d, a)


def simulate(d):
    A_d = get_actions(d)
    while len(A_d) > 0:
        a = random.choice(A_d)
        d = get_state_from_action(d, a)
        A_d = get_actions(d)
    return get_utility(d)


def backpropagate(r, V, det_vec):
    V.n += 1
    V.r += r
    for S in V.get_siblings():
        if det_vec[-1] in S:
            S.n_1 += 1
    backpropagate(r, V.parent, det_vec[:-1])


def ismcts(IS_0, n, k):
    V0 = Node(IS_0)
    for it in range(n):
        d0 = random.choice(IS_0)
        det_vec.append(d0)
        (V, d) = select(V0, d0, k)
        det_vec.append(d)
        A_d = get_actions(d)
        U = get_U(V, A_d)
        if len(U) > 0:
            V, d = expand(V, d)
            det_vec.append(d)
        r = simulate(d)
        backpropagate(r, V, det_vec)
        det_vec = []


if __name__ == '__main__':
    print()
