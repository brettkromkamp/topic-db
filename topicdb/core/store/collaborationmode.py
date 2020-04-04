"""
CollaborationMode enumeration. Part of the StoryTechnologies project.

April 04, 2020
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

from enum import Enum


class CollaborationMode(Enum):
    CAN_VIEW = 1  # Read-only
    CAN_COMMENT = 2
    CAN_EDIT = 3  # Read/write

    def __str__(self):
        return self.name
