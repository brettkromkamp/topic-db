"""
TopicStore class. Part of the StoryTechnologies project.

February 24, 2017
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

from __future__ import annotations

from collections import namedtuple
from datetime import datetime
from typing import Optional, List, Union, Dict, Tuple

import psycopg2  # type: ignore
import psycopg2.extras  # type: ignore
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
from topicdb.core.models.topicmap import TopicMap
from topicdb.core.store.retrievalmode import RetrievalMode
from topicdb.core.store.taxonomymode import TaxonomyMode
from topicdb.core.store.topicfield import TopicField
from topicdb.core.topicdberror import TopicDbError

TopicRefs = namedtuple("TopicRefs", ["instance_of", "role_spec", "topic_ref"])


class TopicStore:
    def __init__(
        self,
        username: str,
        password: str,
        host: str = "localhost",
        port: int = 5432,
        dbname: str = "storytech",
    ) -> None:
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.dbname = dbname

        self.connection = None

        self.base_topics = {
            ("*", "Universal"),  # Universal scope (context)
            ("home", "Home"),
            ("entity", "Entity"),
            ("topic", "Topic"),
            ("association", "Association"),
            ("occurrence", "Occurrence"),
            ("navigation", "Navigation"),
            ("member", "Member"),
            ("category", "Category"),
            ("categorization", "Categorization"),
            ("tag", "Tag"),
            ("tags", "Tags"),
            ("note", "Note"),
            ("notes", "Notes"),
            ("broader", "Broader"),
            ("narrower", "Narrower"),
            ("related", "Related"),
            ("parent", "Parent"),
            ("child", "Child"),
            ("previous", "Previous"),
            ("next", "Next"),
            ("up", "Up"),
            ("down", "Down"),
            ("image", "Image"),
            ("video", "Video"),
            ("audio", "Audio"),
            ("note", "Note"),
            ("file", "File"),
            ("url", "URL"),
            ("text", "Text"),
            ("3d-scene", "3D Scene"),
            ("string", "String"),
            ("number", "Number"),
            ("timestamp", "Timestamp"),
            ("boolean", "Boolean"),
            ("eng", "English Language"),
            ("spa", "Spanish Language"),
            ("nld", "Dutch Language"),
        }

    def open(self) -> TopicStore:
        self.connection = psycopg2.connect(
            dbname=self.dbname,
            user=self.username,
            password=self.password,
            host=self.host,
            port=self.port,
        )
        return self

    def close(self) -> None:
        if self.connection:
            self.connection.close()

    # Context manager methods
    def __enter__(self) -> TopicStore:
        return self.open()

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    # ========== ASSOCIATION ==========

    def delete_association(self, map_identifier: int, identifier: str) -> None:
        # http://initd.org/psycopg/docs/usage.html#with-statement
        with self.connection, self.connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor
        ) as cursor:
            # Delete topic/association record
            cursor.execute(
                "DELETE FROM topicdb.topic WHERE topicmap_identifier = %s AND identifier = %s AND scope IS NOT NULL",
                (map_identifier, identifier),
            )

            # Delete base name record(s)
            cursor.execute(
                "DELETE FROM topicdb.basename WHERE topicmap_identifier = %s AND topic_identifier = %s",
                (map_identifier, identifier),
            )

            # Get members
            cursor.execute(
                "SELECT identifier FROM topicdb.member WHERE topicmap_identifier = %s AND association_identifier = %s",
                (map_identifier, identifier),
            )
            member_records = cursor.fetchall()

            # Delete members
            cursor.execute(
                "DELETE FROM topicdb.member WHERE topicmap_identifier = %s AND association_identifier = %s",
                (map_identifier, identifier),
            )
            if member_records:
                for member_record in member_records:
                    # Delete topic refs
                    cursor.execute(
                        "DELETE FROM topicdb.topicref WHERE topicmap_identifier = %s AND member_identifier = %s",
                        (map_identifier, member_record["identifier"]),
                    )
        # Delete attributes
        self.delete_attributes(map_identifier, identifier)

    def get_association(
        self,
        map_identifier: int,
        identifier: str,
        language: Language = None,
        resolve_attributes: RetrievalMode = RetrievalMode.DONT_RESOLVE_ATTRIBUTES,
        resolve_occurrences: RetrievalMode = RetrievalMode.DONT_RESOLVE_OCCURRENCES,
    ) -> Optional[Association]:
        result = None

        with self.connection, self.connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor
        ) as cursor:
            cursor.execute(
                "SELECT identifier, instance_of, scope FROM topicdb.topic WHERE topicmap_identifier = %s AND identifier = %s AND scope IS NOT NULL",
                (map_identifier, identifier),
            )
            association_record = cursor.fetchone()
            if association_record:
                result = Association(
                    identifier=association_record["identifier"],
                    instance_of=association_record["instance_of"],
                    scope=association_record["scope"],
                )
                result.clear_base_names()
                if language:
                    sql = """SELECT name, language, identifier 
                    FROM topicdb.basename
                    WHERE topicmap_identifier = %s AND 
                    topic_identifier = %s AND
                    language = %s"""
                    bind_variables = (map_identifier, identifier, language.name.lower())
                else:
                    sql = """SELECT name, language, identifier
                    FROM topicdb.basename
                    WHERE topicmap_identifier = %s AND
                    topic_identifier = %s"""
                    bind_variables = (map_identifier, identifier)
                cursor.execute(sql, bind_variables)
                base_name_records = cursor.fetchall()
                if base_name_records:
                    for base_name_record in base_name_records:
                        result.add_base_name(
                            BaseName(
                                base_name_record["name"],
                                Language[base_name_record["language"].upper()],
                                base_name_record["identifier"],
                            )
                        )
                cursor.execute(
                    "SELECT * FROM topicdb.member WHERE topicmap_identifier = %s AND association_identifier = %s",
                    (map_identifier, identifier),
                )
                member_records = cursor.fetchall()
                if member_records:
                    for member_record in member_records:
                        role_spec = member_record["role_spec"]
                        cursor.execute(
                            "SELECT * FROM topicdb.topicref WHERE topicmap_identifier = %s AND member_identifier = %s",
                            (map_identifier, member_record["identifier"]),
                        )
                        topic_ref_records = cursor.fetchall()
                        if topic_ref_records:
                            member = Member(
                                role_spec=role_spec,
                                identifier=member_record["identifier"],
                            )
                            for topic_ref_record in topic_ref_records:
                                member.add_topic_ref(topic_ref_record["topic_ref"])
                            result.add_member(member)
                if resolve_attributes is RetrievalMode.RESOLVE_ATTRIBUTES:
                    result.add_attributes(
                        self.get_attributes(map_identifier, identifier)
                    )
                if resolve_occurrences is RetrievalMode.RESOLVE_OCCURRENCES:
                    result.add_occurrences(
                        self.get_topic_occurrences(map_identifier, identifier)
                    )

        return result

    def get_association_groups(
        self,
        map_identifier: int,
        identifier: str = "",
        associations: Optional[List[Association]] = None,
        instance_ofs: Optional[List[str]] = None,
        scope: str = None,
    ) -> DoubleKeyDict:
        if identifier == "" and associations is None:
            raise TopicDbError(
                "At least one of the 'identifier' or 'associations' parameters is required"
            )

        result = DoubleKeyDict()

        if not associations:
            associations = self.get_topic_associations(
                map_identifier, identifier, instance_ofs=instance_ofs, scope=scope
            )

        for association in associations:
            resolved_topic_refs = self._resolve_topic_refs(association)
            for resolved_topic_ref in resolved_topic_refs:
                instance_of = resolved_topic_ref.instance_of
                role_spec = resolved_topic_ref.role_spec
                topic_ref = resolved_topic_ref.topic_ref
                if topic_ref != identifier:
                    if [instance_of, role_spec] in result:
                        topic_refs = result[instance_of, role_spec]
                        if topic_ref not in topic_refs:
                            topic_refs.append(topic_ref)
                        result[instance_of, role_spec] = topic_refs
                    else:
                        result[instance_of, role_spec] = [topic_ref]
        return result

    @staticmethod
    def _resolve_topic_refs(association: Association) -> List[TopicRefs]:
        result: List[TopicRefs] = []

        for member in association.members:
            for topic_ref in member.topic_refs:
                result.append(
                    TopicRefs(association.instance_of, member.role_spec, topic_ref)
                )
        return result

    def get_associations(self):
        pass

    def set_association(
        self,
        map_identifier: int,
        association: Association,
        taxonomy_mode: TaxonomyMode = TaxonomyMode.STRICT,
    ) -> None:
        if taxonomy_mode is TaxonomyMode.STRICT:
            instance_of_exists = self.topic_exists(
                map_identifier, association.instance_of
            )
            if not instance_of_exists:
                raise TopicDbError(
                    "Taxonomy 'STRICT' mode violation: 'instance Of' topic does not exist"
                )

            scope_exists = self.topic_exists(map_identifier, association.scope)
            if not scope_exists:
                raise TopicDbError(
                    "Taxonomy 'STRICT' mode violation: 'scope' topic does not exist"
                )

        with self.connection, self.connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO topicdb.topic (topicmap_identifier, identifier, INSTANCE_OF, scope) VALUES (%s, %s, %s, %s)",
                (
                    map_identifier,
                    association.identifier,
                    association.instance_of,
                    association.scope,
                ),
            )
            for base_name in association.base_names:
                cursor.execute(
                    "INSERT INTO topicdb.basename (topicmap_identifier, identifier, name, topic_identifier, language) VALUES (%s, %s, %s, %s, %s)",
                    (
                        map_identifier,
                        base_name.identifier,
                        base_name.name,
                        association.identifier,
                        base_name.language.name.lower(),
                    ),
                )
            for member in association.members:
                cursor.execute(
                    "INSERT INTO topicdb.member (topicmap_identifier, identifier, role_spec, association_identifier) VALUES (%s, %s, %s, %s)",
                    (
                        map_identifier,
                        member.identifier,
                        member.role_spec,
                        association.identifier,
                    ),
                )
                for topic_ref in member.topic_refs:
                    cursor.execute(
                        "INSERT INTO topicdb.topicref (topicmap_identifier, topic_ref, member_identifier) VALUES (%s, %s, %s)",
                        (map_identifier, topic_ref, member.identifier),
                    )

            if not association.get_attribute_by_name("creation-timestamp"):
                timestamp = str(datetime.now())
                timestamp_attribute = Attribute(
                    "creation-timestamp",
                    timestamp,
                    association.identifier,
                    data_type=DataType.TIMESTAMP,
                    scope="*",
                    language=Language.ENG,
                )
                association.add_attribute(timestamp_attribute)
        self.set_attributes(map_identifier, association.attributes)

    # ========== ATTRIBUTE ==========

    def attribute_exists(
        self, map_identifier: int, entity_identifier: str, name: str
    ) -> bool:
        result = False

        with self.connection, self.connection.cursor() as cursor:
            cursor.execute(
                "SELECT identifier FROM topicdb.attribute WHERE topicmap_identifier = %s AND parent_identifier = %s AND name = %s",
                (map_identifier, entity_identifier, name),
            )
            record = cursor.fetchone()
            if record:
                result = True
        return result

    def delete_attribute(self, map_identifier: int, identifier: str) -> None:
        with self.connection, self.connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM topicdb.attribute WHERE topicmap_identifier = %s AND identifier = %s",
                (map_identifier, identifier),
            )

    def delete_attributes(self, map_identifier: int, entity_identifier: str) -> None:
        with self.connection, self.connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM topicdb.attribute WHERE topicmap_identifier = %s AND parent_identifier = %s",
                (map_identifier, entity_identifier),
            )

    def get_attribute(
        self, map_identifier: int, identifier: str
    ) -> Optional[Attribute]:
        result = None

        with self.connection, self.connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor
        ) as cursor:
            cursor.execute(
                "SELECT * FROM topicdb.attribute WHERE topicmap_identifier = %s AND identifier = %s",
                (map_identifier, identifier),
            )
            record = cursor.fetchone()
            if record:
                result = Attribute(
                    record["name"],
                    record["value"],
                    record["parent_identifier"],
                    record["identifier"],
                    DataType[record["data_type"].upper()],
                    record["scope"],
                    Language[record["language"].upper()],
                )
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
                sql = """SELECT * FROM topicdb.attribute 
                WHERE topicmap_identifier = %s AND 
                parent_identifier = %s AND 
                scope = %s AND
                language = %s"""
                bind_variables = (
                    map_identifier,
                    entity_identifier,
                    scope,
                    language.name.lower(),
                )
            else:
                sql = """SELECT * FROM topicdb.attribute 
                WHERE topicmap_identifier = %s AND 
                parent_identifier = %s AND 
                scope = %s"""
                bind_variables = (map_identifier, entity_identifier, scope)
        else:
            if language:
                sql = """SELECT * FROM topicdb.attribute 
                WHERE topicmap_identifier = %s AND 
                parent_identifier = %s AND 
                language = %s"""
                bind_variables = (
                    map_identifier,
                    entity_identifier,
                    language.name.lower(),
                )
            else:
                sql = """SELECT * FROM topicdb.attribute 
                WHERE topicmap_identifier = %s AND
                parent_identifier = %s"""
                bind_variables = (map_identifier, entity_identifier)

        with self.connection, self.connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor
        ) as cursor:
            cursor.execute(sql, bind_variables)
            records = cursor.fetchall()
            for record in records:
                attribute = Attribute(
                    record["name"],
                    record["value"],
                    record["parent_identifier"],
                    record["identifier"],
                    DataType[record["data_type"].upper()],
                    record["scope"],
                    Language[record["language"].upper()],
                )
                result.append(attribute)
        return result

    def set_attribute(
        self,
        map_identifier: int,
        attribute: Attribute,
        taxonomy_mode: TaxonomyMode = TaxonomyMode.LENIENT,
    ) -> None:
        if attribute.entity_identifier == "":
            raise TopicDbError("Attribute has an empty 'entity identifier' property")

        if taxonomy_mode is TaxonomyMode.STRICT:
            scope_exists = self.topic_exists(map_identifier, attribute.scope)
            if not scope_exists:
                raise TopicDbError(
                    "Taxonomy 'STRICT' mode violation: 'scope' topic does not exist"
                )

        with self.connection, self.connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO topicdb.attribute (topicmap_identifier, identifier, parent_identifier, name, value, data_type, scope, language) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
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

    def set_attributes(self, map_identifier: int, attributes: List[Attribute]) -> None:
        for attribute in attributes:
            self.set_attribute(map_identifier, attribute)

    def update_attribute_value(
        self, map_identifier: int, identifier: str, value: str
    ) -> None:
        with self.connection, self.connection.cursor() as cursor:
            cursor.execute(
                "UPDATE topicdb.attribute SET value = %s WHERE topicmap_identifier = %s AND identifier = %s",
                (value, map_identifier, identifier),
            )

    # ========== OCCURRENCE ==========

    def delete_occurrence(self, map_identifier: int, identifier: str) -> None:
        with self.connection, self.connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM topicdb.occurrence WHERE topicmap_identifier = %s AND identifier = %s",
                (map_identifier, identifier),
            )
        # Delete attributes
        self.delete_attributes(map_identifier, identifier)

    def delete_occurrences(self, map_identifier: int, topic_identifier: str) -> None:
        with self.connection, self.connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor
        ) as cursor:
            cursor.execute(
                "SELECT identifier FROM topicdb.occurrence WHERE topicmap_identifier = %s AND topic_identifier = %s",
                (map_identifier, topic_identifier),
            )
            records = cursor.fetchall()
        # Delete attributes for all of the topic's occurrences
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

        with self.connection, self.connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor
        ) as cursor:
            cursor.execute(
                "SELECT identifier, instance_of, scope, resource_ref, topic_identifier, language FROM topicdb.occurrence WHERE topicmap_identifier = %s AND identifier = %s",
                (map_identifier, identifier),
            )
            record = cursor.fetchone()
            if record:
                resource_data = None
                if inline_resource_data is RetrievalMode.INLINE_RESOURCE_DATA:
                    resource_data = self.get_occurrence_data(
                        map_identifier, identifier=identifier
                    )
                result = Occurrence(
                    record["identifier"],
                    record["instance_of"],
                    record["topic_identifier"],
                    record["scope"],
                    record["resource_ref"],
                    resource_data,
                    Language[record["language"].upper()],
                )
                if resolve_attributes is RetrievalMode.RESOLVE_ATTRIBUTES:
                    result.add_attributes(
                        self.get_attributes(map_identifier, identifier)
                    )
        return result

    def get_occurrence_data(
        self, map_identifier: int, identifier: str
    ) -> Optional[bytes]:
        result = None

        with self.connection, self.connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor
        ) as cursor:
            cursor.execute(
                "SELECT resource_data FROM topicdb.occurrence WHERE topicmap_identifier = %s AND identifier = %s",
                (map_identifier, identifier),
            )
            record = cursor.fetchone()
            if record:
                # BYTEA field is returned as a 'memoryview' and needs to be converted to bytes
                if record["resource_data"] is not None:
                    result = bytes(record["resource_data"])
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
        sql = """SELECT * FROM topicdb.occurrence 
        WHERE topicmap_identifier = %s 
        {0} 
        ORDER BY topic_identifier, identifier 
        LIMIT %s OFFSET %s"""
        if instance_of:
            if scope:
                if language:
                    query_filter = (
                        " AND instance_of = %s AND scope = %s AND language = %s"
                    )
                    bind_variables = (
                        map_identifier,
                        instance_of,
                        scope,
                        language.name.lower(),
                        limit,
                        offset,
                    )
                else:
                    query_filter = " AND instance_of = %s AND scope = %s"
                    bind_variables = (map_identifier, instance_of, scope, limit, offset)
            else:
                if language:
                    query_filter = " AND instance_of = %s AND language = %s"
                    bind_variables = (
                        map_identifier,
                        instance_of,
                        language.name.lower(),
                        limit,
                        offset,
                    )
                else:
                    query_filter = " AND instance_of = %s"
                    bind_variables = (map_identifier, instance_of, limit, offset)
        else:
            if scope:
                if language:
                    query_filter = " AND scope = %s AND language = %s"
                    bind_variables = (
                        map_identifier,
                        scope,
                        language.name.lower(),
                        limit,
                        offset,
                    )
                else:
                    query_filter = " AND scope = %s"
                    bind_variables = (map_identifier, scope, limit, offset)
            else:
                if language:
                    query_filter = " AND language = %s"
                    bind_variables = (
                        map_identifier,
                        language.name.lower(),
                        limit,
                        offset,
                    )
                else:
                    query_filter = ""
                    bind_variables = (map_identifier, limit, offset)

        with self.connection, self.connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor
        ) as cursor:
            cursor.execute(sql.format(query_filter), bind_variables)
            records = cursor.fetchall()
            for record in records:
                resource_data = None
                if inline_resource_data is RetrievalMode.INLINE_RESOURCE_DATA:
                    resource_data = self.get_occurrence_data(
                        map_identifier, identifier=record["identifier"]
                    )
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
                    occurrence.add_attributes(
                        self.get_attributes(map_identifier, occurrence.identifier)
                    )
                result.append(occurrence)
        return result

    def occurrence_exists(self, map_identifier: int, identifier: str) -> bool:
        result = False

        with self.connection, self.connection.cursor() as cursor:
            cursor.execute(
                "SELECT identifier FROM topicdb.occurrence WHERE topicmap_identifier = %s AND identifier = %s",
                (map_identifier, identifier),
            )
            record = cursor.fetchone()
            if record:
                result = True
        return result

    def set_occurrence(
        self,
        map_identifier: int,
        occurrence: Occurrence,
        taxonomy_mode: TaxonomyMode = TaxonomyMode.STRICT,
    ) -> None:
        if occurrence.topic_identifier == "":
            raise TopicDbError("Occurrence has an empty 'topic identifier' property")

        if taxonomy_mode is TaxonomyMode.STRICT:
            instance_of_exists = self.topic_exists(
                map_identifier, occurrence.instance_of
            )
            if not instance_of_exists:
                raise TopicDbError(
                    "Taxonomy 'STRICT' mode violation: 'instance Of' topic does not exist"
                )

            scope_exists = self.topic_exists(map_identifier, occurrence.scope)
            if not scope_exists:
                raise TopicDbError(
                    "Taxonomy 'STRICT' mode violation: 'scope' topic does not exist"
                )

        with self.connection, self.connection.cursor() as cursor:
            resource_data = None
            if occurrence.resource_data is not None:
                resource_data = (
                    occurrence.resource_data
                    if isinstance(occurrence.resource_data, bytes)
                    else bytes(occurrence.resource_data, encoding="utf-8")
                )
            cursor.execute(
                "INSERT INTO topicdb.occurrence (topicmap_identifier, identifier, instance_of, scope, resource_ref, resource_data, topic_identifier, language) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    map_identifier,
                    occurrence.identifier,
                    occurrence.instance_of,
                    occurrence.scope,
                    occurrence.resource_ref,
                    psycopg2.Binary(resource_data),
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
                scope="*",
                language=Language.ENG,
            )
            occurrence.add_attribute(timestamp_attribute)
        self.set_attributes(map_identifier, occurrence.attributes)

    def update_occurrence_data(
        self, map_identifier: int, identifier: str, resource_data: Union[str, bytes]
    ) -> None:
        resource_data = (
            resource_data
            if isinstance(resource_data, bytes)
            else bytes(resource_data, encoding="utf-8")
        )

        with self.connection, self.connection.cursor() as cursor:
            cursor.execute(
                "UPDATE topicdb.occurrence SET resource_data = %s WHERE topicmap_identifier = %s AND identifier = %s",
                (psycopg2.Binary(resource_data), map_identifier, identifier),
            )

    def update_occurrence_scope(
        self, map_identifier: int, identifier: str, scope: str
    ) -> None:
        with self.connection, self.connection.cursor() as cursor:
            cursor.execute(
                "UPDATE topicdb.occurrence SET scope = %s WHERE topicmap_identifier = %s AND identifier = %s",
                (scope, map_identifier, identifier),
            )

    def update_occurrence_topic_identifier(
        self, map_identifier: int, identifier: str, topic_identifier: str
    ) -> None:
        with self.connection, self.connection.cursor() as cursor:
            cursor.execute(
                "UPDATE topicdb.occurrence SET topic_identifier = %s WHERE topicmap_identifier = %s AND identifier = %s",
                (topic_identifier, map_identifier, identifier),
            )

    # ========== TAG ==========

    def get_tags(self, map_identifier: int, identifier: str) -> List[Optional[str]]:
        result = []

        associations = self.get_topic_associations(map_identifier, identifier)
        if associations:
            groups = self.get_association_groups(
                map_identifier, associations=associations
            )
            for instance_of in groups.dict:
                for role in groups.dict[instance_of]:
                    for topic_ref in groups[instance_of, role]:
                        if topic_ref == identifier:
                            continue
                        if instance_of == "categorization":
                            result.append(topic_ref)
        return result

    def set_tag(self, map_identifier: int, identifier: str, tag: str) -> None:
        if not self.topic_exists(map_identifier, identifier):
            identifier_topic = Topic(
                identifier=identifier,
                base_name=identifier.capitalize(),
                instance_of="tag",
            )
            self.set_topic(map_identifier, identifier_topic)

        if not self.topic_exists(map_identifier, tag):
            tag_topic = Topic(
                identifier=tag, base_name=tag.capitalize(), instance_of="tag"
            )
            self.set_topic(map_identifier, tag_topic)

        tag_association1 = Association(
            instance_of="categorization",
            src_topic_ref=identifier,
            dest_topic_ref=tag,
            src_role_spec="member",
            dest_role_spec="category",
        )
        tag_association2 = Association(
            instance_of="categorization",
            src_topic_ref="tags",
            dest_topic_ref=tag,
            src_role_spec="broader",
            dest_role_spec="narrower",
        )
        self.set_association(map_identifier, tag_association1)
        self.set_association(map_identifier, tag_association2)

    def set_tags(self, map_identifier: int, identifier: str, tags: List[str]) -> None:
        for tag in tags:
            self.set_tag(map_identifier, identifier, tag)

    # ========== TOPIC ==========

    def delete_topic(
        self,
        map_identifier: int,
        identifier: str,
        taxonomy_mode: TaxonomyMode = TaxonomyMode.STRICT,
    ) -> None:
        if taxonomy_mode is TaxonomyMode.STRICT:
            for item in self.base_topics:
                if item[TopicField.IDENTIFIER.value] == identifier:
                    raise TopicDbError(
                        "Taxonomy 'STRICT' mode violation: attempt to delete a base topic"
                    )

        sql = """SELECT identifier FROM topicdb.topic WHERE topicmap_identifier = %s AND 
        identifier IN
            (SELECT association_identifier FROM topicdb.member
            WHERE topicmap_identifier = %s AND
            identifier IN (
                SELECT member_identifier FROM topicdb.topicref
                WHERE topicmap_identifier = %s AND 
                topic_ref = %s))"""

        # Delete associations
        with self.connection, self.connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor
        ) as cursor:
            cursor.execute(
                sql, (map_identifier, map_identifier, map_identifier, identifier)
            )
            records = cursor.fetchall()
            for record in records:
                self.delete_association(map_identifier, record["identifier"])

        # Delete occurrences
        self.delete_occurrences(map_identifier, identifier)

        # Delete attributes
        self.delete_attributes(map_identifier, identifier)

        # Delete topic
        with self.connection, self.connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM topicdb.topic WHERE topicmap_identifier = %s AND identifier = %s",
                (map_identifier, identifier),
            )

    def get_related_topics(
        self,
        map_identifier: int,
        identifier: str,
        instance_ofs: Optional[List[str]] = None,
        scope: str = None,
    ) -> List[Optional[Topic]]:
        result = []

        associations = self.get_topic_associations(
            map_identifier, identifier, instance_ofs=instance_ofs, scope=scope
        )
        if associations:
            groups = self.get_association_groups(
                map_identifier, associations=associations
            )
            for instance_of in groups.dict:
                for role in groups.dict[instance_of]:
                    for topic_ref in groups[instance_of, role]:
                        if topic_ref == identifier:
                            continue
                        result.append(self.get_topic(map_identifier, topic_ref))
        return result

    def get_topic(
        self,
        map_identifier: int,
        identifier: str,
        language: Language = None,
        resolve_attributes: RetrievalMode = RetrievalMode.DONT_RESOLVE_ATTRIBUTES,
        resolve_occurrences: RetrievalMode = RetrievalMode.DONT_RESOLVE_OCCURRENCES,
    ) -> Optional[Topic]:
        result = None

        with self.connection, self.connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor
        ) as cursor:
            cursor.execute(
                "SELECT identifier, instance_of FROM topicdb.topic WHERE topicmap_identifier = %s AND identifier = %s AND scope IS NULL",
                (map_identifier, identifier),
            )
            topic_record = cursor.fetchone()
            if topic_record:
                result = Topic(topic_record["identifier"], topic_record["instance_of"])
                result.clear_base_names()
                if language:
                    sql = """SELECT name, language, identifier 
                    FROM topicdb.basename 
                    WHERE topicmap_identifier = %s AND 
                    topic_identifier = %s AND 
                    language = %s"""
                    bind_variables = (map_identifier, identifier, language.name.lower())
                else:
                    sql = """SELECT name, language, identifier 
                    FROM topicdb.basename 
                    WHERE topicmap_identifier = %s AND 
                    topic_identifier = %s"""
                    bind_variables = (map_identifier, identifier)
                cursor.execute(sql, bind_variables)
                base_name_records = cursor.fetchall()
                if base_name_records:
                    for base_name_record in base_name_records:
                        result.add_base_name(
                            BaseName(
                                base_name_record["name"],
                                Language[base_name_record["language"].upper()],
                                base_name_record["identifier"],
                            )
                        )
                if resolve_attributes is RetrievalMode.RESOLVE_ATTRIBUTES:
                    result.add_attributes(
                        self.get_attributes(map_identifier, identifier)
                    )
                if resolve_occurrences is RetrievalMode.RESOLVE_OCCURRENCES:
                    result.add_occurrences(
                        self.get_topic_occurrences(map_identifier, identifier)
                    )

        return result

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
        result = []
        sql = """SELECT identifier FROM topicdb.topic WHERE topicmap_identifier = %s {0} AND 
        identifier IN
            (SELECT association_identifier FROM topicdb.member
             WHERE topicmap_identifier = %s AND
             identifier IN (
                SELECT member_identifier FROM topicdb.topicref
                    WHERE topicmap_identifier = %s
                    AND topic_ref = %s))"""
        if instance_ofs:
            instance_of_in_condition = " AND instance_of IN ("
            for index, value in enumerate(instance_ofs):
                if (index + 1) != len(instance_ofs):
                    instance_of_in_condition += "%s, "
                else:
                    instance_of_in_condition += "%s) "
            if scope:
                query_filter = instance_of_in_condition + " AND scope = %s "
                bind_variables = (
                    (map_identifier,)
                    + tuple(instance_ofs)
                    + (scope, map_identifier, map_identifier, identifier)
                )
            else:
                query_filter = instance_of_in_condition
                bind_variables = (
                    (map_identifier,)
                    + tuple(instance_ofs)
                    + (map_identifier, map_identifier, identifier)
                )
        else:
            if scope:
                query_filter = " AND scope = %s"
                bind_variables = (
                    map_identifier,
                    scope,
                    map_identifier,
                    map_identifier,
                    identifier,
                )
            else:
                query_filter = ""
                bind_variables = (
                    map_identifier,
                    map_identifier,
                    map_identifier,
                    identifier,
                )

        with self.connection, self.connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor
        ) as cursor:
            cursor.execute(sql.format(query_filter), bind_variables)
            records = cursor.fetchall()
            for record in records:
                association = self.get_association(
                    map_identifier,
                    record["identifier"],
                    language=language,
                    resolve_attributes=resolve_attributes,
                    resolve_occurrences=resolve_occurrences,
                )
                if association:
                    result.append(association)

        return result

    def get_topics_network(
        self,
        map_identifier: int,
        identifier: str,
        maximum_depth: int = 10,
        cumulative_depth: int = 0,
        accumulative_tree: Tree = None,
        accumulative_nodes: List[str] = None,
        instance_ofs: Optional[List[str]] = None,
        scope: str = None,
    ) -> Tree:
        if accumulative_tree is None:
            tree = Tree()
            root_topic = self.get_topic(map_identifier, identifier)
            tree.add_node(
                identifier, node_type=root_topic.instance_of, payload=root_topic
            )
        else:
            tree = accumulative_tree

        if accumulative_nodes is None:
            nodes: List[str] = []
        else:
            nodes = accumulative_nodes

        if cumulative_depth <= maximum_depth:  # Exit case
            associations = self.get_topic_associations(
                map_identifier, identifier, instance_ofs=instance_ofs, scope=scope
            )
            for association in associations:
                resolved_topic_refs = self._resolve_topic_refs(association)
                for resolved_topic_ref in resolved_topic_refs:
                    topic_ref = resolved_topic_ref.topic_ref
                    if (topic_ref != identifier) and (topic_ref not in nodes):
                        topic = self.get_topic(map_identifier, topic_ref)
                        tree.add_node(
                            topic_ref,
                            parent_pointer=identifier,
                            node_type=topic.instance_of,
                            edge_type=association.instance_of,
                            payload=topic,
                        )
                    if topic_ref not in nodes:
                        nodes.append(topic_ref)
            children = tree[identifier].children

            for child in children:
                # Recursive call
                self.get_topics_network(
                    map_identifier,
                    child.pointer,
                    cumulative_depth=cumulative_depth + 1,
                    accumulative_tree=tree,
                    accumulative_nodes=nodes,
                    instance_ofs=instance_ofs,
                    scope=scope,
                )
        return tree

    def get_topic_identifiers(
        self,
        map_identifier: int,
        query: str,
        instance_ofs: Optional[List[str]] = None,
        offset: int = 0,
        limit: int = 100,
    ) -> List[str]:
        result = []

        query_string = "{0}%%".format(query)
        sql = """SELECT identifier FROM topicdb.topic
        WHERE topicmap_identifier = %s AND
        identifier LIKE %s AND
        scope IS NULL
        {0}
        ORDER BY identifier
        LIMIT %s OFFSET %s"""

        if instance_ofs:
            instance_of_in_condition = " AND instance_of IN ("
            for index, value in enumerate(instance_ofs):
                if (index + 1) != len(instance_ofs):
                    instance_of_in_condition += "%s, "
                else:
                    instance_of_in_condition += "%s) "
            query_filter = instance_of_in_condition
            bind_variables = (
                (map_identifier, query_string) + tuple(instance_ofs) + (limit, offset)
            )
        else:
            query_filter = ""
            bind_variables = (map_identifier, query_string, limit, offset)

        with self.connection, self.connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor
        ) as cursor:
            cursor.execute(sql.format(query_filter), bind_variables)
            records = cursor.fetchall()
            for record in records:
                result.append(record["identifier"])
        return result

    def get_topic_names(
        self, map_identifier: int, offset: int = 0, limit: int = 100
    ) -> List[Tuple[str, str]]:
        result = []
        sql = """SELECT topicdb.basename.name AS name, topicdb.topic.identifier AS identifier
        FROM topicdb.topic 
        JOIN topicdb.basename ON topicdb.topic.identifier = topicdb.basename.topic_identifier
        WHERE topicdb.basename.topicmap_identifier = %s 
        AND topicdb.topic.topicmap_identifier = %s 
        AND topicdb.topic.scope IS NULL
        ORDER BY topicdb.basename.name
        LIMIT %s OFFSET %s"""

        with self.connection, self.connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor
        ) as cursor:
            cursor.execute(sql, (map_identifier, map_identifier, limit, offset))
            records = cursor.fetchall()
            for record in records:
                result.append((record["name"], record["identifier"]))
        return result

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
        FROM topicdb.occurrence
        WHERE topicmap_identifier = %s AND
        topic_identifier = %s
        {0}"""
        if instance_of:
            if scope:
                if language:
                    query_filter = (
                        " AND instance_of = %s AND scope = %s AND language = %s"
                    )
                    bind_variables = (
                        map_identifier,
                        identifier,
                        instance_of,
                        scope,
                        language.name.lower(),
                    )
                else:
                    query_filter = " AND instance_of = %s AND scope = %s"
                    bind_variables = (map_identifier, identifier, instance_of, scope)
            else:
                if language:
                    query_filter = " AND instance_of = %s AND language = %s"
                    bind_variables = (
                        map_identifier,
                        identifier,
                        instance_of,
                        language.name.lower(),
                    )
                else:
                    query_filter = " AND instance_of = %s"
                    bind_variables = (map_identifier, identifier, instance_of)
        else:
            if scope:
                if language:
                    query_filter = " AND scope = %s AND language = %s"
                    bind_variables = (
                        map_identifier,
                        identifier,
                        scope,
                        language.name.lower(),
                    )
                else:
                    query_filter = " AND scope = %s"
                    bind_variables = (map_identifier, identifier, scope)
            else:
                if language:
                    query_filter = " AND language = %s"
                    bind_variables = (map_identifier, identifier, language.name.lower())
                else:
                    query_filter = ""
                    bind_variables = (map_identifier, identifier)

        with self.connection, self.connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor
        ) as cursor:
            cursor.execute(sql.format(query_filter), bind_variables)
            records = cursor.fetchall()
            for record in records:
                resource_data = None
                if inline_resource_data is RetrievalMode.INLINE_RESOURCE_DATA:
                    resource_data = self.get_occurrence_data(
                        map_identifier, record["identifier"]
                    )
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
                    occurrence.add_attributes(
                        self.get_attributes(map_identifier, occurrence.identifier)
                    )
                result.append(occurrence)

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
        result = []

        if instance_of:
            sql = """SELECT identifier FROM topicdb.topic
            WHERE topicmap_identifier = %s AND
            instance_of = %s AND
            scope IS NULL
            ORDER BY identifier
            LIMIT %s OFFSET %s"""
            bind_variables = (map_identifier, instance_of, limit, offset)
        else:
            sql = """SELECT identifier FROM topicdb.topic 
            WHERE topicmap_identifier = %s AND 
            scope IS NULL
            ORDER BY identifier
            LIMIT %s OFFSET %s"""
            bind_variables = (map_identifier, limit, offset)

        with self.connection, self.connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor
        ) as cursor:
            cursor.execute(sql, bind_variables)
            records = cursor.fetchall()
            for record in records:
                result.append(
                    self.get_topic(
                        map_identifier,
                        record["identifier"],
                        language=language,
                        resolve_attributes=resolve_attributes,
                    )
                )
        return result

    def get_topic_identifiers_by_attribute_name(
        self,
        map_identifier: int,
        name: str = None,
        instance_of: str = None,
        scope: str = None,
        language: Language = None,
    ) -> List[Optional[str]]:
        result = []
        sql = """SELECT topicdb.topic.identifier AS identifier
        FROM topicdb.topic
        JOIN topicdb.attribute ON topicdb.topic.identifier = topicdb.attribute.parent_identifier
        WHERE topicdb.attribute.topicmap_identifier = %s
        AND topicdb.topic.topicmap_identifier = %s
        AND topicdb.attribute.name = %s
        {0}
        """

        if instance_of:
            if scope:
                if language:
                    query_filter = " AND topicdb.topic.instance_of = %s AND topicdb.attribute.scope = %s AND topicdb.attribute.language = %s"
                    bind_variables = (
                        map_identifier,
                        map_identifier,
                        name,
                        instance_of,
                        scope,
                        language.name.lower(),
                    )
                else:
                    query_filter = " AND topicdb.topic.instance_of = %s AND topicdb.attribute.scope = %s"
                    bind_variables = (
                        map_identifier,
                        map_identifier,
                        name,
                        instance_of,
                        scope,
                    )
            else:
                if language:
                    query_filter = " AND topicdb.topic.instance_of = %s AND topicdb.attribute.language = %s"
                    bind_variables = (
                        map_identifier,
                        map_identifier,
                        name,
                        instance_of,
                        language.name.lower(),
                    )
                else:
                    query_filter = " AND topicdb.topic.instance_of = %s"
                    bind_variables = (map_identifier, map_identifier, name, instance_of)
        else:
            if scope:
                if language:
                    query_filter = " AND topicdb.attribute.scope = %s AND topicdb.attribute.language = %s"
                    bind_variables = (
                        map_identifier,
                        map_identifier,
                        name,
                        scope,
                        language.name.lower(),
                    )
                else:
                    query_filter = " AND topicdb.attribute.scope = %s"
                    bind_variables = (map_identifier, map_identifier, name, scope)
            else:
                if language:
                    query_filter = " AND topicdb.attribute.language = %s"
                    bind_variables = (
                        map_identifier,
                        map_identifier,
                        name,
                        language.name.lower(),
                    )
                else:
                    query_filter = ""
                    bind_variables = (map_identifier, map_identifier, name)

        with self.connection, self.connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor
        ) as cursor:
            cursor.execute(sql.format(query_filter), bind_variables)
            records = cursor.fetchall()
            for record in records:
                result.append(record["identifier"])
        return result

    def set_topic(
        self,
        map_identifier: int,
        topic: Topic,
        taxonomy_mode: TaxonomyMode = TaxonomyMode.STRICT,
    ) -> None:
        if taxonomy_mode is TaxonomyMode.STRICT:
            instance_of_exists = self.topic_exists(map_identifier, topic.instance_of)
            if not instance_of_exists:
                raise TopicDbError(
                    "Taxonomy 'STRICT' mode violation: 'instance Of' topic does not exist"
                )

        with self.connection, self.connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO topicdb.topic (topicmap_identifier, identifier, instance_of) VALUES (%s, %s, %s)",
                (map_identifier, topic.identifier, topic.instance_of),
            )
            for base_name in topic.base_names:
                cursor.execute(
                    "INSERT INTO topicdb.basename (topicmap_identifier, identifier, name, topic_identifier, language) VALUES (%s, %s, %s, %s, %s)",
                    (
                        map_identifier,
                        base_name.identifier,
                        base_name.name,
                        topic.identifier,
                        base_name.language.name.lower(),
                    ),
                )
        if not topic.get_attribute_by_name("creation-timestamp"):
            timestamp = str(datetime.now())
            timestamp_attribute = Attribute(
                "creation-timestamp",
                timestamp,
                topic.identifier,
                data_type=DataType.TIMESTAMP,
                scope="*",
                language=Language.ENG,
            )
            topic.add_attribute(timestamp_attribute)
        self.set_attributes(map_identifier, topic.attributes)

    def update_topic_instance_of(
        self, map_identifier: int, identifier: str, instance_of: str
    ) -> None:
        with self.connection, self.connection.cursor() as cursor:
            cursor.execute(
                "UPDATE topicdb.topic SET instance_of = %s WHERE topicmap_identifier = %s AND identifier = %s",
                (instance_of, map_identifier, identifier),
            )

    def set_basename(
        self, map_identifier: int, identifier: str, base_name: BaseName
    ) -> None:
        with self.connection, self.connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO topicdb.basename (topicmap_identifier, identifier, name, topic_identifier, language) VALUES (%s, %s, %s, %s, %s)",
                (
                    map_identifier,
                    base_name.identifier,
                    base_name.name,
                    identifier,
                    base_name.language.name.lower(),
                ),
            )

    def update_basename(
        self,
        map_identifier: int,
        identifier: str,
        name: str,
        language: Language = Language.ENG,
    ) -> None:
        with self.connection, self.connection.cursor() as cursor:
            cursor.execute(
                "UPDATE topicdb.basename SET name = %s, language = %s WHERE topicmap_identifier = %s AND identifier = %s",
                (name, language.name.lower(), map_identifier, identifier),
            )

    def delete_basename(self, map_identifier: int, identifier: str) -> None:
        with self.connection, self.connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM topicdb.basename WHERE topicmap_identifier = %s AND identifier = %s",
                (map_identifier, identifier),
            )

    def topic_exists(self, map_identifier: int, identifier: str) -> bool:
        result = False

        with self.connection, self.connection.cursor() as cursor:
            cursor.execute(
                "SELECT identifier FROM topicdb.topic WHERE topicmap_identifier = %s AND identifier = %s",
                (map_identifier, identifier),
            )
            record = cursor.fetchone()
            if record:
                result = True
        return result

    # ========== TOPICMAP ==========

    def delete_topic_map(self, map_identifier: int) -> None:
        with self.connection, self.connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM topicdb.topicmap WHERE identifier = %s", (map_identifier,)
            )
            cursor.execute(
                "DELETE FROM topicdb.attribute WHERE topicmap_identifier = %s",
                (map_identifier,),
            )
            cursor.execute(
                "DELETE FROM topicdb.occurrence WHERE topicmap_identifier = %s",
                (map_identifier,),
            )
            cursor.execute(
                "DELETE FROM topicdb.topicref WHERE topicmap_identifier = %s",
                (map_identifier,),
            )
            cursor.execute(
                "DELETE FROM topicdb.member WHERE topicmap_identifier = %s",
                (map_identifier,),
            )
            cursor.execute(
                "DELETE FROM topicdb.basename WHERE topicmap_identifier = %s",
                (map_identifier,),
            )
            cursor.execute(
                "DELETE FROM topicdb.topic WHERE topicmap_identifier = %s",
                (map_identifier,),
            )

    def get_topic_map(self, map_identifier: int) -> Optional[TopicMap]:
        result = None

        with self.connection, self.connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor
        ) as cursor:
            cursor.execute(
                "SELECT * FROM topicdb.topicmap WHERE identifier = %s",
                (map_identifier,),
            )
            record = cursor.fetchone()
            if record:
                result = TopicMap(
                    record["user_identifier"],
                    record["identifier"],
                    record["name"],
                    description=record["description"],
                    image_path=record["image_path"],
                    initialised=record["initialised"],
                    shared=record["shared"],
                    promoted=record["promoted"],
                )
        return result

    def get_topic_maps(self, user_identifier: int) -> List[TopicMap]:
        result = []

        with self.connection, self.connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor
        ) as cursor:
            cursor.execute(
                "SELECT * FROM topicdb.topicmap WHERE user_identifier = %s ORDER BY identifier",
                (user_identifier,),
            )
            records = cursor.fetchall()
            for record in records:
                topic_map = TopicMap(
                    record["user_identifier"],
                    record["identifier"],
                    record["name"],
                    description=record["description"],
                    image_path=record["image_path"],
                    initialised=record["initialised"],
                    shared=record["shared"],
                    promoted=record["promoted"],
                )
                result.append(topic_map)
        return result

    def get_shared_topic_maps(self) -> List[TopicMap]:
        result = []

        with self.connection, self.connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor
        ) as cursor:
            cursor.execute(
                "SELECT * FROM topicdb.topicmap WHERE shared = TRUE ORDER BY identifier"
            )
            records = cursor.fetchall()
            for record in records:
                topic_map = TopicMap(
                    record["user_identifier"],
                    record["identifier"],
                    record["name"],
                    description=record["description"],
                    image_path=record["image_path"],
                    initialised=record["initialised"],
                    shared=record["shared"],
                    promoted=record["promoted"],
                )
                result.append(topic_map)
        return result

    def get_promoted_topic_maps(self) -> List[TopicMap]:
        result = []

        with self.connection, self.connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor
        ) as cursor:
            cursor.execute(
                "SELECT * FROM topicdb.topicmap WHERE promoted = TRUE ORDER BY identifier"
            )
            records = cursor.fetchall()
            for record in records:
                topic_map = TopicMap(
                    record["user_identifier"],
                    record["identifier"],
                    record["name"],
                    description=record["description"],
                    image_path=record["image_path"],
                    initialised=record["initialised"],
                    shared=record["shared"],
                    promoted=record["promoted"],
                )
                result.append(topic_map)
        return result

    def set_topic_map(
        self,
        user_identifier: int,
        name: str,
        description: str = "",
        image_path: str = "",
        initialised: bool = False,
        shared: bool = False,
        promoted: bool = False,
    ) -> int:
        with self.connection, self.connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO topicdb.topicmap (user_identifier, name, description, image_path, initialised, shared, promoted) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING identifier",
                (
                    user_identifier,
                    name,
                    description,
                    image_path,
                    initialised,
                    shared,
                    promoted,
                ),
            )
            result = cursor.fetchone()[0]
        return result

    def initialise_topic_map(self, map_identifier: int) -> None:
        topic_map = self.get_topic_map(map_identifier)

        if (
            topic_map
            and not topic_map.initialised
            and not self.topic_exists(map_identifier, "home")
        ):
            for item in self.base_topics:
                topic = Topic(
                    identifier=item[TopicField.IDENTIFIER.value],
                    base_name=item[TopicField.BASE_NAME.value],
                )
                self.set_topic(map_identifier, topic, TaxonomyMode.LENIENT)

            with self.connection, self.connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE topicdb.topicmap SET initialised = TRUE WHERE identifier = %s",
                    (map_identifier,),
                )

    def update_topic_map(
        self,
        map_identifier: int,
        name: str,
        description: str = "",
        image_path: str = "",
        initialised: bool = True,
        shared: bool = False,
        promoted: bool = False,
    ) -> None:
        with self.connection, self.connection.cursor() as cursor:
            cursor.execute(
                "UPDATE topicdb.topicmap SET name = %s, description = %s, image_path = %s, initialised = %s, shared = %s, promoted = %s WHERE identifier = %s",
                (
                    name,
                    description,
                    image_path,
                    initialised,
                    shared,
                    promoted,
                    map_identifier,
                ),
            )

    def is_topic_map_owner(self, user_identifier: int, map_identifier: int) -> bool:
        result = False

        with self.connection, self.connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM topicdb.topicmap WHERE user_identifier = %s AND identifier = %s",
                (user_identifier, map_identifier),
            )
            record = cursor.fetchone()
            if record:
                result = True
        return result

    # ========== STATISTICS ==========

    def get_topic_occurrences_statistics(
        self, map_identifier: int, identifier: str, scope: str = None
    ) -> Dict:
        result = {
            "image": 0,
            "3d-scene": 0,
            "video": 0,
            "audio": 0,
            "note": 0,
            "file": 0,
            "url": 0,
            "text": 0,
        }

        with self.connection, self.connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor
        ) as cursor:
            if scope:
                cursor.execute(
                    "SELECT instance_of, COUNT(identifier) FROM topicdb.occurrence GROUP BY topicmap_identifier, topic_identifier, instance_of, scope HAVING topicmap_identifier = %s AND topic_identifier = %s AND scope = %s",
                    (map_identifier, identifier, scope),
                )
                records = cursor.fetchall()
            else:
                cursor.execute(
                    "SELECT instance_of, COUNT(identifier) FROM topicdb.occurrence GROUP BY topicmap_identifier, topic_identifier, instance_of HAVING topicmap_identifier = %s AND topic_identifier = %s",
                    (map_identifier, identifier),
                )
                records = cursor.fetchall()
            for record in records:
                result[record["instance_of"]] = record["count"]
        return result
