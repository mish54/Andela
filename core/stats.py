# stats.py
import os

class Stats(object):
    """Class holding info about atats in Ava raids."""

    roles = {
        "Newby": 0,
        "Raider": 10,
        "Middle Class Raider": 50,
        "Experienced Raider": 100,
        "Elite Raider": 200
    }
    players = {
#        "A": 500,
#        "B": 2,
#        "C": 300
    }

    def __init__(self):
        pass

    def add_xp_to_player(self, player, value):
        if player in self.players.keys():
            self.players[player] += value
        else:
            self.players[player] = value
        return [player, self.players[player]]

    def add_role(self, role, value):
        if role in self.roles.keys():
            return false
        else:
            self.roles[role] = value
            return true

    def remove_role(self, role):
        if role not in self.roles.keys():
            return false
        else:
            self.roles.pop(role)
            return true

    def change_role_limit(self, role, value):
        if role not in self.roles.keys():
            return false
        else:
            self.roles[role] = value
            return true

    def get_player(self, name):
        if name not in self.players.keys():
            return None
        else:
            return [self.players[name], self.index_player_toplist(name)]

    def get_roles(self):
        return self.roles.copy()

    def index_player_toplist(self, name):
        toplist = self.toplist()
        for i in range(len(self.players)):
            if toplist[i][0] == name:
                return i+1
        else:
            return -1

    def toplist(self):
        return sorted(stat.players.items(), key=lambda x: x[1], reverse=True)
