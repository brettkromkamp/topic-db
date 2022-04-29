"""
Member class. Part of the Contextualise (https://contextualise.dev) project.

July 03, 2016
Brett Alistair Kromkamp (brettkromkamp@gmail.com)
"""

import uuid
from typing import List

from slugify import slugify  # type: ignore
from topicdb.core.topicdberror import TopicDbError


class Member:
    def __init__(
        self,
        src_topic_ref: str = "",
        src_role_spec: str = "related",
        dest_topic_ref: str = "",
        dest_role_spec: str = "related",
        identifier: str = "",
    ) -> None:
        if src_role_spec == "":
            raise TopicDbError("Empty 'src_role spec' parameter")
        if dest_role_spec == "":
            raise TopicDbError("Empty 'dest_role spec' parameter")
        self.__src_topic_ref = slugify(str(src_topic_ref))
        self.__src_role_spec = slugify(str(src_role_spec))
        self.__dest_topic_ref = slugify(str(dest_topic_ref))
        self.__dest_role_spec = slugify(str(dest_role_spec))
        self.__identifier = str(uuid.uuid4()) if identifier == "" else slugify(str(identifier))

    @property
    def src_topic_ref(self) -> str:
        return self.__src_topic_ref

    @src_topic_ref.setter
    def src_topic_ref(self, value: str) -> None:
        if value == "":
            raise TopicDbError("Empty 'value' parameter")
        self.__src_topic_ref = slugify(str(value))

    @property
    def src_role_spec(self) -> str:
        return self.__src_role_spec

    @src_role_spec.setter
    def src_role_spec(self, value: str) -> None:
        if value == "":
            raise TopicDbError("Empty 'value' parameter")
        self.__src_role_spec = slugify(str(value))

    @property
    def dest_topic_ref(self) -> str:
        return self.__dest_topic_ref

    @dest_topic_ref.setter
    def dest_topic_ref(self, value: str) -> None:
        if value == "":
            raise TopicDbError("Empty 'value' parameter")
        self.__dest_topic_ref = slugify(str(value))

    @property
    def dest_role_spec(self) -> str:
        return self.__dest_role_spec

    @dest_role_spec.setter
    def dest_role_spec(self, value: str) -> None:
        if value == "":
            raise TopicDbError("Empty 'value' parameter")
        self.__dest_role_spec = slugify(str(value))

    @property
    def identifier(self) -> str:
        return self.__identifier
