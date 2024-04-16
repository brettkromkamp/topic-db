"""
Scopes class. Part of the Contextualise (https://contextualise.dev) project.

April 16, 2024
Brett Alistair Kromkamp (brettkromkamp@gmail.com)
"""

from typing import List

from slugify import slugify
from topicdb.models.scope import Scope


class Scopes:
    def __init__(self) -> None:
        self.__scopes: List[Scope] = []

    @property
    def scopes(self) -> List[Scope]:
        return self.__scopes

    def add_scope(self, scope: Scope) -> None:
        self.__scopes.append(scope)

    def add_scopes(self, scopes: List[Scope]) -> None:
        self.__scopes = [*self.__scopes, *scopes]

    def remove_scope(self, identifier: str) -> None:
        self.__scopes[:] = [x for x in self.__scopes if x.identifier != identifier]
