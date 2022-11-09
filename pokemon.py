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

import numpy as np
import json
import random
from subprocess import check_output
import utils


class Node:
    """A node in the game's tree.

    Attributes
    ----------
    name : str
        first name of the person
    surname : str
        family name of the person
    age : int
        age of the person

    Methods
    -------
    info(additional=""):
        Prints the person's name and age.
    """

    def __init__(self, uuid, state, print=False):

        self.uuid = uuid
        self.state = state
        self.sides = self.state['sides']
        self.healths = []
        self.chosen_actions = None
        self.actions_count = [[0]*len(self.actions[0]), [0]*len(self.actions[1])]
        self.probs = None
        self.parent = None
        self.children = []
        self.level = 0

        self.ser = [
            np.array([0]*len(self.actions[0]), dtype=float),
            np.array([0]*len(self.actions[1]), dtype=float)
        ]  # sum of expected rewards

        if print:
            self.print_teams()

    def print_teams(self):
        print('-----TEAMS STATE-----\n')
        for team_id, team in enumerate(self.teams):
            print(team_id)
            for pokemon in team:
                species = pokemon["speciesData"]["id"]
                print(species, end=' ')
                print(' '*(15-len(species)), end='')
                health_ratio = pokemon["hp"] / pokemon["maxhp"]
                self.healths.append(round(health_ratio*10))
                for i in range(round(health_ratio*10)):
                    print('■', end='')
                print()
            print('\n')

    def ended(self):
        return self.state['ended']

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

    def write_state(self):
        with open("{}.txt".format(self.uuid), "w") as f:
            f.write(json.dumps(self.state))

    def get_child(self, moves):
        for c in self.children:
            if c.parent_actions == moves:
                return c
        return None

    @property
    def actions(self):
        """For each player, retrieve the actions that can be selected."""
        actions = [[], []]
        if len(self.need_replacement) == 1:
            actions = [[-1], [-1]]
            p = self.need_replacement[0]
            actions[p] = self.available[p]
        elif len(self.need_replacement) == 2:
            for p in range(2):
                actions[p] = self.available[p]
        else:
            for i in range(2):
                if 'mustrecharge' in self.volatiles[i] or 'twoturnmove' in self.volatiles[i]:
                    actions[i].append('m0')
                else:
                    actions[i].extend(['m{}'.format(j) for j, m in enumerate(self.move_slots[i]) if not m['disabled']])
                    actions[i].extend(self.available[i])
            # TODO: check possible switches
        return actions

    @property
    def volatiles(self):
        """Get volatile conditions for each active pokemon"""
        v1 = self.sides[0]['pokemon'][self.active[0]]['volatiles']
        v2 = self.sides[1]['pokemon'][self.active[1]]['volatiles']
        return [v1, v2]

    @property
    def active(self):
        """For each team, retrieve the indices of the active pokemon."""
        active1 = [it for it, pokemon in enumerate(self.teams[0]) if pokemon['isActive']][0]
        active2 = [it for it, pokemon in enumerate(self.teams[1]) if pokemon['isActive']][0]
        return [active1, active2]

    @property
    def move_slots(self):
        """For each team, retrieve the active pokemon move slots."""
        ms1 = self.sides[0]['pokemon'][self.active[0]]['moveSlots']
        ms2 = self.sides[1]['pokemon'][self.active[1]]['moveSlots']
        return [ms1, ms2]

    @property
    def teams(self):
        """For each side, retrieve the pokemon team."""
        team1 = self.sides[0]['pokemon']
        team2 = self.sides[1]['pokemon']
        return [team1, team2]

    @property
    def need_replacement(self): # TODO: check if PS changes order of team members (each pokemon should always get the same slot)
        need_replacement = []
        for i in range(2):
            if self.sides[i]['faintedThisTurn']:
                need_replacement.append(i)
        return need_replacement

    @property
    def available(self):
        available = []
        for i in range(2):
            available.append(['s{}'.format(it) for it, pokemon in enumerate(self.teams[i]) if pokemon['hp'] > 0
                              and not pokemon['isActive']])
        return available
