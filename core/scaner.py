# scaner.py
import os

class Scanner(object):
    """Class for Scanner. Creates tokens."""
    message = ""
    index = 0
    types = {"number": 0, "keyword": 1, "other": 2}
    keywords = ["Andelka", "add", "remove", "xp", "show", "top", "current"]

    def __init__(self):
        pass

    def new_message(self, arg):
        self.message = arg
        self.index = 0

    def get_token(self):
        if (self.index) >= len(self.message):
            return None

        submessage = ""
        type = self.types["number"]
        index = self.index
        while index < len(self.message):
            # delete more spaces than it should be
            if submessage == "" and self.message[index].isspace():
                index += 1
                continue

            # space - separator?
            if self.message[index].isspace():
                # numbers
                if type == self.types["number"]:
                    self.index = index + 1
                    return [self.types["number"], submessage]

                # keyword?
                if submessage in self.keywords:
                    self.index = index + 1
                    return [self.types["keyword"], submessage]

                # else - insert symbol into submessage

            submessage += self.message[index]
            index += 1
            if type == self.types["number"]:
                try:
                    number = int(submessage)
                except ValueError:
                    try:
                        number = float(submessage)
                    except:
                        type = self.types["other"] # keyword or something else
                except:
                    # not number anymore
                    type = self.types["other"] # keyword or something else

        self.index = len(self.message)
        # end of message
        if type == self.types["number"]:
            return [self.types["number"], submessage]

        if submessage in self.keywords:
            return [self.types["keyword"], submessage]

        return [self.types["other"], submessage]
