"""
RetrievalOption enumeration. Part of the StoryTechnologies project.

July 03, 2016
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

from enum import Enum


class RetrievalOption(Enum):
    RESOLVE_ATTRIBUTES = 1
    DONT_RESOLVE_ATTRIBUTES = 2
    RESOLVE_OCCURRENCES = 3
    DONT_RESOLVE_OCCURRENCES = 4
    INLINE_RESOURCE_DATA = 5
    DONT_INLINE_RESOURCE_DATA = 6
