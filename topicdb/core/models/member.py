"""
Member class. Part of the StoryTechnologies project.

July 03, 2016
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

import uuid
from typing import List

from slugify import slugify  # type: ignore

from topicdb.core.topicdberror import TopicDbError


class Member:
    def __init__(
        self, topic_ref: str = "", role_spec: str = "related", identifier: str = ""
    ) -> None:
        if role_spec == "":
            raise TopicDbError("Empty 'role spec' parameter")
        self.__role_spec = slugify(str(role_spec))
        self.__topic_refs = [] if topic_ref == "" else [slugify(str(topic_ref))]
        self.__identifier = (
            str(uuid.uuid4()) if identifier == "" else slugify(str(identifier))
        )

    @property
    def role_spec(self) -> str:
        return self.__role_spec

    @role_spec.setter
    def role_spec(self, value: str) -> None:
        if value == "":
            raise TopicDbError("Empty 'value' parameter")
        self.__role_spec = slugify(str(value))

    @property
    def identifier(self) -> str:
        return self.__identifier

    @property
    def topic_refs(self) -> List[str]:
        return self.__topic_refs

    def add_topic_ref(self, topic_ref: str) -> None:
        if topic_ref == "":
            raise TopicDbError("Empty 'topic ref' parameter")
        self.__topic_refs.append(slugify(str(topic_ref)))

    def remove_topic_ref(self, topic_ref: str) -> None:
        self.__topic_refs[:] = [x for x in self.__topic_refs if x != topic_ref]

    def clear_topic_refs(self) -> None:
        del self.__topic_refs[:]
