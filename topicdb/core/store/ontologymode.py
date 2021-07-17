"""
OntologyMode enumeration. Part of the StoryTechnologies project.

December 28, 2016
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

from enum import Enum


class OntologyMode(Enum):
    STRICT = 1
    LENIENT = 2

    def __str__(self):
        return self.name
