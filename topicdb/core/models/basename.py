"""
BaseName class. Part of the StoryTechnologies project.

June 12, 2016
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

import uuid

from slugify import slugify  # type: ignore
from topicdb.core.models.language import Language
from topicdb.core.topicdberror import TopicDbError


class BaseName:
    def __init__(
            self,
            name: str,
            scope: str = "*",
            language: Language = Language.ENG,
            identifier: str = "",
    ) -> None:
        self.__identifier = (
            str(uuid.uuid4()) if identifier == "" else slugify(str(identifier))
        )

        self.name = name
        self.__scope = scope if scope == "*" else slugify(str(scope))
        self.language = language

    @property
    def identifier(self) -> str:
        return self.__identifier

    @property
    def scope(self) -> str:
        return self.__scope

    @scope.setter
    def scope(self, value: str) -> None:
        if value == "":
            raise TopicDbError("Empty 'value' parameter")
        self.__scope = value if value == "*" else slugify(str(value))
