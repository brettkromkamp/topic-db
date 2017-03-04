"""
TopicStoreException class. Part of the StoryTechnologies project.

June 15, 2016
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""


class TopicStoreError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
