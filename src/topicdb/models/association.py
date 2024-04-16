"""
Association class. Part of the Contextualise (https://contextualise.dev) project.

July 03, 2016
Brett Alistair Kromkamp (brettkromkamp@gmail.com)
"""

from slugify import slugify
from topicdb.models.language import Language
from topicdb.models.member import Member
from topicdb.models.scope import Scope
from topicdb.models.topic import Topic
from topicdb.topicdberror import TopicDbError

UNIVERSAL_SCOPE = "*"


class Association(Topic):
    def __init__(
        self,
        identifier: str = "",
        instance_of: str = "association",
        name: str = "Undefined",
        language: Language = Language.ENG,
        scope: str = UNIVERSAL_SCOPE,
        src_topic_ref: str = "",
        src_role_spec: str = "related",
        dest_topic_ref: str = "",
        dest_role_spec: str = "related",
    ) -> None:
        super().__init__(identifier, instance_of, name, scope, language)  # Base name 'scope' parameter

        self.member: Member = Member()

        if src_topic_ref != "" and src_role_spec != "" and dest_topic_ref != "" and dest_role_spec != "":
            member = Member(src_topic_ref, src_role_spec, dest_topic_ref, dest_role_spec)
            self.member = member

        self.scopes.add_scope(Scope(topic_identifier=scope))
