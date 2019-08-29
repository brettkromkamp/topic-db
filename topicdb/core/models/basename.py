"""
BaseName class. Part of the StoryTechnologies project.

June 12, 2016
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

import uuid

from slugify import slugify  # type: ignore

from topicdb.core.models.language import Language


class BaseName:
    def __init__(
        self, name: str, language: Language = Language.ENG, identifier: str = ""
    ) -> None:
        self.__identifier = (
            str(uuid.uuid4()) if identifier == "" else slugify(str(identifier))
        )

        self.name = name
        self.language = language

    @property
    def identifier(self) -> str:
        return self.__identifier
