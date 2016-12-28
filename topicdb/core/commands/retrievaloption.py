"""
RetrievalOption enumeration. Part of the StoryTechnologies project.

July 03, 2016
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

from enum import Enum


class RetrievalOption(Enum):
    resolve_attributes = 1
    dont_resolve_attributes = 2
    resolve_occurrences = 3
    dont_resolve_occurrences = 4
    inline_resource_data = 5
    dont_inline_resource_data = 6
