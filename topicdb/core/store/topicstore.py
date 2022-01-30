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
from topicdb.core.models.collaborationmode import CollaborationMode
from topicdb.core.models.collaborator import Collaborator
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

_UNIVERSAL_SCOPE = "*"
_DATABASE_PATH = "topics.db"
_DDL = """
CREATE TABLE IF NOT EXISTS topic (
    map_identifier INTEGER NOT NULL,
    identifier TEXT NOT NULL,
    instance_of TEXT NOT NULL,
    scope TEXT,
    PRIMARY KEY (map_identifier, identifier)
);
CREATE INDEX topic_1_index ON topic (map_identifier);
CREATE INDEX topic_2_index ON topic (map_identifier, instance_of);
CREATE INDEX topic_3_index ON topic (map_identifier, identifier, scope);
CREATE INDEX topic_4_index ON topic (map_identifier, instance_of, scope);
CREATE INDEX topic_5_index ON topic (map_identifier, scope);
CREATE TABLE IF NOT EXISTS basename (
    map_identifier INTEGER NOT NULL,
    identifier TEXT NOT NULL,
    name TEXT NOT NULL,
    topic_identifier TEXT NOT NULL,
    scope TEXT NOT NULL,
    language TEXT NOT NULL,
    PRIMARY KEY (map_identifier, identifier)
);
CREATE INDEX basename_1_index ON basename (map_identifier);
CREATE INDEX basename_2_index ON basename (map_identifier, topic_identifier);
CREATE INDEX basename_3_index ON basename (map_identifier, topic_identifier, scope);
CREATE INDEX basename_4_index ON basename (map_identifier, topic_identifier, scope, language);
CREATE TABLE IF NOT EXISTS member (
    map_identifier INTEGER NOT NULL,
    identifier TEXT NOT NULL,
    association_identifier TEXT NOT NULL,
    src_topic_ref TEXT NOT NULL,
    src_role_spec TEXT NOT NULL,
    dest_topic_ref TEXT NOT NULL,
    dest_role_spec TEXT NOT NULL,
    PRIMARY KEY (map_identifier, identifier)
);
CREATE UNIQUE INDEX member_1_index ON member(map_identifier, association_identifier, src_role_spec, src_topic_ref, dest_role_spec, dest_topic_ref);
CREATE TABLE IF NOT EXISTS occurrence (
    map_identifier INTEGER NOT NULL,
    identifier TEXT NOT NULL,
    instance_of TEXT NOT NULL,
    scope TEXT NOT NULL,
    resource_ref TEXT NOT NULL,
    resource_data BLOB,
    topic_identifier TEXT NOT NULL,
    language TEXT NOT NULL,
    PRIMARY KEY (map_identifier, identifier)
);
CREATE INDEX occurrence_1_index ON occurrence (map_identifier);
CREATE INDEX occurrence_2_index ON occurrence (map_identifier, topic_identifier);
CREATE INDEX occurrence_3_index ON occurrence (map_identifier, topic_identifier, scope, language);
CREATE INDEX occurrence_4_index ON occurrence (map_identifier, topic_identifier, instance_of, scope, language);
CREATE TABLE IF NOT EXISTS attribute (
    map_identifier INTEGER NOT NULL,
    identifier TEXT NOT NULL,
    entity_identifier TEXT NOT NULL,
    name TEXT NOT NULL,
    value TEXT NOT NULL,
    data_type TEXT NOT NULL,
    scope TEXT NOT NULL,
    language TEXT NOT NULL,
    PRIMARY KEY (map_identifier, entity_identifier, name, scope, language)
);
CREATE INDEX attribute_1_index ON attribute (map_identifier);
CREATE INDEX attribute_2_index ON attribute (map_identifier, identifier);
CREATE INDEX attribute_3_index ON attribute (map_identifier, entity_identifier);
CREATE INDEX attribute_4_index ON attribute (map_identifier, entity_identifier, language);
CREATE INDEX attribute_5_index ON attribute (map_identifier, entity_identifier, scope);
CREATE INDEX attribute_6_index ON attribute (map_identifier, entity_identifier, scope, language);
CREATE TABLE IF NOT EXISTS map (
    identifier INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    image_path TEXT,
    initialised BOOLEAN DEFAULT FALSE NOT NULL,
    published BOOLEAN DEFAULT FALSE NOT NULL,
    promoted BOOLEAN DEFAULT FALSE NOT NULL
);
CREATE INDEX map_1_index ON map (published);
CREATE INDEX map_2_index ON map (promoted);
CREATE TABLE IF NOT EXISTS user_map (
    user_identifier INT NOT NULL,
    map_identifier INT NOT NULL,
    owner BOOLEAN DEFAULT FALSE NOT NULL,
    collaboration_mode TEXT NOT NULL,
    PRIMARY KEY (user_identifier, map_identifier)
);
CREATE INDEX user_map_1_index ON user_map (owner);
CREATE VIRTUAL TABLE text USING fts5 (
    occurrence_identifier,
    resource_data
);
"""


