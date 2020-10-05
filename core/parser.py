# parser.py
import os
import discord
from .stats import Stats
from .scaner import Scanner

class Parser(object):
    """Class for Parser, that will parse and interpret commands."""
    guild = None
    stat = Stats()
    scaner = Scanner()
    message = None
    token = None
    admin_roles = []
    leader_roles = []

    def __init__(self, guild):
        self.guild = guild

        for role in self.guild.roles:
            if "admin" in role.name or "Admin" in role.name:
                self.admin_roles.append(role)
            if "moderator" in role.name or "Moderator" in role.name:
                self.admin_roles.append(role)
            if "leader" in role.name or "Leader" in role.name:
                self.leader_roles.append(role)

    def parse(self, message):
        self.scaner.new_message(message.content)
        print("MESSAGE:" + message.content)
        self.message = message

        self.token = self.scaner.get_token()
        if self.token is None:
            print("Begins with None.")
            return None
        if not (self.token[0] == self.scaner.types["keyword"] and self.token[1] == "Andelka"):
            print("Begins with nothing for me.")
            print("|" + str(self.token[0]) + "," + self.token[1] + "|")
            return None

        print("Begins with Andelka.")
        self.token = self.scaner.get_token()
        if self.token is None:
            return "Hello, what do you need? Please, use prepared syntax for commands."
        if self.token[0] != self.scaner.types["keyword"]: # syntax error
            return "I cannot read your command. Please, use prepared syntax for commands."

        if self.token[1] == "show":
            return self.show_command()

        if self.token[1] == "add":
            return self.add_command(pozitive=True)

        if self.token[1] == "remove":
            return self.add_command(pozitive=False)

        else: # syntax error
            return "I cannot read your command. Please, use prepared syntax for commands."

    def show_command(self):
        self.token = self.scaner.get_token()
        if self.token is None:
            return "Hello, what do you need to show? Please, use prepared syntax for commands."
        if self.token[0] != self.scaner.types["keyword"]: # syntax error
            return "I cannot read your command. Please, use prepared syntax for commands."

        if self.token[1] == "current":
            self.token = self.scaner.get_token()
            if self.token is None or self.token[0] != self.scaner.types["keyword"]:
                return "I cannot read your command. Please, use prepared syntax for commands."

            if self.token[1] == "xp":
                self.token = self.scaner.get_token()
                if self.token is None or self.token[0] != self.scaner.types["other"]:
                    return "I cannot read your command. Please, use prepared syntax for commands."

                player_stat = self.stat.get_player(self.token[1])
                if player_stat is None:
                    return "Unknown player. Be avare to use point in float numbers like '0.5', not '0,5'."

                output = self.token[1] + "\n" + \
                        "Current XP = " + player_stat[0] + "\n" + \
                        "Current position in the highscore = " + player_stat[1]
                return output
            else:
                return "I cannot read your command. Please, use prepared syntax for commands."

        elif self.token[1] == "top":
            return self.toplist()

    def toplist(self):
        self.token = self.scaner.get_token()
        if self.token is None:
            return "I cannot read your command. Please, use prepared syntax for commands. Expected a number after 'top'.1"
        elif self.token[0] != self.scaner.types["number"]:
            print(self.token)
            print("Ma byt:")
            print(self.scaner.types["number"])
            return "I cannot read your command. Please, use prepared syntax for commands. Expected a number after 'top'.2"

        count = None
        try:
            count = int(self.token[1])
        except:
            return "Expected integer. Please, use prepared syntax for commands."

        self.token = self.scaner.get_token()
        if self.token is None or self.token[1] != "xp":
            return "I expected 'xp'. Please, use prepared syntax for commands."

        sorted = self.stat.toplist()

        # solving a problem with role filter
        self.token = self.scaner.get_token()
        if self.token is not None and self.token[0] == self.scaner.types["other"]:
            role = discord.utils.get(self.guild.roles, name = self.token[1])
            if role is None:
                return "Unknown role."

            filter_list = []
            for player in self.guild.members:
                if role in player.roles:
                    filter_list.append(player.id)
            sorted = [i for i in sorted if i[0] in filter_list]

        if len(sorted) > count:
            sorted = sorted[0:count]
        output = "Toplist:\n"
        for i in sorted:
            player = discord.utils.get(self.guild.members, id = i[0])
            if player is not None:
                output += player.name + " -> " + i[1] + "\n"
            else:
                output += "This player is not there anymore. Hopefully he/she will come back as a kind player. \n"
        return output

    def add_command(self, pozitive=True):
        self.token = self.scaner.get_token()
        if self.token is None:
            return "Hello, what do you need to add or remove? Please, use prepared syntax for commands."
        if self.token[0] != self.scaner.types["keyword"]: # syntax error
            return "I cannot read your command. Please, use prepared syntax for commands."

        intersection_1 = [item for item in self.message.author.roles if item in self.admin_roles]
        intersection_2 = [item for item in self.message.author.roles if item in self.leader_roles]

        if self.token[1] == "xp":
            if ( len(intersection_1)==0 and len(intersection_2)==0 ):
                return "You have no permition to call that command."
            return self.add_xp(pozitive)

        if self.token[1] == "role":
            if ( len(intersection_1)==0 ):
                return "You have no permition to call that command."
            return self.add_role(pozitive)

        else:
            return "I cannot read your command. Please, use prepared syntax for commands."

    def add_xp(self, pozitive=True):
        self.token = self.scaner.get_token()
        if self.token is None or self.token[0] != self.scaner.types["number"]:
            return "I cannot read your command. Please, use prepared syntax for commands. Expected a number after 'xp'."
        value = float(self.token[1])
        if pozitive is False:
            value = -value

        self.token = self.scaner.get_token()
        if self.token is None or self.token[0] != self.scaner.types["other"]:
            return "I cannot read your command. Please, use prepared syntax for commands. Expected a name of player, role or voice room."

        output = ""
        # player
        if self.token[1].startswith("<@!"):
            output = self.add_xp_to_player(self.token[1][3:-1], value)
        elif self.token[1].startswith("<@&"):
            role = discord.utils.get(self.guild.roles, name = self.token[1][3:-1])
            for player in self.guild.members:
                if role in player.roles:
                    output += self.add_xp_to_player(player.id, value) + "\n"
        elif self.token[1].startswith("@"):
            output = "Unknown voice player or role."
        else:
            # voice room
            voice_channel = discord.utils.get(self.guild.voice_channels, name = self.token[1])
            if voice_channel is None:
                output = "Unknown voice room."
            else:
                for player in voice_channel.members:
                    output += self.add_xp_to_player(player.id, value) + "\n"

        return output

    def add_xp_to_player(self, player_id, value):
        output = self.stat.add_xp_to_player(player_id, value)
        self.control_roles_to_player(player_id)
        return output

    def control_roles_to_player(self, player_id, seasonal_reset=False):
        player_stat = self.stat.get_player(player_id)
        if player_stat is None:
            return
        player = discord.utils.get(self.guild.members, id = player_id)
        if player is None:
            return

        roles = self.stat.get_roles()
        roles_to_give = []
        roles_to_remove = []
        for role in roles:
            print("Role:")
            print(role)
            print(role[1])
            if player_stat[0] >= role[1]:
                roles_to_give.append( discord.utils.get(self.guild.roles, name = role) )
            else:
                if role[0] is not "Middle Class Raider":
                    roles_to_remove.append( discord.utils.get(self.guild.roles, name = role) )

        player.remove_roles(roles_to_remove, "Andelka role management")
        player.add_roles(roles_to_remove, "Andelka role management")

    def add_role(self, pozitive=True):
        if positive:
            self.token = self.scaner.get_token()
            if self.token is None or self.token[0] != self.scaner.types["number"]:
                return "I cannot read your command. Please, use prepared syntax for commands. Expected a number."
            value = int(self.token[1])

            self.token = self.scaner.get_token()
            if self.token is None or self.token[0] != self.scaner.types["other"]:
                return "I cannot read your command. Please, use prepared syntax for commands. Expected a name of a role."

            result = self.stat.add_role(self.token[1], value)
            if result == False:
                return "Cannot add role " + self.token[1] + ". This role is already on a list."

            for player in self.guild.members:
                self.control_roles_to_player(player.id)

            return "New role was added."
        else:
            self.token = self.scaner.get_token()
            if self.token is None or self.token[0] != self.scaner.types["other"]:
                return "I cannot read your command. Please, use prepared syntax for commands. Expected a name of a role."

            role = discord.utils.get(self.guild.roles, name = self.token[1])
            if role is None:
                return "Unknown role."

            current_max_xp = self.stat.toplist()[0][1]
            self.stat.change_role_limit(self, role.name, current_max_xp + 100)
            for player in self.guild.members:
                self.control_roles_to_player(self, player.id)

            result = self.stat.remove_role(self.token[1])
            if result == False:
                return "This role cannot be removed by me."

            role.delete()
            return "Role was removed."
