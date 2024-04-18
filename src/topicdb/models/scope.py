"""
Scope class. Part of the Contextualise (https://contextualise.dev) project.

April 16, 2024
Brett Alistair Kromkamp (brettkromkamp@gmail.com)
"""

import uuid
from slugify import slugify

from topicdb.topicdberror import TopicDbError

UNIVERSAL_SCOPE = "*"


class Scope:
    def __init__(self, topic_identifier: str, entity_identifier: str) -> None:
        self.__identifier = str(uuid.uuid4())
        self.topic_identifier = (
            topic_identifier if topic_identifier == UNIVERSAL_SCOPE else slugify(str(topic_identifier))
        )
        self.__entity_identifier = (
            entity_identifier if entity_identifier == UNIVERSAL_SCOPE else slugify(str(entity_identifier))
        )

    @property
    def entity_identifier(self) -> str:
        return self.__entity_identifier

    @entity_identifier.setter
    def entity_identifier(self, value: str) -> None:
        if value == "":
            raise TopicDbError("Empty 'entity identifier' parameter")
        self.__entity_identifier = value if value == UNIVERSAL_SCOPE else slugify(str(value))

    @property
    def identifier(self) -> str:
        return self.__identifier
