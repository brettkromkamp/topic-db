"""
TopicStore class. Part of the Contextualise (https://contextualise.dev) project.

February 24, 2017
Brett Alistair Kromkamp (brettkromkamp@gmail.com)
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
from topicdb.core.models.map import Map
from topicdb.core.store.retrievalmode import RetrievalMode
from topicdb.core.store.ontologymode import OntologyMode
from topicdb.core.topicdberror import TopicDbError

import os
import sqlite3


TopicRefs = namedtuple("TopicRefs", ["instance_of", "role_spec", "topic_ref"])

UNIVERSAL_SCOPE = "*"
FALSE = 0
TRUE = 1
DATABASE_PATH = "data" + os.path.sep + "topics.db"

DDL = """
CREATE TABLE IF NOT EXISTS topic (
    identifier TEXT NOT NULL PRIMARY KEY,
    instance_of TEXT NOT NULL,
    scope TEXT
);
CREATE INDEX topic_1_index ON topic(instance_of);
CREATE INDEX topic_2_index ON topic(scope);
CREATE INDEX topic_3_index ON topic(instance_of, scope);

CREATE TABLE IF NOT EXISTS basename (
    identifier TEXT NOT NULL PRIMARY KEY,
    topic_identifier TEXT NOT NULL,
    name TEXT NOT NULL,
    scope TEXT NOT NULL,
    language TEXT NOT NULL
);
CREATE UNIQUE INDEX basename_1_index ON basename(topic_identifier, name);
CREATE INDEX basename_2_index ON basename(topic_identifier);
CREATE INDEX basename_3_index ON basename(topic_identifier, scope);
CREATE INDEX basename_4_index ON basename(topic_identifier, scope, language);

CREATE TABLE IF NOT EXISTS member (
    identifier TEXT NOT NULL PRIMARY KEY,
    association_identifier TEXT NOT NULL,
    src_role_spec TEXT NOT NULL,
    src_topic_ref TEXT NOT NULL,
    dest_role_spec TEXT NOT NULL,
    dest_topic_ref TEXT NOT NULL
);
CREATE UNIQUE INDEX member_1_index ON member(association_identifier, src_role_spec, src_topic_ref, dest_role_spec, dest_topic_ref);

CREATE TABLE IF NOT EXISTS occurrence (
    identifier TEXT NOT NULL PRIMARY KEY,
    topic_identifier TEXT NOT NULL,
    instance_of TEXT NOT NULL,
    resource_ref TEXT NOT NULL,
    resource_data BLOB,    
    scope TEXT NOT NULL,
    language TEXT NOT NULL
);
CREATE INDEX occurrence_1_index ON occurrence(topic_identifier);
CREATE INDEX occurrence_2_index ON occurrence(topic_identifier, scope, language);
CREATE INDEX occurrence_3_index ON occurrence(topic_identifier, instance_of, scope, language);

CREATE TABLE IF NOT EXISTS attribute (
    identifier TEXT NOT NULL PRIMARY KEY,
    entity_identifier TEXT NOT NULL,
    name TEXT NOT NULL,
    value TEXT NOT NULL,
    data_type TEXT NOT NULL,
    scope TEXT NOT NULL,
    language TEXT NOT NULL
);
CREATE UNIQUE INDEX attribute_1_index ON attribute(entity_identifier, name, scope, language);
CREATE INDEX attribute_2_index ON attribute(entity_identifier);
CREATE INDEX attribute_3_index ON attribute(entity_identifier, language);
CREATE INDEX attribute_4_index ON attribute(entity_identifier, scope);
CREATE INDEX attribute_5_index ON attribute(entity_identifier, scope, language);

CREATE TABLE IF NOT EXISTS map (
    name TEXT NOT NULL PRIMARY KEY,
    description TEXT,
    creation_datetime TEXT,
    modification_datetime TEXT
);

