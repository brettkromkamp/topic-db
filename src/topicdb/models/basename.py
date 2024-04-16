"""
BaseName class. Part of the Contextualise (https://contextualise.dev) project.

June 12, 2016
Brett Alistair Kromkamp (brettkromkamp@gmail.com)
"""

import uuid

from slugify import slugify
from topicdb.models.language import Language
from topicdb.models.scope import Scope
from topicdb.models.scopes import Scopes

UNIVERSAL_SCOPE = "*"


class BaseName(Scopes):
    def __init__(
        self,
        name: str,
        scope: str = UNIVERSAL_SCOPE,
        language: Language = Language.ENG,
        identifier: str = "",
    ) -> None:
        self.__identifier = str(uuid.uuid4()) if identifier == "" else slugify(str(identifier))

        self.name = name
        self.language = language

        self.scopes.add_scope(Scope(topic_identifier=scope))

    @property
    def identifier(self) -> str:
        return self.__identifier
