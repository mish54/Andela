# parser.py
import os
import discord
import core.stats
import core.scaner

class Parser(object):
    """Class for Parser, that will parse and interpret commands."""
    guild = None
    stat = Stats()
    scaner = Scanner()
    message = None
    token = None

    def __init__(self, guild):
        self.guild = guild
        pass

    def parse(self, message):
        scaner.new_message(message.content)
        self.message = message

        self.token = scaner.get_token()
        if self.token is None:
            return None
        if not (self.token[0] is "keyword" and self.token[1] is "Andelka"):
            return None

        self.token = scaner.get_token()
        if self.token is None:
            return "Hello, what do you need? Please, use prepared syntax for commands."
        if self.token[0] is not "keyword": # syntax error
            return "I cannot read your command. Please, use prepared syntax for commands."

        if self.token[1] is "show":
            return self.show_command()

        if self.token[1] is "add":
            return self.add_command(pozitive=True)

        if self.token[1] is "remove":
            return self.add_command(pozitive=False)

        else: # syntax error
            return "I cannot read your command. Please, use prepared syntax for commands."

    def show_command(self):
        self.token = scaner.get_token()
        if self.token is None:
            return "Hello, what do you need to show? Please, use prepared syntax for commands."
        if self.token[0] is not "keyword": # syntax error
            return "I cannot read your command. Please, use prepared syntax for commands."

        if self.token[1] is "current":
            self.token = scaner.get_token()
            if self.token is None or self.token[0] is not "keyword":
                return "I cannot read your command. Please, use prepared syntax for commands."

            if self.token[1] is "xp":
                self.token = scaner.get_token()
                if self.token is None or self.token[0] is not "other":
                    return "I cannot read your command. Please, use prepared syntax for commands."

                player_stat = stat.get_player(self.token[1])
                if player_stat is None:
                    return "Unknown player. Be avare to use point in float numbers like '0.5', not '0,5'."

                output = self.token[1] + "\n" + \
                        "Current XP = " + player_stat[0] + "\n" + \
                        "Current position in the highscore = " + player_stat[1]
                return output
            else:
                return "I cannot read your command. Please, use prepared syntax for commands."

        elif self.token[1] is "top":
            return toplist()

    def toplist(self): #TODO
        self.token = scaner.get_token()
        if self.token is None or self.token[0] is not "number":
            return "I cannot read your command. Please, use prepared syntax for commands. Expected a number after 'top'."

        count = None
        try:
            count = int(self.token[1])
        except:
            return "Expected integer. Please, use prepared syntax for commands."

        self.token = scaner.get_token()
        if self.token is None or self.token[1] is not "xp":
            return "I expected 'xp'. Please, use prepared syntax for commands."

        sorted = self.stats.toplist()

        # solving a problem with role filter
        self.token = scaner.get_token()
        if self.token is not None and self.token[0] is "other":
            role = get(guild.roles, name = self.token[1])
            if role is None:
                return "Unknown role."

            filter_list = []
            for player in guild.members:
                if role in player.roles:
                    filter_list.append(player.id)
            sorted = [i for i in sorted if i[0] in filter_list]

        if len(sorted) > count:
            sorted = sorted[0:count]
        output = "Toplist:\n"
        for i in sorted:
            player = get(guild.members, id = i[0])
            if player is not None:
                output += player.name + " -> " + i[1] + "\n"
            else:
                output += "This player is not there anymore. Hopefully he/she will come back as a kind player. \n"
        return output

    def add_command(self, pozitive=True):
        self.token = scaner.get_token()
        if self.token is None:
            return "Hello, what do you need to add or remove? Please, use prepared syntax for commands."
        if self.token[0] is not "keyword": # syntax error
            return "I cannot read your command. Please, use prepared syntax for commands."

        if self.token[1] is "xp":
            return add_xp(pozitive)
        if self.token[1] is "role":
            return add_role(pozitive)
        else:
            return "I cannot read your command. Please, use prepared syntax for commands."

    def add_xp(self, pozitive=True):
        self.token = scaner.get_token()
        if self.token is None or self.token[0] is not "number":
            return "I cannot read your command. Please, use prepared syntax for commands. Expected a number after 'xp'."
        value = float(self.token[1])
        if pozitive is False:
            value = -value

        self.token = scaner.get_token()
        if self.token is None or self.token[0] is not "other":
            return "I cannot read your command. Please, use prepared syntax for commands. Expected a name of player, role or voice room."

        output = ""
        if self.token[1][0] == "@":
            # player or role
            role = get(guild.roles, name = self.token[1][1:])
            if role is None:
                # player
                output = self.add_xp_to_player(self.token[1], value)
            else:
                # xp for role
                for player in guild.members:
                    if role in player.roles:
                        output += self.add_xp_to_player(player.id, value) + "\n"
        else:
            # voice room
            voice_channel = get(guild.voice_channels, name = self.token[1])
            if voice_channel is None:
                output = "Unknown voice room."
            else:
                for player in voice_channel.members:
                    output += self.add_xp_to_player(player.id, value) + "\n"

        return output

    def add_xp_to_player(self, player_id, value):
        output = self.stat.add_xp_to_player(player_id, value)
        control_roles_to_player(player_id)
        return output

    def control_roles_to_player(self, player_id, seasonal_reset=False):
        player_stat = self.stat.get_player()
        if player_stat is None:
            return
        player = get(guild.members, id = player_id)
        if player is None:
            return

        roles = self.stat.get_roles()
        roles_to_give = []
        roles_to_remove = []
        for role in roles:
            if player_stat[0] >= role[1]:
                roles_to_give.append( get(guild.roles, name = role) )
            else:
                if role[0] is not "Middle Class Raider":
                    roles_to_remove.append( get(guild.roles, name = role) )

        player.remove_roles(roles_to_remove, "Andelka role management")
        player.add_roles(roles_to_remove, "Andelka role management")

    def add_role(self, pozitive=True):
        if positive:
            self.token = scaner.get_token()
            if self.token is None or self.token[0] is not "number":
                return "I cannot read your command. Please, use prepared syntax for commands. Expected a number."
            value = int(self.token[1])

            self.token = scaner.get_token()
            if self.token is None or self.token[0] is not "other":
                return "I cannot read your command. Please, use prepared syntax for commands. Expected a name of a role."

            result = self.stat.add_role(self.token[1], value)
            if result == False:
                return "Cannot add role " + self.token[1] + ". This role is already on a list."

            for player in guild.members:
                control_roles_to_player(player.id)

            return "New role was added."
        else:
            self.token = scaner.get_token()
            if self.token is None or self.token[0] is not "other":
                return "I cannot read your command. Please, use prepared syntax for commands. Expected a name of a role."

            role = get(guild.roles, name = self.token[1])
            if role is None:
                return "Unknown role."

            current_max_xp = self.stat.toplist()[0][1]
            self.stat.change_role_limit(self, role.name, current_max_xp + 100)
            for player in guild.members:
                control_roles_to_player(self, player.id)

            result = self.stat.remove_role(self.token[1])
            if result == False:
                return "This role cannot be removed by me."

            role.delete()
            return "Role was removed."
