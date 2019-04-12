"""
Node class. Part of the StoryTechnologies project.

July 02, 2016
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""
from typing import Optional, List

from topicdb.core.models.topic import Topic


class Node:
    # Based on this implementation: http://www.quesucede.com/page/show/id/python-3-tree-implementation

    def __init__(self, identifier: str, parent: Optional[str] = None, topic: Optional[Topic] = None) -> None:
        self.__identifier = identifier

        self.parent = parent

        self.__topic = topic
        self.__children: List[str] = []

    @property
    def identifier(self) -> str:
        return self.__identifier

    @property
    def topic(self) -> Optional[Topic]:
        return self.__topic

    @topic.setter
    def topic(self, value: Topic) -> None:
        if isinstance(value, Topic):
            self.__topic = value

    @property
    def children(self) -> List[str]:
        return self.__children

    def add_child(self, identifier: str) -> None:
        self.__children.append(identifier)