class TopicStore:
    def __init__(self, database_path=_DATABASE_PATH) -> None:
        self.database_path = database_path

        self.base_topics = {
            _UNIVERSAL_SCOPE: "Universal",
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

    def set_association(
        self,
        map_identifier: int,
        association: Association,
        ontology_mode: OntologyMode = OntologyMode.STRICT,
    ) -> None:
        pass

    # ========== ATTRIBUTE ==========

    def attribute_exists(self, map_identifier: int, entity_identifier: str, name: str) -> bool:
        result = False

        connection = sqlite3.connect(self.database_path)
        cursor = connection.cursor()
        try:
            cursor.execute(
                "SELECT identifier FROM attribute WHERE map_identifier = ? AND entity_identifier = ? AND name = ?",
                (map_identifier, entity_identifier, name),
            )
            record = cursor.fetchone()
            if record:
                result = True
        except sqlite3.Error as error:
            raise TopicDbError(f"Error confirming the existence of an attribute: {error}")
        finally:
            cursor.close()
            connection.close()
        return result

    def delete_attribute(self, map_identifier: int, identifier: str) -> None:
        connection = sqlite3.connect(self.database_path)
        try:
            with connection:
                connection.execute(
                    "DELETE FROM attribute WHERE map_identifier = ? AND identifier = ?",
                    (map_identifier, identifier),
                )
        except sqlite3.Error as error:
            raise TopicDbError(f"Error deleting the attribute: {error}")
        finally:
            connection.close()

    def delete_attributes(self, map_identifier: int, entity_identifier: str) -> None:
        connection = sqlite3.connect(self.database_path)
        try:
            with connection:
                connection.execute(
                    "DELETE FROM attribute WHERE map_identifier = ? AND entity_identifier = ?",
                    (map_identifier, entity_identifier),
                )
        except sqlite3.Error as error:
            raise TopicDbError(f"Error deleting the attributes: {error}")
        finally:
            connection.close()

    def get_attribute(self, map_identifier: int, identifier: str) -> Optional[Attribute]:
        result = None

        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        try:
            cursor.execute(
                "SELECT * FROM attribute WHERE map_identifier = ? AND identifier = ?",
                (map_identifier, identifier),
            )
            record = cursor.fetchone()
            if record:
                result = Attribute(
                    record["name"],
                    record["value"],
                    record["entity_identifier"],
                    record["identifier"],
                    DataType[record["data_type"].upper()],
                    record["scope"],
                    Language[record["language"].upper()],
                )
        except sqlite3.Error as error:
            raise TopicDbError(f"Error getting an attribute: {error}")
        finally:
            cursor.close()
            connection.close()
        return result

    def get_attributes(
        self,
        map_identifier: int,
        entity_identifier: str,
        scope: str = None,
        language: Language = None,
    ) -> List[Attribute]:
        result = []

        if scope:
            if language:
                sql = """SELECT * FROM attribute
                    WHERE map_identifier = ? AND
                    entity_identifier = ? AND
                    scope = ? AND
                    language = ?"""
                bind_variables = (
                    map_identifier,
                    entity_identifier,
                    scope,
                    language.name.lower(),
                )
            else:
                sql = """SELECT * FROM attribute
                    WHERE map_identifier = ? AND
                    entity_identifier = ? AND
                    scope = ?"""
                bind_variables = (map_identifier, entity_identifier, scope)
        else:
            if language:
                sql = """SELECT * FROM attribute
                    WHERE map_identifier = ? AND
                    entity_identifier = ? AND
                    language = ?"""
                bind_variables = (
                    map_identifier,
                    entity_identifier,
                    language.name.lower(),
                )
            else:
                sql = """SELECT * FROM attribute
                    WHERE map_identifier = ? AND
                    entity_identifier = ?"""
                bind_variables = (map_identifier, entity_identifier)

        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        try:
            cursor.execute(sql, bind_variables)
            records = cursor.fetchall()
            for record in records:
                attribute = Attribute(
                    record["name"],
                    record["value"],
                    record["entity_identifier"],
                    record["identifier"],
                    DataType[record["data_type"].upper()],
                    record["scope"],
                    Language[record["language"].upper()],
                )
                result.append(attribute)
        except sqlite3.Error as error:
            raise TopicDbError(f"Error getting the attributes: {error}")
        finally:
            cursor.close()
            connection.close()
        return

    def set_attribute(
        self,
        map_identifier: int,
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
                    "INSERT INTO attribute (map_identifier, identifier, entity_identifier, name, value, data_type, scope, language) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        map_identifier,
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
            raise TopicDbError(f"Error creating the attribute: {error}")
        finally:
            connection.close()

    def set_attributes(self, map_identifier: int, attributes: List[Attribute]) -> None:
        for attribute in attributes:
            self.set_attribute(map_identifier, attribute)

    def update_attribute_value(self, map_identifier: int, identifier: str, value: str) -> None:
        connection = sqlite3.connect(self.database_path)
        try:
            with connection:
                connection.execute(
                    "UPDATE attribute SET value = ? WHERE map_identifier = ? AND identifier = ?",
                    (value, map_identifier, identifier),
                )
        except sqlite3.Error as error:
            raise TopicDbError(f"Error updating the attribute: {error}")
        finally:
            connection.close()

    # ========== OCCURRENCE ==========

    def delete_occurrence(self, map_identifier: int, identifier: str) -> None:
        connection = sqlite3.connect(self.database_path)
        try:
            with connection:
                connection.execute(
                    "DELETE FROM occurrence WHERE map_identifier = ? AND identifier = ?",
                    (map_identifier, identifier),
                )
        except sqlite3.Error as error:
            raise TopicDbError(f"Error deleting the occurrence: {error}")
        finally:
            connection.close()
        self.delete_attributes(map_identifier, identifier)

    def delete_occurrences(self, map_identifier: int, topic_identifier: str) -> None:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        try:
            cursor.execute(
                "SELECT identifier FROM occurrence WHERE map_identifier = ? AND topic_identifier = ?",
                (map_identifier, topic_identifier),
            )
            records = cursor.fetchall()
        except sqlite3.Error as error:
            raise TopicDbError(f"Error deleting the occurrences: {error}")
        finally:
            cursor.close()
            connection.close()
        for record in records:
            self.delete_occurrence(map_identifier, record["identifier"])

    def get_occurrence(
        self,
        map_identifier: int,
        identifier: str,
        inline_resource_data: RetrievalMode = RetrievalMode.DONT_INLINE_RESOURCE_DATA,
        resolve_attributes: RetrievalMode = RetrievalMode.DONT_RESOLVE_ATTRIBUTES,
    ) -> Optional[Occurrence]:
        result = None

        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        try:
            connection.execute(
                "SELECT identifier, instance_of, scope, resource_ref, topic_identifier, language FROM occurrence WHERE map_identifier = ? AND identifier = ?",
                (map_identifier, identifier),
            )
            record = cursor.fetchone()
            if record:
                resource_data = None
                if inline_resource_data is RetrievalMode.INLINE_RESOURCE_DATA:
                    resource_data = self.get_occurrence_data(map_identifier, identifier=identifier)
                result = Occurrence(
                    record["identifier"],
                    record["instance_of"],
                    record["topic_identifier"],
                    record["scope"],
                    record["resource_ref"],
                    resource_data,  # Type: bytes
                    Language[record["language"].upper()],
                )
                if resolve_attributes is RetrievalMode.RESOLVE_ATTRIBUTES:
                    result.add_attributes(self.get_attributes(map_identifier, identifier))
        except sqlite3.Error as error:
            raise TopicDbError(f"Error getting the occurrence data: {error}")
        finally:
            cursor.close()
            connection.close()
        return result

    def get_occurrence_data(self, map_identifier: int, identifier: str) -> Optional[bytes]:
        result = None

        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        try:
            cursor.execute(
                "SELECT resource_data FROM occurrence WHERE map_identifier = ? AND identifier = ?",
                (map_identifier, identifier),
            )
            record = cursor.fetchone()
            if record:
                if record["resource_data"] is not None:
                    result = record["resource_data"]  # Type: bytes
        except sqlite3.Error as error:
            raise TopicDbError(f"Error getting the occurrence data: {error}")
        finally:
            cursor.close()
            connection.close()
        return result

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
        result = []

        sql = """SELECT * FROM occurrence
            WHERE map_identifier = ?
            {0}
            ORDER BY topic_identifier, identifier
            LIMIT ? OFFSET ?"""
        if instance_of:
            if scope:
                if language:
                    query_filter = " AND instance_of = ? AND scope = ? AND language = ?"
                    bind_variables = (
                        map_identifier,
                        instance_of,
                        scope,
                        language.name.lower(),
                        limit,
                        offset,
                    )
                else:
                    query_filter = " AND instance_of = ? AND scope = ?"
                    bind_variables = (map_identifier, instance_of, scope, limit, offset)
            else:
                if language:
                    query_filter = " AND instance_of = ? AND language = ?"
                    bind_variables = (
                        map_identifier,
                        instance_of,
                        language.name.lower(),
                        limit,
                        offset,
                    )
                else:
                    query_filter = " AND instance_of = ?"
                    bind_variables = (map_identifier, instance_of, limit, offset)
        else:
            if scope:
                if language:
                    query_filter = " AND scope = ? AND language = ?"
                    bind_variables = (
                        map_identifier,
                        scope,
                        language.name.lower(),
                        limit,
                        offset,
                    )
                else:
                    query_filter = " AND scope = ?"
                    bind_variables = (map_identifier, scope, limit, offset)
            else:
                if language:
                    query_filter = " AND language = ?"
                    bind_variables = (
                        map_identifier,
                        language.name.lower(),
                        limit,
                        offset,
                    )
                else:
                    query_filter = ""
                    bind_variables = (map_identifier, limit, offset)

        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        try:
            cursor.execute(sql.format(query_filter), bind_variables)
            records = cursor.fetchall()
            for record in records:
                resource_data = None
                if inline_resource_data is RetrievalMode.INLINE_RESOURCE_DATA:
                    resource_data = self.get_occurrence_data(map_identifier, identifier=record["identifier"])
                occurrence = Occurrence(
                    record["identifier"],
                    record["instance_of"],
                    record["topic_identifier"],
                    record["scope"],
                    record["resource_ref"],
                    resource_data,  # Type: bytes
                    Language[record["language"].upper()],
                )
                if resolve_attributes is RetrievalMode.RESOLVE_ATTRIBUTES:
                    occurrence.add_attributes(self.get_attributes(map_identifier, occurrence.identifier))
                result.append(occurrence)
        except sqlite3.Error as error:
            raise TopicDbError(f"Error getting the occurrences: {error}")
        finally:
            cursor.close()
            connection.close()
        return result

    def occurrence_exists(self, map_identifier: int, identifier: str) -> bool:
        result = False

        connection = sqlite3.connect(self.database_path)
        cursor = connection.cursor()
        try:
            cursor.execute(
                "SELECT identifier FROM occurrence WHERE map_identifier = ? AND identifier = ?",
                (map_identifier, identifier),
            )
            record = cursor.fetchone()
            if record:
                result = True
        except sqlite3.Error as error:
            raise TopicDbError(f"Error confirming existence of occurrence: {error}")
        finally:
            cursor.close()
            connection.close()
        return result

    def set_occurrence(
        self,
        map_identifier: int,
        occurrence: Occurrence,
        ontology_mode: OntologyMode = OntologyMode.STRICT,
    ) -> None:
        if occurrence.topic_identifier == "":
            raise TopicDbError("Occurrence has an empty 'topic identifier' property")

        if ontology_mode is OntologyMode.STRICT:
            instance_of_exists = self.topic_exists(map_identifier, occurrence.instance_of)
            if not instance_of_exists:
                raise TopicDbError("Ontology 'STRICT' mode violation: 'instance Of' topic does not exist")

            scope_exists = self.topic_exists(map_identifier, occurrence.scope)
            if not scope_exists:
                raise TopicDbError("Ontology 'STRICT' mode violation: 'scope' topic does not exist")

        connection = sqlite3.connect(self.database_path)
        try:
            with connection:
                resource_data = None
                if occurrence.resource_data is not None:
                    resource_data = (
                        occurrence.resource_data
                        if isinstance(occurrence.resource_data, bytes)
                        else bytes(occurrence.resource_data, encoding="utf-8")
                    )
                connection.execute(
                    "INSERT INTO occurrence (map_identifier, identifier, instance_of, scope, resource_ref, resource_data, topic_identifier, language) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        map_identifier,
                        occurrence.identifier,
                        occurrence.instance_of,
                        occurrence.scope,
                        occurrence.resource_ref,
                        resource_data,  # Type: bytes
                        occurrence.topic_identifier,
                        occurrence.language.name.lower(),
                    ),
                )
            if not occurrence.get_attribute_by_name("creation-timestamp"):
                timestamp = str(datetime.now())
                timestamp_attribute = Attribute(
                    "creation-timestamp",
                    timestamp,
                    occurrence.identifier,
                    data_type=DataType.TIMESTAMP,
                    scope=_UNIVERSAL_SCOPE,
                    language=Language.ENG,
                )
                occurrence.add_attribute(timestamp_attribute)
        except sqlite3.Error as error:
            raise TopicDbError(f"Error creating the occurrence: {error}")
        finally:
            connection.close()
        self.set_attributes(map_identifier, occurrence.attributes)

    def update_occurrence_data(self, map_identifier: int, identifier: str, resource_data: Union[str, bytes]) -> None:
        resource_data = resource_data if isinstance(resource_data, bytes) else bytes(resource_data, encoding="utf-8")

        connection = sqlite3.connect(self.database_path)
        try:
            with connection:
                connection.execute(
                    "UPDATE occurrence SET resource_data = ? WHERE map_identifier = ? AND identifier = ?",
                    (resource_data, map_identifier, identifier),
                )
        except sqlite3.Error as error:
            raise TopicDbError(f"Error updating the occurrence data: {error}")
        finally:
            connection.close()

    def update_occurrence_scope(self, map_identifier: int, identifier: str, scope: str) -> None:
        connection = sqlite3.connect(self.database_path)
        try:
            with connection:
                connection.execute(
                    "UPDATE occurrence SET scope = ? WHERE map_identifier = ? AND identifier = ?",
                    (scope, map_identifier, identifier),
                )
        except sqlite3.Error as error:
            raise TopicDbError(f"Error updating the occurrence scope: {error}")
        finally:
            connection.close()

    def update_occurrence_topic_identifier(self, map_identifier: int, identifier: str, topic_identifier: str) -> None:
        connection = sqlite3.connect(self.database_path)
        try:
            with connection:
                connection.execute(
                    "UPDATE occurrence SET topic_identifier = ? WHERE map_identifier = ? AND identifier = ?",
                    (topic_identifier, map_identifier, identifier),
                )
        except sqlite3.Error as error:
            raise TopicDbError(f"Error updating the occurrence topic identifier: {error}")
        finally:
            connection.close()

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
        self,
        map_identifier: int,
        offset: int = 0,
        limit: int = 100,
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
        result = []

        sql = """SELECT identifier, instance_of, scope, resource_ref, topic_identifier, language
            FROM occurrence
            WHERE map_identifier = ? AND
            topic_identifier = ?
            {0}
            ORDER BY instance_of, scope, language"""
        if instance_of:
            if scope:
                if language:
                    query_filter = " AND instance_of = ? AND scope = ? AND language = ?"
                    bind_variables = (
                        map_identifier,
                        identifier,
                        instance_of,
                        scope,
                        language.name.lower(),
                    )
                else:
                    query_filter = " AND instance_of = ? AND scope = ?"
                    bind_variables = (map_identifier, identifier, instance_of, scope)
            else:
                if language:
                    query_filter = " AND instance_of = ? AND language = ?"
                    bind_variables = (
                        map_identifier,
                        identifier,
                        instance_of,
                        language.name.lower(),
                    )
                else:
                    query_filter = " AND instance_of = ?"
                    bind_variables = (map_identifier, identifier, instance_of)
        else:
            if scope:
                if language:
                    query_filter = " AND scope = ? AND language = ?"
                    bind_variables = (
                        map_identifier,
                        identifier,
                        scope,
                        language.name.lower(),
                    )
                else:
                    query_filter = " AND scope = ?"
                    bind_variables = (map_identifier, identifier, scope)
            else:
                if language:
                    query_filter = " AND language = ?"
                    bind_variables = (map_identifier, identifier, language.name.lower())
                else:
                    query_filter = ""
                    bind_variables = (map_identifier, identifier)

        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        try:
            cursor.execute(sql.format(query_filter), bind_variables)
            records = cursor.fetchall()
            for record in records:
                resource_data = None
                if inline_resource_data is RetrievalMode.INLINE_RESOURCE_DATA:
                    resource_data = self.get_occurrence_data(map_identifier, record["identifier"])
                occurrence = Occurrence(
                    record["identifier"],
                    record["instance_of"],
                    record["topic_identifier"],
                    record["scope"],
                    record["resource_ref"],
                    resource_data,
                    Language[record["language"].upper()],
                )
                if resolve_attributes is RetrievalMode.RESOLVE_ATTRIBUTES:
                    occurrence.add_attributes(self.get_attributes(map_identifier, occurrence.identifier))
                result.append(occurrence)
        except sqlite3.Error as error:
            raise TopicDbError(f"Error getting the topic occurrences: {error}")
        finally:
            cursor.close()
            connection.close()
        return result

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
        if ontology_mode is OntologyMode.STRICT:
            instance_of_exists = self.topic_exists(topic.instance_of)
            if not instance_of_exists:
                raise TopicDbError("Ontology 'STRICT' mode violation: 'instance Of' topic does not exist")

        connection = sqlite3.connect(self.database_path)
        try:
            with connection:
                connection.execute(
                    "INSERT INTO topic (map_identifier, identifier, instance_of) VALUES (?, ?, ?)",
                    (map_identifier, topic.identifier, topic.instance_of),
                )
                for base_name in topic.base_names:
                    connection.execute(
                        "INSERT INTO basename (map_identifier, identifier, name, topic_identifier, scope, language) VALUES (?, ?, ?, ?, ?, ?)",
                        (
                            map_identifier,
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
                    scope=_UNIVERSAL_SCOPE,
                    language=Language.ENG,
                )
                topic.add_attribute(timestamp_attribute)
        except sqlite3.Error as error:
            raise TopicDbError(f"Error creating the topic: {error}")
        finally:
            connection.close()
        self.set_attributes(map_identifier, topic.attributes)

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
        result = False

        connection = sqlite3.connect(self.database_path)
        cursor = connection.cursor()
        try:
            cursor.execute(
                "SELECT identifier FROM topic WHERE map_identifier = ? AND identifier = ?", (map_identifier, identifier)
            )
            record = cursor.fetchone()
            if record:
                result = True
        except sqlite3.Error as error:
            raise TopicDbError(f"Error confirming existence of the topic: {error}")
        finally:
            cursor.close()
            connection.close()

        return result

    def is_topic(self, map_identifier: int, identifier: str) -> bool:
        pass

    # ========== DATABASE ==========

    def create_database(self):
        statements = _DDL.split(";")

        connection = sqlite3.connect(self.database_path)
        try:
            with connection:
                for statement in statements:
                    connection.execute(statement)
        except sqlite3.Error as error:
            raise TopicDbError(f"Error creating the database: {error}")
        finally:
            connection.close()

    # ========== TOPIC MAP ==========

    def populate_map(self, map_identifier: int, user_identifier: int) -> None:
        map = self.get_map(map_identifier, user_identifier)

        if map and not map.initialised and not self.topic_exists(map_identifier, "home"):
            for k, v in self.base_topics.items():
                topic = Topic(
                    identifier=k,
                    instance_of="base-topic",
                    name=v,
                )
                self.set_topic(map_identifier, topic, OntologyMode.LENIENT)

    def delete_map(self, map_identifier: int, user_identifier: int) -> None:
        connection = sqlite3.connect(self.database_path)
        cursor = connection.cursor()
        try:
            with connection:
                cursor.execute(
                    "SELECT * FROM user_map WHERE user_identifier = ? AND map_identifier = ? AND owner = 1",  # 1 = True
                    (user_identifier, map_identifier),
                )
                record = cursor.fetchone()
                if record:
                    connection.execute("DELETE FROM user_map WHERE map_identifier = ?", (map_identifier,))
                    connection.execute("DELETE FROM map WHERE identifier = ?", (map_identifier,))
                    connection.execute("DELETE FROM attribute WHERE map_identifier = ?", (map_identifier,))
                    connection.execute("DELETE FROM occurrence WHERE map_identifier = ?", (map_identifier,))
                    connection.execute("DELETE FROM member WHERE map_identifier = ?", (map_identifier,))
                    connection.execute("DELETE FROM basename WHERE map_identifier = ?", (map_identifier,))
                    connection.execute("DELETE FROM topic WHERE map_identifier = ?", (map_identifier,))
        except sqlite3.Error as error:
            raise TopicDbError(f"Error deleting the map: {error}")
        finally:
            cursor.close()
            connection.close()

    def get_map(self, map_identifier: int, user_identifier: int = None) -> Optional[Map]:
        result = None

        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        if user_identifier:
            sql = """SELECT
                map.identifier AS map_identifier,
                map.name AS name,
                map.description AS description,
                map.image_path AS image_path,
                map.initialised AS initialised,
                map.published AS published,
                map.promoted AS promoted,
                user_map.user_identifier AS user_identifier,
                user_map.owner AS owner,
                user_map.collaboration_mode AS collaboration_mode
                FROM map
                INNER JOIN user_map ON map.identifier = user_map.map_identifier
                WHERE user_map.user_identifier = ?
                AND map.identifier = ?
                ORDER BY map_identifier"""
            try:
                cursor.execute(sql, (user_identifier, map_identifier))
                record = cursor.fetchone()
                if record:
                    result = Map(
                        record["map_identifier"],
                        record["name"],
                        user_identifier=record["user_identifier"],
                        description=record["description"],
                        image_path=record["image_path"],
                        initialised=record["initialised"],
                        published=record["published"],
                        promoted=record["promoted"],
                        owner=record["owner"],
                        collaboration_mode=CollaborationMode[record["collaboration_mode"].upper()],
                    )
            except sqlite3.Error as error:
                raise TopicDbError(f"Error retrieving the map: {error}")
            finally:
                cursor.close()
                connection.close()
        else:
            try:
                cursor.execute("SELECT * FROM map WHERE identifier = ?", (map_identifier,))
                record = cursor.fetchone()
                if record:
                    result = Map(
                        record["identifier"],
                        record["name"],
                        user_identifier=None,
                        description=record["description"],
                        image_path=record["image_path"],
                        initialised=record["initialised"],
                        published=record["published"],
                        promoted=record["promoted"],
                        owner=None,
                        collaboration_mode=None,
                    )
            except sqlite3.Error as error:
                raise TopicDbError(f"Error retrieving the topic map: {error}")
            finally:
                cursor.close()
                connection.close()
        return result

    def get_maps(self, user_identifier: int) -> List[Map]:
        result = []

        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        sql = """SELECT
            map.identifier AS map_identifier,
            map.name AS name,
            map.description AS description,
            map.image_path AS image_path,
            map.initialised AS initialised,
            map.published AS published,
            map.promoted AS promoted,
            user_map.user_identifier AS user_identifier,
            user_map.owner AS owner,
            user_map.collaboration_mode AS collaboration_mode
            FROM map
            INNER JOIN user_map ON map.identifier = user_map.map_identifier
            WHERE user_map.user_identifier = ?
            ORDER BY map_identifier"""
        try:
            cursor.execute(sql, (user_identifier,))
            records = cursor.fetchall()
            for record in records:
                map = Map(
                    record["map_identifier"],
                    record["name"],
                    user_identifier=record["user_identifier"],
                    description=record["description"],
                    image_path=record["image_path"],
                    initialised=record["initialised"],
                    published=record["published"],
                    promoted=record["promoted"],
                    owner=record["owner"],
                    collaboration_mode=CollaborationMode[record["collaboration_mode"].upper()],
                )
                result.append(map)
        except sqlite3.Error as error:
            raise TopicDbError(f"Error retrieving the maps: {error}")
        finally:
            cursor.close()
            connection.close()
        return result

    def set_map(
        self,
        user_identifier: int,
        name: str,
        description: str = "",
        image_path: str = "",
        initialised: bool = False,
        published: bool = False,
        promoted: bool = False,
    ) -> int:
        result = -1

        connection = sqlite3.connect(self.database_path)
        cursor = connection.cursor()
        try:
            with connection:
                connection.execute(
                    "INSERT INTO map (name, description, image_path, initialised, published, promoted) VALUES (?, ?, ?, ?, ?, ?)",
                    (
                        name,
                        description,
                        image_path,
                        initialised,
                        published,
                        promoted,
                    ),
                )
                cursor.execute("SELECT seq from sqlite_sequence WHERE name = 'map'")
                result = cursor.fetchone()[0]
                connection.execute(
                    "INSERT INTO user_map (user_identifier, map_identifier, owner, collaboration_mode) VALUES (?, ?, ?, ?)",
                    (user_identifier, result, 1, CollaborationMode.EDIT.name.lower()),  # 1 = True
                )
        except sqlite3.Error as error:
            raise TopicDbError(f"Error creating the map: {error}")
        finally:
            cursor.close()
            connection.close()
        return result

    def update_map(
        self,
        map_identifier: int,
        name: str,
        description: str = "",
        image_path: str = "",
        initialised: bool = True,
        published: bool = False,
        promoted: bool = False,
    ) -> None:
        connection = sqlite3.connect(self.database_path)
        try:
            with connection:
                connection.execute(
                    "UPDATE map SET name = ?, description = ?, image_path = ?, initialised = ?, published = ?, promoted = ? WHERE identifier = ?",
                    (
                        name,
                        description,
                        image_path,
                        initialised,
                        published,
                        promoted,
                        map_identifier,
                    ),
                )
        except sqlite3.Error as error:
            raise TopicDbError(f"Error updating the map: {error}")
        finally:
            connection.close()

    def get_published_maps(self) -> List[Map]:
        result = []

        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT * FROM map WHERE published = 1 ORDER BY identifier")  # 1 = True
            records = cursor.fetchall()
            for record in records:
                map = Map(
                    record["identifier"],
                    record["name"],
                    user_identifier=None,
                    description=record["description"],
                    image_path=record["image_path"],
                    initialised=record["initialised"],
                    published=record["published"],
                    promoted=record["promoted"],
                    owner=None,
                    collaboration_mode=None,
                )
                result.append(map)
        except sqlite3.Error as error:
            raise TopicDbError(f"Error getting the published maps: {error}")
        finally:
            cursor.close()
            connection.close()
        return result

    def get_promoted_maps(self) -> List[Map]:
        result = []

        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT * FROM map WHERE promoted = 1 ORDER BY identifier")  # 1 = True
            records = cursor.fetchall()
            for record in records:
                map = Map(
                    record["identifier"],
                    record["name"],
                    user_identifier=None,
                    description=record["description"],
                    image_path=record["image_path"],
                    initialised=record["initialised"],
                    published=record["published"],
                    promoted=record["promoted"],
                    owner=None,
                    collaboration_mode=None,
                )
                result.append(map)
        except sqlite3.Error as error:
            raise TopicDbError(f"Error getting the promoted maps: {error}")
        finally:
            cursor.close()
            connection.close()
        return result

    def is_map_owner(self, map_identifier: int, user_identifier: int) -> bool:
        result = False

        connection = sqlite3.connect(self.database_path)
        cursor = connection.cursor()
        try:
            cursor.execute(
                "SELECT * FROM user_map WHERE user_identifier = ? AND map_identifier = ? AND owner = 1",  # 1 = True
                (user_identifier, map_identifier),
            )
            record = cursor.fetchone()
            if record:
                result = True
        except sqlite3.Error as error:
            raise TopicDbError(f"Error confirming owner of the map: {error}")
        finally:
            cursor.close()
            connection.close()
        return result

    # ========== COLLABORATION ==========

    def collaborate(
        self,
        map_identifier: int,
        user_identifier: int,
        collaboration_mode: CollaborationMode = CollaborationMode.VIEW,
    ) -> None:
        pass

    def stop_collaboration(self, map_identifier: int, user_identifier: int) -> None:
        pass

    def get_collaboration_mode(self, map_identifier: int, user_identifier: int) -> Optional[CollaborationMode]:
        pass

    def update_collaboration_mode(
        self,
        map_identifier: int,
        user_identifier: int,
        collaboration_mode: CollaborationMode,
    ) -> None:
        pass

    def get_collaborators(self, map_identifier: int) -> List[Collaborator]:
        pass

    def get_collaborator(self, map_identifier: int, user_identifier: int) -> Optional[Collaborator]:
        pass

    # ========== STATISTICS ==========

    def get_topic_occurrences_statistics(self, map_identifier: int, identifier: str, scope: str = None) -> Dict:
        pass
