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
            return "Hello, what do you need? Please, use prepaired syntax for commands."
        if self.token[0] is not "keyword": # syntax error
            return "I cannot read your command. Please, use prepaired syntax for commands."

        if self.token[1] is "show":
            return self.show_command()

        if self.token[1] is "add":
            return self.add_command(pozitive=True)

        if self.token[1] is "remove":
            return self.add_command(pozitive=False)

        else: # syntax error
            return "I cannot read your command. Please, use prepaired syntax for commands."

    def show_command(self):
        self.token = scaner.get_token()
        if self.token is None:
            return "Hello, what do you need to show? Please, use prepaired syntax for commands."
        if self.token[0] is not "keyword": # syntax error
            return "I cannot read your command. Please, use prepaired syntax for commands."

        if self.token[1] is "current":
            self.token = scaner.get_token()
            if self.token is None or self.token[0] is not "keyword":
                return "I cannot read your command. Please, use prepaired syntax for commands."

            if self.token[1] is "xp":
                self.token = scaner.get_token()
                if self.token is None or self.token[0] is not "other":
                    return "I cannot read your command. Please, use prepaired syntax for commands."

                player_stat = stat.get_player(self.token[1])
                if player_stat is None:
                    return "Unknown player. Be avare to use point in float numbers like '0.5', not '0,5'."

                output = self.token[1] + "\n" + \
                        "Current XP = " + player_stat[0] + "\n" + \
                        "Current position in the highscore = " + player_stat[1]
                return output
            else:
                return "I cannot read your command. Please, use prepaired syntax for commands."

        elif self.token[1] is "top":
            return toplist()

    def toplist(self): #TODO
        self.token = scaner.get_token()
        if self.token is None or self.token[0] is not "number":
            return "I cannot read your command. Please, use prepaired syntax for commands. Expected a number after 'top'."

        count = None
        try:
            count = int(self.token[1])
        except:
            return "Expected integer. Please, use prepaired syntax for commands."

        self.token = scaner.get_token()
        if self.token is None or self.token[1] is not "xp":
            return "I expected 'xp'. Please, use prepaired syntax for commands."

        sorted = self.stats.toplist()

        self.token = scaner.get_token()
        if self.token is not None and self.token[0] is "other":
            role = get(guild.roles, name = self.token[1])
            if role is None:
                return "Unknown role."
            for player in guild.members:
                if role not in player.roles:
                    sorted = [i for i in in_tup if i[0] >= 50]
                    sorted.remove(player.id)



            pass #TODO filtr pro role

        if len(sorted) > count:
            sorted = sorted[0:count]
        output = "Toplist:\n"
        for i in sorted:
            output += i[0] + " -> " + i[1] + "\n"
        return output

    def add_command(self, pozitive=True):
        self.token = scaner.get_token()
        if self.token is None:
            return "Hello, what do you need to add or remove? Please, use prepaired syntax for commands."
        if self.token[0] is not "keyword": # syntax error
            return "I cannot read your command. Please, use prepaired syntax for commands."

        if self.token[1] is "xp":
            return add_xp(pozitive)
        if self.token[1] is "role":
            return add_role(pozitive)
        else:
            return "I cannot read your command. Please, use prepaired syntax for commands."

    def add_xp(self, pozitive=True):
        self.token = scaner.get_token()
        if self.token is None or self.token[0] is not "number":
            return "I cannot read your command. Please, use prepaired syntax for commands. Expected a number after 'xp'."
        value = float(self.token[1])
        if pozitive is False:
            value = -value

        self.token = scaner.get_token()
        if self.token is None or self.token[0] is not "other":
            return "I cannot read your command. Please, use prepaired syntax for commands. Expected a name of player, role or voice room."

        if "@" in self.token[1]:
            # player or role - TODO role
            output = self.stat.add_xp_to_player(self, self.token[1], value)
            # TODO role change
            return output
        else:
            pass # voice room

        pass

    def add_role(self, pozitive=True):
        pass
