"""
Occurrence class. Part of the StoryTechnologies project.

June 12, 2016
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

from typing import Optional

from slugify import slugify  # type: ignore

from topicdb.core.store.topicstoreerror import TopicStoreError
from topicdb.core.models.entity import Entity
from topicdb.core.models.language import Language


class Occurrence(Entity):

    def __init__(self,
                 identifier: str = '',
                 instance_of: str = 'occurrence',
                 topic_identifier: str = '',
                 scope: str = '*',  # Universal scope
                 resource_ref: str = '',
                 resource_data: Optional[bytes] = None,
                 language: Language = Language.ENG) -> None:
        super().__init__(identifier, instance_of)

        if topic_identifier == '*':  # Universal Scope.
            self.__topic_identifier = '*'
        else:
            self.__topic_identifier = slugify(str(topic_identifier))

        self.__scope = scope if scope == '*' else slugify(str(scope))

        self.resource_ref = resource_ref
        self.resource_data = resource_data
        self.language = language

    @property
    def scope(self) -> str:
        return self.__scope

    @scope.setter
    def scope(self, value: str) -> None:
        if value == '':
            raise TopicStoreError("Empty 'value' parameter")
        self.__scope = value if value == '*' else slugify(str(value))

    @property
    def topic_identifier(self) -> str:
        return self.__topic_identifier

    @topic_identifier.setter
    def topic_identifier(self, value: str) -> None:
        if value == '':
            raise TopicStoreError("Empty 'value' parameter")
        elif value == '*':  # Universal Scope.
            self.__topic_identifier = '*'
        else:
            self.__topic_identifier = slugify(str(value))

    def has_data(self) -> bool:
        return self.resource_data is not None
