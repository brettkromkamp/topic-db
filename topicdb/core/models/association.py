"""
Association class. Part of the StoryTechnologies project.

July 03, 2016
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

from typing import List, Optional

from slugify import slugify  # type: ignore

from topicdb.core.models.language import Language
from topicdb.core.models.member import Member
from topicdb.core.models.topic import Topic
from topicdb.core.topicdberror import TopicDbError


class Association(Topic):
    def __init__(
        self,
        identifier: str = "",
        instance_of: str = "association",
        base_name: str = "Undefined",
        language: Language = Language.ENG,
        scope: str = "*",
        src_topic_ref: str = "",
        dest_topic_ref: str = "",
        src_role_spec: str = "related",
        dest_role_spec: str = "related",
    ) -> None:
        super().__init__(identifier, instance_of, base_name, language)

        self.__scope = scope if scope == "*" else slugify(str(scope))
        self.__members: List[Member] = []

        if (
            src_topic_ref != ""
            and src_role_spec != ""
            and dest_topic_ref != ""
            and dest_role_spec != ""
        ):
            src_member = Member(src_topic_ref, src_role_spec)
            dest_member = Member(dest_topic_ref, dest_role_spec)
            self.__members.append(src_member)
            self.__members.append(dest_member)

    @property
    def scope(self) -> str:
        return self.__scope

    @scope.setter
    def scope(self, value: str) -> None:
        if value == "":
            raise TopicDbError("Empty 'scope' parameter")
        self.__scope = value if value == "*" else slugify(str(value))

    @property
    def members(self) -> List[Member]:
        return self.__members

    def create_member(self, topic_ref: str, role_spec: str = "related") -> None:
        member = Member(topic_ref, role_spec)
        self.add_member(member)

    def create_members(
        self,
        src_topic_ref: str,
        dest_topic_ref: str,
        src_role_spec: str = "related",
        dest_role_spec: str = "related",
    ) -> None:
        members = [
            Member(src_topic_ref, src_role_spec),
            Member(dest_topic_ref, dest_role_spec),
        ]
        self.add_members(members)

    def add_member(self, member: Member) -> None:
        self.__members.append(member)

    def add_members(self, members: List[Member]) -> None:
        self.__members = [*self.__members, *members]

    def remove_member(self, identifier: str) -> None:
        self.__members[:] = [x for x in self.__members if x.identifier != identifier]

    def get_member_by_role(self, role: str) -> Optional[Member]:
        result = None
        for member in self.__members:
            if member.role_spec == role:
                result = member
                break
        return result

    def clear_members(self) -> None:
        del self.__members[:]
