"""
TopicStore class. Part of the Contextualise (https://contextualise.dev) project.

February 24, 2017
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

from __future__ import annotations

from collections import namedtuple
from datetime import datetime
from typing import Optional, List, Union, Dict, Tuple

from typedtree.tree import Tree  # type: ignore

from topicdb.core.models.association import Association
from topicdb.core.models.attribute import Attribute
from topicdb.core.models.basename import BaseName
from topicdb.core.models.datatype import DataType
from topicdb.core.models.doublekeydict import DoubleKeyDict
from topicdb.core.models.language import Language
from topicdb.core.models.member import Member
from topicdb.core.models.occurrence import Occurrence
from topicdb.core.models.topic import Topic
from topicdb.core.models.map import TopicMap
from topicdb.core.store.retrievalmode import RetrievalMode
from topicdb.core.store.ontologymode import OntologyMode
from topicdb.core.topicdberror import TopicDbError

TopicRefs = namedtuple("TopicRefs", ["instance_of", "role_spec", "topic_ref"])

UNIVERSAL_SCOPE = "*"
MIN_CONNECTIONS = 1
MAX_CONNECTIONS = 20


class TopicStore:
    def __init__(self) -> None:

        self.base_topics = {
            UNIVERSAL_SCOPE: "Universal",
            "home": "Home",
            "entity": "Entity",
            "topic": "Topic",
            "base-topic": "Base Topic",
            "association": "Association",
            "occurrence": "Occurrence",
            "navigation": "Navigation",
            "member": "Member",
            "category": "Category",
            "categorization": "Categorization",
            "tag": "Tag",
            "tags": "Tags",
            "note": "Note",
            "notes": "Notes",
            "broader": "Broader",
            "narrower": "Narrower",
            "related": "Related",
            "parent": "Parent",
            "child": "Child",
            "previous": "Previous",
            "next": "Next",
            "up": "Up",
            "down": "Down",
            "image": "Image",
            "video": "Video",
            "audio": "Audio",
            "note": "Note",
            "file": "File",
            "url": "URL",
            "text": "Text",
            "3d-scene": "3D Scene",
            "string": "String",
            "number": "Number",
            "timestamp": "Timestamp",
            "boolean": "Boolean",
            "eng": "English Language",
            "spa": "Spanish Language",
            "nld": "Dutch Language",
        }

    def open(self) -> TopicStore:
        pass

    def close(self) -> None:
        pass

    # Context manager methods
    def __enter__(self) -> TopicStore:
        return self.open()

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    # ========== ASSOCIATION ==========

    def delete_association(self, map_identifier: int, identifier: str) -> None:
        pass

    def get_association(
        self,
        map_identifier: int,
        identifier: str,
        scope: str = None,
        language: Language = None,
        resolve_attributes: RetrievalMode = RetrievalMode.DONT_RESOLVE_ATTRIBUTES,
        resolve_occurrences: RetrievalMode = RetrievalMode.DONT_RESOLVE_OCCURRENCES,
    ) -> Optional[Association]:
        pass

    def get_association_groups(
        self,
        map_identifier: int,
        identifier: str = "",
        associations: Optional[List[Association]] = None,
        instance_ofs: Optional[List[str]] = None,
        scope: str = None,
    ) -> DoubleKeyDict:
        pass

    @staticmethod
    def _resolve_topic_refs(association: Association) -> List[TopicRefs]:
        result: List[TopicRefs] = []

        result.append(
            TopicRefs(association.instance_of, association.member.src_role_spec, association.member.src_topic_ref)
        )
        result.append(
            TopicRefs(association.instance_of, association.member.dest_role_spec, association.member.dest_topic_ref)
        )
        return result

    def get_associations(self):
        pass

    def set_association(
        self,
        map_identifier: int,
        association: Association,
        ontology_mode: OntologyMode = OntologyMode.STRICT,
    ) -> None:
        pass

    # ========== ATTRIBUTE ==========

    def attribute_exists(self, map_identifier: int, entity_identifier: str, name: str) -> bool:
        pass

    def delete_attribute(self, map_identifier: int, identifier: str) -> None:
        pass

    def delete_attributes(self, map_identifier: int, entity_identifier: str) -> None:
        pass

    def get_attribute(self, map_identifier: int, identifier: str) -> Optional[Attribute]:
        pass

    def get_attributes(
        self,
        map_identifier: int,
        entity_identifier: str,
        scope: str = None,
        language: Language = None,
    ) -> List[Attribute]:
        pass

    def set_attribute(
        self,
        map_identifier: int,
        attribute: Attribute,
        ontology_mode: OntologyMode = OntologyMode.LENIENT,
    ) -> None:
        pass

    def set_attributes(self, map_identifier: int, attributes: List[Attribute]) -> None:
        pass

    def update_attribute_value(self, map_identifier: int, identifier: str, value: str) -> None:
        pass

    # ========== OCCURRENCE ==========

    def delete_occurrence(self, map_identifier: int, identifier: str) -> None:
        pass

    def delete_occurrences(self, map_identifier: int, topic_identifier: str) -> None:
        pass

    def get_occurrence(
        self,
        map_identifier: int,
        identifier: str,
        inline_resource_data: RetrievalMode = RetrievalMode.DONT_INLINE_RESOURCE_DATA,
        resolve_attributes: RetrievalMode = RetrievalMode.DONT_RESOLVE_ATTRIBUTES,
    ) -> Optional[Occurrence]:
        pass

    def get_occurrence_data(self, map_identifier: int, identifier: str) -> Optional[bytes]:
        pass

    def get_occurrences(
        self,
        map_identifier: int,
        instance_of: str = None,
        scope: str = None,
        language: Language = None,
        offset: int = 0,
        limit: int = 100,
        inline_resource_data: RetrievalMode = RetrievalMode.DONT_INLINE_RESOURCE_DATA,
        resolve_attributes: RetrievalMode = RetrievalMode.DONT_RESOLVE_ATTRIBUTES,
    ) -> List[Occurrence]:
        pass

    def occurrence_exists(self, map_identifier: int, identifier: str) -> bool:
        pass

    def set_occurrence(
        self,
        map_identifier: int,
        occurrence: Occurrence,
        ontology_mode: OntologyMode = OntologyMode.STRICT,
    ) -> None:
        pass

    def update_occurrence_data(self, map_identifier: int, identifier: str, resource_data: Union[str, bytes]) -> None:
        pass

    def update_occurrence_scope(self, map_identifier: int, identifier: str, scope: str) -> None:
        pass

    def update_occurrence_topic_identifier(self, map_identifier: int, identifier: str, topic_identifier: str) -> None:
        pass

    # ========== TAG ==========

    def get_tags(self, map_identifier: int, identifier: str) -> List[Optional[str]]:
        pass

    def set_tag(self, map_identifier: int, identifier: str, tag: str) -> None:
        pass

    def set_tags(self, map_identifier: int, identifier: str, tags: List[str]) -> None:
        pass

    # ========== TOPIC ==========

    @staticmethod
    def _normalize_topic_name(topic_identifier):
        return " ".join([word.capitalize() for word in topic_identifier.split("-")])

    def delete_topic(
        self,
        map_identifier: int,
        identifier: str,
        ontology_mode: OntologyMode = OntologyMode.STRICT,
    ) -> None:
        pass

    def get_related_topics(
        self,
        map_identifier: int,
        identifier: str,
        instance_ofs: Optional[List[str]] = None,
        scope: str = None,
    ) -> List[Optional[Topic]]:
        pass

    def get_topic(
        self,
        map_identifier: int,
        identifier: str,
        scope: str = None,
        language: Language = None,
        resolve_attributes: RetrievalMode = RetrievalMode.DONT_RESOLVE_ATTRIBUTES,
        resolve_occurrences: RetrievalMode = RetrievalMode.DONT_RESOLVE_OCCURRENCES,
    ) -> Optional[Topic]:
        pass

    def get_topic_associations(
        self,
        map_identifier: int,
        identifier: str,
        instance_ofs: Optional[List[str]] = None,
        scope: str = None,
        language: Language = None,
        resolve_attributes: RetrievalMode = RetrievalMode.DONT_RESOLVE_ATTRIBUTES,
        resolve_occurrences: RetrievalMode = RetrievalMode.DONT_RESOLVE_OCCURRENCES,
    ) -> List[Association]:
        pass

    def get_topics_network(
        self,
        map_identifier: int,
        identifier: str,
        maximum_depth: int = 3,
        cumulative_depth: int = 0,
        accumulative_tree: Tree = None,
        accumulative_nodes: List[str] = None,
        instance_ofs: Optional[List[str]] = None,
        scope: str = None,
    ) -> Tree:
        pass

    def get_topic_identifiers(
        self,
        map_identifier: int,
        query: str,
        instance_ofs: Optional[List[str]] = None,
        offset: int = 0,
        limit: int = 100,
    ) -> List[str]:
        pass

    def get_topic_names(  # TODO: Refactor method to return a namedtuple including 'scope' and 'language' fields
        self, map_identifier: int, offset: int = 0, limit: int = 100
    ) -> List[Tuple[str, str]]:
        pass

    def get_topic_occurrences(
        self,
        map_identifier: int,
        identifier: str,
        instance_of: str = None,
        scope: str = None,
        language: Language = None,
        inline_resource_data: RetrievalMode = RetrievalMode.DONT_INLINE_RESOURCE_DATA,
        resolve_attributes: RetrievalMode = RetrievalMode.DONT_RESOLVE_ATTRIBUTES,
    ) -> List[Occurrence]:
        pass

    def get_topics(
        self,
        map_identifier: int,
        instance_of: str = None,
        language: Language = None,
        offset: int = 0,
        limit: int = 100,
        resolve_attributes=RetrievalMode.DONT_RESOLVE_ATTRIBUTES,
    ) -> List[Optional[Topic]]:
        pass

    def get_topic_identifiers_by_attribute_name(
        self,
        map_identifier: int,
        name: str = None,
        instance_of: str = None,
        scope: str = None,
        language: Language = None,
    ) -> List[Optional[str]]:
        pass

    def get_topics_by_attribute_name(
        self,
        map_identifier: int,
        name: str = None,
        instance_of: str = None,
        scope: str = None,
        language: Language = None,
        resolve_attributes=RetrievalMode.DONT_RESOLVE_ATTRIBUTES,
    ) -> List[Optional[Topic]]:
        pass

    def set_topic(
        self,
        map_identifier: int,
        topic: Topic,
        ontology_mode: OntologyMode = OntologyMode.STRICT,
    ) -> None:
        pass

    def update_topic_instance_of(self, map_identifier: int, identifier: str, instance_of: str) -> None:
        pass

    def update_topic_identifier(self, map_identifier: int, old_identifier: str, new_identifier: str) -> None:
        pass

    def set_base_name(self, map_identifier: int, identifier: str, base_name: BaseName) -> None:
        pass

    def update_base_name(
        self,
        map_identifier: int,
        identifier: str,
        name: str,
        scope: str,
        language: Language = Language.ENG,
    ) -> None:
        pass

    def delete_base_name(self, map_identifier: int, identifier: str) -> None:
        pass

    def topic_exists(self, map_identifier: int, identifier: str) -> bool:
        pass

    def is_topic(self, map_identifier: int, identifier: str) -> bool:
        pass

    # ========== TOPIC MAP ==========

    def initialise_map(self, map_identifier: int, user_identifier: int) -> None:
        pass

    # ========== STATISTICS ==========

    def get_topic_occurrences_statistics(self, map_identifier: int, identifier: str, scope: str = None) -> Dict:
        pass

    def get_map_statistics(self, map_identifier: int) -> Dict:
        pass
