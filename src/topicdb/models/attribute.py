"""
Attribute class. Part of the Contextualise (https://contextualise.dev) project.

June 12, 2016
Brett Alistair Kromkamp (brettkromkamp@gmail.com)
"""

import uuid

from slugify import slugify
from topicdb.models.datatype import DataType
from topicdb.models.language import Language
from topicdb.models.scope import Scope
from topicdb.models.scopes import Scopes
from topicdb.topicdberror import TopicDbError

UNIVERSAL_SCOPE = "*"


class Attribute(Scopes):
    def __init__(
        self,
        name: str,
        value: str,
        entity_identifier: str,
        identifier: str = "",
        data_type: DataType = DataType.STRING,
        scope: str = UNIVERSAL_SCOPE,
        language: Language = Language.ENG,
    ) -> None:
        self.__entity_identifier = (
            entity_identifier if entity_identifier == UNIVERSAL_SCOPE else slugify(str(entity_identifier))
        )
        self.__identifier = str(uuid.uuid4()) if identifier == "" else slugify(str(identifier))

        self.name = name
        self.data_type = data_type
        self.language = language
        self.value = value

        self.scopes.add_scope(Scope(topic_identifier=scope))

    @property
    def entity_identifier(self) -> str:
        return self.__entity_identifier

    @entity_identifier.setter
    def entity_identifier(self, value: str) -> None:
        if value == "":
            raise TopicDbError("Empty 'value' parameter")
        self.__entity_identifier = value if value == UNIVERSAL_SCOPE else slugify(str(value))

    @property
    def identifier(self) -> str:
        return self.__identifier
