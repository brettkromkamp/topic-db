"""
OntologyMode enumeration. Part of the Contextualise (https://contextualise.dev) project.

December 28, 2016
Brett Alistair Kromkamp (brettkromkamp@gmail.com)
"""

from enum import Enum


class OntologyMode(Enum):
    STRICT = 1
    LENIENT = 2

    def __str__(self):
        return self.name
