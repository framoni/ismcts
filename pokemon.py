"""

Tools for setupping simulations of the game of Pokémon

Format and rules:

Start by considering Smogon Gen X OU tier with its standard clauses

[link to reference page]

Start with computing the initial information set IS_0:
    * assume each team member belongs to the Smogon Gen X OU tier
    * for each pokémon, create a list of the most likely sets, taken from Smogon usage statistics:
      https://www.smogon.com/stats/2020-10-DLC2/moveset/

"""

import copy
import numpy as np
import json
import random
from subprocess import check_output
import utils


class Node:

    def __init__(self, state):

        self.state = json.loads(state)
        self.sides = self.state['sides']

        self.chosen_actions = None
        self.actions_count = [[0]*len(self.actions[0]), [0]*len(self.actions[1])]
        self.probs = None
        self.parent = None
        self.level = 0

        self.ser = [
            np.array([0]*len(self.actions[0]), dtype=float),
            np.array([0]*len(self.actions[1]), dtype=float)
        ]  # sum of expected rewards

    def ended(self):
        if any([p.health == None for p in self.team1 + self.team2]):
            return False
        if any([p.health > 0 for p in self.team1]) and any([p.health > 0 for p in self.team2]):
            return False
        return True

    def turn(self):
        # decide who starts first
        self.team1[self.current1].speed

    def calc_damage(self, action, p1, p2, c):
        p1 = self.team1[self.current1]
        p2 = self.team2[self.current2]
        content = utils.js_string.format(self.gen, p1.name, p1.item, p1.nature,
                                         json.dumps(p1.evs).replace('"', ''), json.dumps(p1.boosts).replace('"', ''),
                                         p2.name, p2.item, p2.nature,
                                         json.dumps(p2.evs).replace('"', ''), json.dumps(p2.boosts).replace('"', ''),
                                         action)
        with open("calc.mjs", "w") as f:
            f.write(content)
        out = json.loads(check_output(["node", "calc.mjs"]))
        damage = random.choice(out["damage"]) if type(out["damage"]) == list else out["damage"]  # this should be a random node
        if c.health == None:
            c.health = out['defender']['originalCurHP']
            c.max_health = c.health
        old_health = c.health
        c.health -= damage
        print("{} health {} --> {}".format(c.name, old_health, c.health))

    def step(self, actions):
        child = copy.deepcopy(self)
        child.parent = self
        child.level = self.level + 1
        self.calc_damage(actions[0], self.team1[self.current1], self.team2[self.current2], child.team2[child.current2])
        self.calc_damage(actions[1], self.team2[self.current2], self.team1[self.current1], child.team1[child.current1])
        # calculate both damages, modify pokemon stats, return new status
        return child

    @property
    def actions(self):
        """For each active pokemon, retrieve the indices of moves that can be selected."""
        actions = []
        for i in range(2):
            actions.append([j for j, m in enumerate(self.move_slots[i]) if not m['disabled']])
        return actions

    @property
    def active(self):
        """For each team, retrieve the indices of the active pokemon."""
        active1 = self.sides[0]['active']
        active2 = self.sides[1]['active']
        return [active1, active2]

    @property
    def move_slots(self):
        """For each team, retrieve the active pokemon move slots."""
        ms1 = self.sides[0]['pokemon'][self.active[0]]['moveSlots']
        ms2 = self.sides[1]['pokemon'][self.active[1]]['moveSlots']
        return [ms1, ms2]
