"""
AssociationField enumeration. Part of the StoryTechnologies Builder project.

July 02, 2016
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

from enum import Enum


class AssociationField(Enum):
    instance_of = 0
    role_spec = 1
    topic_ref = 2
