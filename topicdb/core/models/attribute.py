"""
Attribute class. Part of the StoryTechnologies Builder project.

June 12, 2016
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

import uuid

from slugify import slugify  # type: ignore

from topicdb.core.store.topicstoreerror import TopicStoreError
from topicdb.core.models.datatype import DataType
from topicdb.core.models.language import Language


class Attribute:

    def __init__(self, name: str, value: str, entity_identifier: str,
                 identifier: str = '',
                 data_type: DataType = DataType.STRING,
                 scope: str = '*',
                 language: Language = Language.ENG) -> None:
        if entity_identifier == '*':  # Universal Scope.
            self.__entity_identifier = '*'
        else:
            self.__entity_identifier = slugify(str(entity_identifier))

        self.__identifier = (str(uuid.uuid4()) if identifier == '' else slugify(str(identifier)))
        self.__scope = scope if scope == '*' else slugify(scope)

        self.name = name
        self.data_type = data_type
        self.language = language
        self.value = value

    def __repr__(self) -> str:
        return "Attribute('{0}', '{1}', '{2}', '{3}', {4}, '{5}', {6})".format(
            self.name,
            self.value,
            self.__entity_identifier,
            self.__identifier,
            str(self.data_type),
            self.__scope,
            str(self.language))

    @property
    def entity_identifier(self) -> str:
        return self.__entity_identifier

    @entity_identifier.setter
    def entity_identifier(self, value: str) -> None:
        if value == '':
            raise TopicStoreError("Empty 'value' parameter")
        elif value == '*':  # Universal Scope.
            self.__entity_identifier = '*'
        else:
            self.__entity_identifier = slugify(str(value))

    @property
    def identifier(self) -> str:
        return self.__identifier

    @property
    def scope(self) -> str:
        return self.__scope

    @scope.setter
    def scope(self, value: str) -> None:
        if value == '':
            raise TopicStoreError("Empty 'value' parameter")
        self.__scope = value if value == '*' else slugify(str(value))
