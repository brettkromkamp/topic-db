"""
Scope class. Part of the Contextualise (https://contextualise.dev) project.

April 16, 2024
Brett Alistair Kromkamp (brettkromkamp@gmail.com)
"""

import uuid
from slugify import slugify

UNIVERSAL_SCOPE = "*"


class Scope:
    def __init__(self, topic_identifier) -> None:
        self.__identifier = str(uuid.uuid4())
        self.topic_identifier = (
            topic_identifier if topic_identifier == UNIVERSAL_SCOPE else slugify(str(topic_identifier))
        )

    @property
    def identifier(self) -> str:
        return self.__identifier
