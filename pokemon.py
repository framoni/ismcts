"""

Tools for setupping simulations of the game of Pokémon

Format and rules:

Start by considering Smogon Gen X OU tier with its standard clauses

[link to reference page]

Start with computing the initial information set IS_0:
    * assume each team member belongs to the Smogon Gen X OU tier
    * for each pokémon, create a list of the most likely sets, taken from Smogon usage statistics

"""

import numpy as np


class Pokemon():

    def __init__(self, moves):
        self.health = 1
        self.status = []
        self.moves = moves


class GameStatus():

    def __init__(self, team1, team2, current1, current2):
        self.hazards = {"sr": 0, "spikes": 0, "tspikes": 0}
        self.weather = None
        self.terrain = None
        self.team1 = team1
        self.team2 = team2
        self.current1 = current1
        self.current2 = current2

        self.actions = self.get_actions()
        self.sor = [
            np.array([0]*len(self.actions[0])),
            np.array([0]*len(self.actions[1]))
        ]  # sum of expected rewards


    def ended(self):
        if any([p.health > 0 for p in self.team1]) and any([p.health > 0 for p in self.team2]):
            return False
        return True

    def get_actions(self):
        a1 = self.current1.moves
        a2 = self.current2.moves
        return [a1, a2]
