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


class Pokemon:

    def __init__(self, name, item, evs, nature, trait, moves, gen=5):
        self.name = name
        self.health = None
        self.status = {}
        self.boosts = {}
        self.item = item
        self.evs = evs
        self.gen = gen
        self.nature = nature
        self.trait = trait
        self.moves = moves

    # @property
    # def stats(self):
    #     # calculate the pokemon stats
    #     if self.gen < 3:
    #
    #     a1 = self.current1.moves
    #     a2 = self.current2.moves
    #     return [a1, a2]


class GameStatus:

    def __init__(self, team1, team2, current1, current2):
        self.hazards = {"sr": 0, "spikes": 0, "tspikes": 0}
        self.weather = None
        self.terrain = None
        self.team1 = team1
        self.team2 = team2
        self.current1 = current1
        self.current2 = current2
        self.gen = team1[0].gen  # get the gen from the first pokemon of the first team (all are from the same gen)

        self.ser = [
            np.array([0]*len(self.actions[0])),
            np.array([0]*len(self.actions[1]))
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
        old_health = c.health
        c.health -= damage
        print("{} health {} --> {}".format(c.name, old_health, c.health))

    def step(self, actions):
        child = copy.deepcopy(self)
        self.calc_damage(actions[0], self.team1[self.current1], self.team2[self.current2], child.team2[child.current2])
        self.calc_damage(actions[1], self.team2[self.current2], self.team1[self.current1], child.team1[child.current1])
        # calculate both damages, modify pokemon stats, return new status
        return child

    @property
    def actions(self):
        a1 = self.team1[self.current1].moves
        a2 = self.team2[self.current2].moves
        return [a1, a2]
