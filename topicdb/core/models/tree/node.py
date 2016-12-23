"""
Node class. Part of the StoryTechnologies Builder project.

July 02, 2016
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

from topicdb.core.models.topic import Topic


class Node:
    # Based on this implementation: http://www.quesucede.com/page/show/id/python-3-tree-implementation

    def __init__(self, identifier, parent=None, topic=None):
        self.__identifier = identifier

        self.parent = parent

        self.__topic = topic
        self.__children = []

    @property
    def identifier(self):
        return self.__identifier

    @property
    def topic(self):
        return self.__topic

    @topic.setter
    def topic(self, value):
        if isinstance(value, Topic):
            self.__topic = value

    @property
    def children(self):
        return self.__children

    def add_child(self, identifier):
        self.__children.append(identifier)
