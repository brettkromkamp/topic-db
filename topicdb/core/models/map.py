"""
TopicMap class. Part of the Contextualise (https://contextualise.dev) project.

January 07, 2016
Brett Alistair Kromkamp (brettkromkamp@gmail.com)
"""

from datetime import datetime


class Map:
    def __init__(self, name: str, description: str = "") -> None:
        self.name = name
        self.description = description
        self.creation_datetime = datetime.utcnow().replace(microsecond=0).isoformat()
        self.modification_datetime = None
