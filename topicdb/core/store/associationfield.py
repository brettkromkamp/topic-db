"""
AssociationField enumeration. Part of the StoryTechnologies Builder project.

July 02, 2016
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

from enum import Enum


class AssociationField(Enum):
    INSTANCE_OF = 0
    ROLE_SPEC = 1
    TOPIC_REF = 2
