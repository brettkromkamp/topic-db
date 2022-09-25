"""
CollaborationMode enumeration. Part of the Contextualise (https://contextualise.dev) project.
April 04, 2020
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

from enum import Enum


class CollaborationMode(Enum):
    VIEW = 1  # Read-only
    COMMENT = 2
    EDIT = 3  # Read/write

    def __str__(self):
        return self.name
