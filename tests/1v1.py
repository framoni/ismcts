import json
from pokemon_showdown import PSBattle
from pokemon import Node
from uct_exp3 import uct_exp3

team1 = json.dumps(
    [
        {
            "name": "Squirtle",
            "species": "Wartortle",
            "moves": [
                "bubblebeam",
                "tailwhip",
                "bodyslam",
                "toxic"
            ],
            "ability": "None",
            "evs": {
                "hp": 255,
                "atk": 255,
                "def": 255,
                "spa": 255,
                "spd": 255,
                "spe": 255
            },
            "ivs": {
                "hp": 30,
                "atk": 30,
                "def": 30,
                "spa": 30,
                "spd": 30,
                "spe": 30
            },
            "item": "",
            "level": 100,
            "shiny": False,
            "gender": False
        }
    ]
)

team2 = json.dumps(
    [
        {
            "name": "Bulbasaur",
            "species": "Bulbasaur",
            "moves": [
                "razorleaf",
                "bodyslam",
                "sleeppowder",
                "growth"
            ],
            "ability": "None",
            "evs": {
                "hp": 255,
                "atk": 255,
                "def": 255,
                "spa": 255,
                "spd": 255,
                "spe": 255
            },
            "ivs": {
                "hp": 30,
                "atk": 30,
                "def": 30,
                "spa": 30,
                "spd": 30,
                "spe": 30
            },
            "item": "",
            "level": 100,
            "shiny": False,
            "gender": False
        }
    ]
)

if __name__ == "__main__":
    battle = PSBattle(log=False, teams=[team1, team2], debug=False)
    battle.root_uuid = battle.uuid
    node = Node(battle.uuid, battle.state)
    node.level = 0
    uct_exp3(node, battle, 100)
