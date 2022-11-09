"""
At a given time, only part of the enemy team is known. Determinization aims at simulating battles with partial
information by averaging out many simulations where hidden information is determinized with random picks.
"""

"""
for each of N simulations:
    for the totally unknown slots, pick a random set (pick from available sets if format is random battle)
    for the partially known slots, pick a coherent set
    for the totally known slots, no determinization is needed
average the result of the simulations and output a move
"""