CREATE VIRTUAL TABLE text USING fts5 (
    occurrence_identifier,
    resource_data
);
"""


class TopicStore:
    def __init__(self, database_path=DATABASE_PATH) -> None:
        self.database_path = database_path

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

    # ========== ASSOCIATION ==========

    def delete_association(self, identifier: str) -> None:
        pass

    def get_association(
        self,
        identifier: str,
        scope: str = None,
        language: Language = None,
        resolve_attributes: RetrievalMode = RetrievalMode.DONT_RESOLVE_ATTRIBUTES,
        resolve_occurrences: RetrievalMode = RetrievalMode.DONT_RESOLVE_OCCURRENCES,
    ) -> Optional[Association]:
        pass

    def get_association_groups(
        self,
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

    def set_association(
        self,
        association: Association,
        ontology_mode: OntologyMode = OntologyMode.STRICT,
    ) -> None:
        pass

    # ========== ATTRIBUTE ==========

    def attribute_exists(self, entity_identifier: str, name: str) -> bool:
        pass

    def delete_attribute(self, identifier: str) -> None:
        pass

    def delete_attributes(self, entity_identifier: str) -> None:
        pass

    def get_attribute(self, identifier: str) -> Optional[Attribute]:
        pass

    def get_attributes(
        self,
        entity_identifier: str,
        scope: str = None,
        language: Language = None,
    ) -> List[Attribute]:
        pass

    def set_attribute(
        self,
        attribute: Attribute,
        ontology_mode: OntologyMode = OntologyMode.LENIENT,
    ) -> None:
        if attribute.entity_identifier == "":
            raise TopicDbError("Attribute has an empty 'entity identifier' property")

        if ontology_mode is OntologyMode.STRICT:
            scope_exists = self.topic_exists(attribute.scope)
            if not scope_exists:
                raise TopicDbError("Ontology 'STRICT' mode violation: 'scope' topic does not exist")

        connection = sqlite3.connect(self.database_path)

        try:
            with connection:
                connection.execute(
                    "INSERT INTO attribute (identifier, entity_identifier, name, value, data_type, scope, language) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (
                        attribute.identifier,
                        attribute.entity_identifier,
                        attribute.name,
                        attribute.value,
                        attribute.data_type.name.lower(),
                        attribute.scope,
                        attribute.language.name.lower(),
                    ),
                )
        except sqlite3.Error as error:
            raise TopicDbError("Error creating the attribute")
        finally:
            connection.close()

    def set_attributes(self, attributes: List[Attribute]) -> None:
        for attribute in attributes:
            self.set_attribute(attribute)

    def update_attribute_value(self, identifier: str, value: str) -> None:
        pass

    # ========== OCCURRENCE ==========

    def delete_occurrence(self, identifier: str) -> None:
        pass

    def delete_occurrences(self, topic_identifier: str) -> None:
        pass

    def get_occurrence(
        self,
        map_identifier: int,
        identifier: str,
        inline_resource_data: RetrievalMode = RetrievalMode.DONT_INLINE_RESOURCE_DATA,
        resolve_attributes: RetrievalMode = RetrievalMode.DONT_RESOLVE_ATTRIBUTES,
    ) -> Optional[Occurrence]:
        pass

    def get_occurrence_data(self, identifier: str) -> Optional[bytes]:
        pass

    def get_occurrences(
        self,
        instance_of: str = None,
        scope: str = None,
        language: Language = None,
        offset: int = 0,
        limit: int = 100,
        inline_resource_data: RetrievalMode = RetrievalMode.DONT_INLINE_RESOURCE_DATA,
        resolve_attributes: RetrievalMode = RetrievalMode.DONT_RESOLVE_ATTRIBUTES,
    ) -> List[Occurrence]:
        pass

    def occurrence_exists(self, identifier: str) -> bool:
        pass

    def set_occurrence(
        self,
        occurrence: Occurrence,
        ontology_mode: OntologyMode = OntologyMode.STRICT,
    ) -> None:
        pass

    def update_occurrence_data(self, identifier: str, resource_data: Union[str, bytes]) -> None:
        pass

    def update_occurrence_scope(self, identifier: str, scope: str) -> None:
        pass

    def update_occurrence_topic_identifier(self, identifier: str, topic_identifier: str) -> None:
        pass

    # ========== TAG ==========

    def get_tags(self, identifier: str) -> List[Optional[str]]:
        pass

    def set_tag(self, identifier: str, tag: str) -> None:
        pass

    def set_tags(self, identifier: str, tags: List[str]) -> None:
        pass

    # ========== TOPIC ==========

    @staticmethod
    def _normalize_topic_name(topic_identifier):
        return " ".join([word.capitalize() for word in topic_identifier.split("-")])

    def delete_topic(
        self,
        identifier: str,
        ontology_mode: OntologyMode = OntologyMode.STRICT,
    ) -> None:
        pass

    def get_related_topics(
        self,
        identifier: str,
        instance_ofs: Optional[List[str]] = None,
        scope: str = None,
    ) -> List[Optional[Topic]]:
        pass

    def get_topic(
        self,
        identifier: str,
        scope: str = None,
        language: Language = None,
        resolve_attributes: RetrievalMode = RetrievalMode.DONT_RESOLVE_ATTRIBUTES,
        resolve_occurrences: RetrievalMode = RetrievalMode.DONT_RESOLVE_OCCURRENCES,
    ) -> Optional[Topic]:
        pass

    def get_topic_associations(
        self,
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
        query: str,
        instance_ofs: Optional[List[str]] = None,
        offset: int = 0,
        limit: int = 100,
    ) -> List[str]:
        pass

    def get_topic_names(  # TODO: Refactor method to return a namedtuple including 'scope' and 'language' fields
        self, offset: int = 0, limit: int = 100
    ) -> List[Tuple[str, str]]:
        pass

    def get_topic_occurrences(
        self,
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
        instance_of: str = None,
        language: Language = None,
        offset: int = 0,
        limit: int = 100,
        resolve_attributes=RetrievalMode.DONT_RESOLVE_ATTRIBUTES,
    ) -> List[Optional[Topic]]:
        pass

    def get_topic_identifiers_by_attribute_name(
        self,
        name: str = None,
        instance_of: str = None,
        scope: str = None,
        language: Language = None,
    ) -> List[Optional[str]]:
        pass

    def get_topics_by_attribute_name(
        self,
        name: str = None,
        instance_of: str = None,
        scope: str = None,
        language: Language = None,
        resolve_attributes=RetrievalMode.DONT_RESOLVE_ATTRIBUTES,
    ) -> List[Optional[Topic]]:
        pass

    def set_topic(
        self,
        topic: Topic,
        ontology_mode: OntologyMode = OntologyMode.STRICT,
    ) -> None:
        if ontology_mode is OntologyMode.STRICT:
            instance_of_exists = self.topic_exists(topic.instance_of)
            if not instance_of_exists:
                raise TopicDbError("Ontology 'STRICT' mode violation: 'instance Of' topic does not exist")

        connection = sqlite3.connect(self.database_path)

        try:
            with connection:
                connection.execute(
                    "INSERT INTO topic (identifier, instance_of) VALUES (?, ?)",
                    (topic.identifier, topic.instance_of),
                )
                for base_name in topic.base_names:
                    connection.execute(
                        "INSERT INTO basename (identifier, name, topic_identifier, scope, language) VALUES (?, ?, ?, ?, ?)",
                        (
                            base_name.identifier,
                            base_name.name,
                            topic.identifier,
                            base_name.scope,
                            base_name.language.name.lower(),
                        ),
                    )
            if not topic.get_attribute_by_name("creation-timestamp"):
                timestamp = datetime.utcnow().replace(microsecond=0).isoformat()
                timestamp_attribute = Attribute(
                    "creation-timestamp",
                    timestamp,
                    topic.identifier,
                    data_type=DataType.TIMESTAMP,
                    scope=UNIVERSAL_SCOPE,
                    language=Language.ENG,
                )
                topic.add_attribute(timestamp_attribute)
        except sqlite3.Error as error:
            raise TopicDbError("Error creating the topic")
        finally:
            connection.close()
        self.set_attributes(topic.attributes)

    def update_topic_instance_of(self, identifier: str, instance_of: str) -> None:
        pass

    def update_topic_identifier(self, old_identifier: str, new_identifier: str) -> None:
        pass

    def set_base_name(self, identifier: str, base_name: BaseName) -> None:
        pass

    def update_base_name(
        self,
        identifier: str,
        name: str,
        scope: str,
        language: Language = Language.ENG,
    ) -> None:
        pass

    def delete_base_name(self, identifier: str) -> None:
        pass

    def topic_exists(self, identifier: str) -> bool:
        result = False

        connection = sqlite3.connect(self.database_path)
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT identifier FROM topic WHERE identifier = ?", (identifier,))
            record = cursor.fetchone()
            if record:
                result = True
        except sqlite3.Error as error:
            raise TopicDbError("Error retrieving the topic map")
        finally:
            cursor.close()
            connection.close()

        return result

    def is_topic(self, identifier: str) -> bool:
        pass

    # ========== TOPIC MAP ==========

    def initialise_map(self, name, description):
        map = Map(name, description)
        connection = sqlite3.connect(self.database_path)
        try:
            with connection:
                connection.execute(
                    "INSERT INTO map (name, description, creation_datetime) VALUES (?, ?, ?)",
                    (name, description, map.creation_datetime),
                )
        except sqlite3.Error as error:
            raise TopicDbError("Error initialising the topic map")
        finally:
            connection.close()

        if not self.topic_exists("home"):
            for k, v in self.base_topics.items():
                topic = Topic(
                    identifier=k,
                    instance_of="base-topic",
                    name=v,
                )
                self.set_topic(topic, OntologyMode.LENIENT)

    def update_map(self, map: Map) -> None:
        connection = sqlite3.connect(self.database_path)
        try:
            with connection:
                connection.execute(
                    "UPDATE map (name, description, modification_datetime) VALUES (?, ?, ?)",
                    (map.name, map.description, datetime.utcnow().replace(microsecond=0).isoformat()),
                )
        except sqlite3.Error as error:
            raise TopicDbError("Error updating the topic map")
        finally:
            connection.close()

    def get_map(self) -> Map:
        result = None

        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT name, description, creation_datetime, modification_datetime FROM map")
            record = cursor.fetchone()
            if record:
                result = Map(name=record["name"], description=record["description"])
                result.creation_datetime = record["creation_datetime"]
                result.modification_datetime = record["modification_datetime"]
        except sqlite3.Error as error:
            raise TopicDbError("Error retrieving the topic map")
        finally:
            cursor.close()
            connection.close()

        return result

    # ========== DATABASE ==========

    def create_database(self):
        statements = DDL.split(";")

        connection = sqlite3.connect(self.database_path)
        try:
            with connection:
                for statement in statements:
                    connection.execute(statement)
        except sqlite3.Error as error:
            raise TopicDbError("Error creating the database")
        finally:
            connection.close()

    # ========== STATISTICS ==========

    def get_topic_occurrences_statistics(self, identifier: str, scope: str = None) -> Dict:
        pass
