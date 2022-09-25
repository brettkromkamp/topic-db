"""
TopicDbError class. Part of the Contextualise (https://contextualise.dev) project.

June 15, 2016
Brett Alistair Kromkamp (brettkromkamp@gmail.com)
"""


class TopicDbError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
