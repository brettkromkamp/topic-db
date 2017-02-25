"""
TopicStore class. Part of the StoryTechnologies project.

February 24, 2017
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

import psycopg2

from datetime import datetime

from topicdb.core.models.attribute import Attribute
from topicdb.core.models.basename import BaseName
from topicdb.core.models.datatype import DataType
from topicdb.core.models.language import Language
from topicdb.core.models.occurrence import Occurrence
from topicdb.core.models.topic import Topic
from topicdb.core.store.ontologymode import OntologyMode
from topicdb.core.store.retrievaloption import RetrievalOption
from topicdb.core.store.topicfield import TopicField
from topicdb.core.store.topicstoreerror import TopicStoreError


class TopicStore:

    def __init__(self, host, port, password):
        self.host = host
        self.port = port
        self.password = password

        self.connection = None

    def open(self):
        connection_string = f"dbname='storytech' user='storytech' host={self.host} password={self.password}"
        self.connection = psycopg2.connect(connection_string)

    def close(self):
        if self.connection:
            self.connection.close()

    # ========== ASSOCIATION ==========

    def delete_association(self):
        pass

    def get_association(self):
        pass

    def get_association_groups(self):
        pass

    def get_associations(self):
        pass

    def set_association(self):
        pass

    # ========== ATTRIBUTE ==========

    def attribute_exists(self, topic_map_identifier, entity_identifier, name):
        result = False

        # http://initd.org/psycopg/docs/usage.html#with-statement
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT identifier FROM topicdb.attribute WHERE topicmap_identifier = %s AND parent_identifier_fk = %s AND name = %s", (topic_map_identifier, entity_identifier, name))
                record = cursor.fetchone()
                if record:
                    result = True
        return result

    def delete_attribute(self):
        pass

    def delete_attributes(self):
        pass

    def get_attribute(self, topic_map_identifier, identifier):
        # http://initd.org/psycopg/docs/usage.html#with-statement
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM topicdb.attribute WHERE topicmap_identifier = %s AND identifier = %s", (self.topic_map_identifier, self.identifier))
                record = cursor.fetchone()
                if record:
                    result = Attribute(
                        record['name'],
                        record['value'],
                        record['parent_identifier_fk'],
                        record['identifier'],
                        DataType[record['data_type'].upper()],
                        record['scope'],
                        Language[record['language'].upper()])
        return result

    def get_attributes(self, topic_map_identifier, entity_identifier, scope=None, language=None):
        result = []

        if scope is None:
            if language is None:
                sql = "SELECT * FROM topicdb.attribute WHERE topicmap_identifier = %s AND parent_identifier_fk = %s"
                bind_variables = (topic_map_identifier, entity_identifier)
            else:
                sql = "SELECT * FROM topicdb.attribute WHERE topicmap_identifier = %s AND parent_identifier_fk = %s AND language = %s"
                bind_variables = (topic_map_identifier, entity_identifier, language.name.lower())
        else:
            if language is None:
                sql = "SELECT * FROM topicdb.attribute WHERE topicmap_identifier = %s AND parent_identifier_fk = %s AND scope = %s"
                bind_variables = (topic_map_identifier, entity_identifier, scope)
            else:
                sql = "SELECT * FROM topicdb.attribute WHERE topicmap_identifier = %s AND parent_identifier_fk = %s AND scope = %s AND language = %s"
                bind_variables = (topic_map_identifier, entity_identifier, scope, language.name.lower())

        # http://initd.org/psycopg/docs/usage.html#with-statement
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute(sql, bind_variables)
                records = cursor.fetchall()
                for record in records:
                    attribute = Attribute(
                        record['name'],
                        record['value'],
                        record['parent_identifier_fk'],
                        record['identifier'],
                        DataType[record['data_type'].upper()],
                        record['scope'],
                        Language[record['language'].upper()])
                    result.append(attribute)
        return result

    def set_attribute(self, topic_map_identifier, attribute, ontology_mode=OntologyMode.LENIENT):
        if attribute.entity_identifier == '':
            raise TopicStoreError("Attribute has an empty 'entity identifier' property")

        if ontology_mode is OntologyMode.STRICT:
            scope_exists = self.topic_exists(topic_map_identifier, attribute.scope)
            if not scope_exists:
                raise TopicStoreError("Ontology mode 'STRICT' violation: 'scope' topic does not exist")

        # http://initd.org/psycopg/docs/usage.html#with-statement
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute("INSERT INTO topicdb.attribute (topicmap_identifier, identifier, parent_identifier_fk, name, value, data_type, scope, language) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                                        (topic_map_identifier,
                                         attribute.identifier,
                                         attribute.entity_identifier,
                                         attribute.name,
                                         attribute.value,
                                         attribute.data_type.name.lower(),
                                         attribute.scope,
                                         attribute.language.name.lower()))

    def set_attributes(self, topic_map_identifier, attributes):
        for attribute in attributes:
            self.set_attribute(topic_map_identifier, attribute)

    # ========== METRIC ==========

    def get_metrics(self):
        pass

    # ========== OCCURRENCE ==========

    def delete_occurrence(self):
        pass

    def delete_occurrences(self):
        pass

    def get_occurrence(self, topic_map_identifier, identifier,
                       inline_resource_data=RetrievalOption.DONT_INLINE_RESOURCE_DATA,
                       resolve_attributes=RetrievalOption.DONT_RESOLVE_ATTRIBUTES):
        result = None

        # http://initd.org/psycopg/docs/usage.html#with-statement
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT identifier, instance_of, scope, resource_ref, topic_identifier_fk, language FROM topicdb.occurrence WHERE topicmap_identifier = %s AND identifier = %s", (topic_map_identifier, identifier))
                record = cursor.fetchone()
                if record:
                    resource_data = None
                    if inline_resource_data is RetrievalOption.INLINE_RESOURCE_DATA:
                        resource_data = self.get_occurrence_data(topic_map_identifier, identifier=identifier)
                    result = Occurrence(
                        record['identifier'],
                        record['instance_of'],
                        record['topic_identifier_fk'],
                        record['scope'],
                        record['resource_ref'],
                        resource_data,
                        Language[record['language'].upper()])
                    if resolve_attributes is RetrievalOption.RESOLVE_ATTRIBUTES:
                        result.add_attributes(self.get_attributes(topic_map_identifier, identifier))
        return result

    def get_occurrence_data(self, topic_map_identifier, identifier):
        result = None

        # http://initd.org/psycopg/docs/usage.html#with-statement
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT resource_data FROM topicdb.occurrence WHERE topicmap_identifier = %s AND identifier = %s", (topic_map_identifier, identifier))
                record = cursor.fetchone()
                if record:
                    result = record['resource_data']
        return result

    def get_occurrences(self, topic_map_identifier,
                        instance_of=None,
                        scope=None,
                        language=None,
                        offset=0,
                        limit=100,
                        inline_resource_data=RetrievalOption.DONT_INLINE_RESOURCE_DATA,
                        resolve_attributes=RetrievalOption.DONT_RESOLVE_ATTRIBUTES):
        result = []
        sql = "SELECT * FROM topicdb.occurrence WHERE topicmap_identifier = %s {0}"
        if instance_of is None:
            if scope is None:
                if language is None:
                    query_filter = ""
                    bind_variables = (topic_map_identifier,)
                else:
                    query_filter = " AND language = %s"
                    bind_variables = (topic_map_identifier, language.name.lower())
            else:
                if language is None:
                    query_filter = " AND scope = %s"
                    bind_variables = (topic_map_identifier, scope)
                else:
                    query_filter = " AND scope = %s AND language = %s"
                    bind_variables = (topic_map_identifier, scope, language.name.lower())
        else:
            if scope is None:
                if language is None:
                    query_filter = " AND instance_of = %s"
                    bind_variables = (topic_map_identifier, instance_of)
                else:
                    query_filter = " AND instance_of = %s AND language = %s"
                    bind_variables = (topic_map_identifier, instance_of, language.name.lower())
            else:
                if language is None:
                    query_filter = " AND instance_of = %s AND scope = %s"
                    bind_variables = (topic_map_identifier, instance_of, scope)
                else:
                    query_filter = " AND instance_of = %s AND scope = %s AND language = %s"
                    bind_variables = (topic_map_identifier, instance_of, scope, language.name.lower())

        # http://initd.org/psycopg/docs/usage.html#with-statement
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute(sql.format(query_filter), bind_variables)
                records = cursor.fetchall()
                for record in records:
                    resource_data = None
                    if inline_resource_data is RetrievalOption.INLINE_RESOURCE_DATA:
                        resource_data = self.get_occurrence_data(topic_map_identifier, identifier=record['identifier'])
                    occurrence = Occurrence(
                        record['identifier'],
                        record['instance_of'],
                        record['topic_identifier_fk'],
                        record['scope'],
                        record['resource_ref'],
                        resource_data,
                        Language[record['language'].upper()])
                    if resolve_attributes is RetrievalOption.RESOLVE_ATTRIBUTES:
                        occurrence.add_attributes(self.get_attributes(topic_map_identifier, occurrence.identifier))
                    result.append(occurrence)
        return result

    def occurrence_exists(self, topic_map_identifier, identifier):
        result = False

        # http://initd.org/psycopg/docs/usage.html#with-statement
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT identifier FROM topicdb.occurrence WHERE topicmap_identifier = %s AND identifier = %s", (topic_map_identifier, identifier))
                record = cursor.fetchone()
                if record:
                    result = True
        return result

    def set_occurrence(self, topic_map_identifier, occurrence, ontology_mode=OntologyMode.STRICT):
        if occurrence.topic_identifier == '':
            raise TopicStoreError("Occurrence has an empty 'topic identifier' property")

        if ontology_mode is OntologyMode.STRICT:
            instance_of_exists = self.topic_exists(topic_map_identifier, occurrence.instance_of)
            if not instance_of_exists:
                raise TopicStoreError("Ontology mode 'STRICT' violation: 'instance Of' topic does not exist")

            scope_exists = self.topic_exists(topic_map_identifier, occurrence.scope)
            if not scope_exists:
                raise TopicStoreError("Ontology mode 'STRICT' violation: 'scope' topic does not exist")

        # http://initd.org/psycopg/docs/usage.html#with-statement
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute("INSERT INTO topicdb.occurrence (topicmap_identifier, identifier, instance_of, scope, resource_ref, resource_data, topic_identifier_fk, language) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                                        (topic_map_identifier,
                                         occurrence.identifier,
                                         occurrence.instance_of,
                                         occurrence.scope,
                                         occurrence.resource_ref,
                                         occurrence.resource_data,
                                         occurrence.topic_identifier,
                                         occurrence.language.name.lower()))
        if not occurrence.get_attribute_by_name('creation-timestamp'):
            timestamp = str(datetime.now())
            timestamp_attribute = Attribute('creation-timestamp', timestamp,
                                            occurrence.identifier,
                                            data_type=DataType.TIMESTAMP,
                                            scope='*',
                                            language=Language.ENG)
            occurrence.add_attribute(timestamp_attribute)
        self.set_attributes(topic_map_identifier, occurrence.attributes)

    def set_occurrence_data(self, topic_map_identifier, identifier, resource_data):
        # http://initd.org/psycopg/docs/usage.html#with-statement
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute("UPDATE topicdb.occurrence SET resource_data = %s WHERE topicmap_identifier = %s AND identifier = %s", (resource_data, topic_map_identifier, identifier))

    # ========== TAG ==========

    def get_tags(self):
        pass

    def set_tag(self):
        pass

    def set_tags(self):
        pass

    # ========== TOPIC ==========

    def delete_topic(self):
        pass

    def get_related_topics(self):
        pass

    def get_topic(self, topic_map_identifier, identifier,
                  language=None,
                  resolve_attributes=RetrievalOption.DONT_RESOLVE_ATTRIBUTES,
                  resolve_occurrences=RetrievalOption.DONT_RESOLVE_OCCURRENCES):
        result = None

        # http://initd.org/psycopg/docs/usage.html#with-statement
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT identifier, instance_of FROM topicdb.topic WHERE topicmap_identifier = %s AND identifier = %s AND scope IS NULL", (topic_map_identifier, identifier))
                topic_record = cursor.fetchone()
                if topic_record:
                    result = Topic(topic_record['identifier'], topic_record['instance_of'])
                    result.clear_base_names()
                    if language is None:
                        sql = "SELECT name, language, identifier FROM topicdb.basename WHERE topicmap_identifier = %s AND topic_identifier_fk = %s"
                        bind_variables = (topic_map_identifier, identifier)
                    else:
                        sql = "SELECT name, language, identifier FROM topicdb.basename WHERE topicmap_identifier = %s AND topic_identifier_fk = %s AND language = %s"
                        bind_variables = (topic_map_identifier, identifier, language.name.lower())
                    cursor.execute(sql, bind_variables)
                    base_name_records = cursor.fetchall()
                    if base_name_records:
                        for base_name_record in base_name_records:
                            result.add_base_name(BaseName(base_name_record['name'], Language[base_name_record['language'].upper()], base_name_record['identifier']))
                    if resolve_attributes is RetrievalOption.RESOLVE_ATTRIBUTES:
                        result.add_attributes(self.get_attributes(topic_map_identifier, identifier))
                    if resolve_occurrences is RetrievalOption.RESOLVE_OCCURRENCES:
                        result.add_occurrences(self.get_occurrences(topic_map_identifier, identifier))

        return result

    def get_topic_associations(self):
        pass

    def get_topic_identifiers(self, topic_map_identifier, query, offset=0, limit=100):
        result = []

        query_string = "{0}%%".format(query)

        # http://initd.org/psycopg/docs/usage.html#with-statement
        with self.connection:
            with self.connection.cursor() as cursor:
                sql = "SELECT identifier FROM topicdb.topic WHERE topicmap_identifier = %s AND identifier LIKE %s AND scope IS NULL ORDER BY identifier LIMIT %s OFFSET %s"
                cursor.execute(sql, (topic_map_identifier, query_string, limit, offset))
                records = cursor.fetchall()
                for record in records:
                    result.append(record['identifier'])
        return result

    def get_topic_occurrences(self, topic_map_identifier, identifier,
                              instance_of=None,
                              scope=None,
                              language=None,
                              inline_resource_data=RetrievalOption.DONT_INLINE_RESOURCE_DATA,
                              resolve_attributes=RetrievalOption.DONT_RESOLVE_ATTRIBUTES):
        result = []
        sql = "SELECT identifier, instance_of, scope, resource_ref, topic_identifier_fk, language FROM topicdb.occurrence WHERE topicmap_identifier = %s AND topic_identifier_fk = %s {0}"
        if instance_of is None:
            if scope is None:
                if language is None:
                    query_filter = ""
                    bind_variables = (topic_map_identifier, identifier)
                else:
                    query_filter = " AND language = %s"
                    bind_variables = (topic_map_identifier, identifier, language.name.lower())
            else:
                if language is None:
                    query_filter = " AND scope = %s"
                    bind_variables = (topic_map_identifier, identifier, scope)
                else:
                    query_filter = " AND scope = %s AND language = %s"
                    bind_variables = (topic_map_identifier, identifier, scope, language.name.lower())
        else:
            if scope is None:
                if language is None:
                    query_filter = " AND instance_of = %s"
                    bind_variables = (topic_map_identifier, identifier, instance_of)
                else:
                    query_filter = " AND instance_of = %s AND language = %s"
                    bind_variables = (topic_map_identifier, identifier, instance_of, language.name.lower())
            else:
                if language is None:
                    query_filter = " AND instance_of = %s AND scope = %s"
                    bind_variables = (topic_map_identifier, identifier, instance_of, scope)
                else:
                    query_filter = " AND instance_of = %s AND scope = %s AND language = %s"
                    bind_variables = (topic_map_identifier, identifier, instance_of, scope, language.name.lower())

        # http://initd.org/psycopg/docs/usage.html#with-statement
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute(sql.format(query_filter), bind_variables)
                records = cursor.fetchall()
                for record in records:
                    resource_data = None
                    if inline_resource_data is RetrievalOption.INLINE_RESOURCE_DATA:
                        resource_data = self.get_occurrence_data(topic_map_identifier, record['identifier'])
                    occurrence = Occurrence(
                        record['identifier'],
                        record['instance_of'],
                        record['topic_identifier_fk'],
                        record['scope'],
                        record['resource_ref'],
                        resource_data,
                        Language[record['language'].upper()])
                    if resolve_attributes is RetrievalOption.RESOLVE_ATTRIBUTES:
                        occurrence.add_attributes(
                            self.get_attributes(topic_map_identifier, occurrence.identifier))
                    result.append(occurrence)

        return result

    def get_topics(self, topic_map_identifier,
                   instance_of=None,
                   language=None,
                   offset=0,
                   limit=100,
                   resolve_attributes=RetrievalOption.DONT_RESOLVE_ATTRIBUTES):
        result = []

        if instance_of is None:
            sql = "SELECT identifier FROM topicdb.topic WHERE topicmap_identifier = %s AND scope IS NULL ORDER BY identifier LIMIT %s OFFSET %s"
            bind_variables = (topic_map_identifier, limit, offset)
        else:
            sql = "SELECT identifier FROM topicdb.topic WHERE topicmap_identifier = %s AND instance_of = %s AND scope IS NULL ORDER BY identifier LIMIT %s OFFSET %s"
            bind_variables = (topic_map_identifier, instance_of, limit, offset)

        # http://initd.org/psycopg/docs/usage.html#with-statement
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute(sql, bind_variables)
                records = cursor.fetchall()
                for record in records:
                    result.append(self.get_topic(topic_map_identifier, record['identifier'],
                                                 language=language,
                                                 resolve_attributes=resolve_attributes))

        return result

    def get_topics_hierarchy(self):
        pass

    def set_topic(self, topic_map_identifier, topic, ontology_mode=OntologyMode.STRICT):
        if ontology_mode is OntologyMode.STRICT:
            instance_of_exists = self.topic_exists(topic_map_identifier, topic.instance_of)
            if not instance_of_exists:
                raise TopicStoreError("Ontology mode 'STRICT' violation: 'instance Of' topic does not exist")

        # http://initd.org/psycopg/docs/usage.html#with-statement
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute("INSERT INTO topicdb.topic (topicmap_identifier, identifier, instance_of) VALUES (%s, %s, %s)",
                                        (topic_map_identifier,
                                         topic.identifier,
                                         topic.instance_of))
                for base_name in topic.base_names:
                    cursor.execute("INSERT INTO topicdb.basename (topicmap_identifier, identifier, name, topic_identifier_fk, language) VALUES (%s, %s, %s, %s, %s)",
                                            (topic_map_identifier,
                                             base_name.identifier,
                                             base_name.name,
                                             topic.identifier,
                                             base_name.language.name.lower()))
        if not topic.get_attribute_by_name('creation-timestamp'):
            timestamp = str(datetime.now())
            timestamp_attribute = Attribute('creation-timestamp', timestamp, topic.identifier,
                                            data_type=DataType.TIMESTAMP,
                                            scope='*',
                                            language=Language.ENG)
            topic.add_attribute(timestamp_attribute)
        self.set_attributes(topic_map_identifier, topic.attributes)

    def topic_exists(self, topic_map_identifier, identifier):
        result = False

        # http://initd.org/psycopg/docs/usage.html#with-statement
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT identifier FROM topicdb.topic WHERE topicmap_identifier = %s AND identifier = %s", (topic_map_identifier, identifier))
                record = cursor.fetchone()
                if record:
                    result = True
        return result

    # ========== TOPICMAP ==========

    def delete_topic_map(self):
        pass

    def get_topic_map(self):
        pass

    def get_topic_maps(self):
        pass

    def set_topic_map(self, topic_map_identifier, title, description='', entry_topic='genesis'):
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute("INSERT INTO topicdb.topicmap (title, description, topicmap_identifier_fk, entry_identifier_fk) VALUES (%s, %s, %s, %s)", (title, description, topic_map_identifier, entry_topic))

        if not self.topic_exists(topic_map_identifier, 'genesis'):
            items = {
                ('entity', 'Entity'),
                ('topic', 'Topic'),
                ('association', 'Association'),
                ('occurrence', 'Occurrence'),
                ('*', 'Universal Scope'),
                ('genesis', 'Genesis'),
                ('navigation', 'Navigation'),
                ('member', 'Member'),
                ('category', 'Category'),
                ('categorization', 'Categorization'),
                ('tags', 'Tags'),
                ('broader', 'Broader'),
                ('narrower', 'Narrower'),
                ('related', 'Related'),
                ('parent', 'Parent'),
                ('child', 'Child'),
                ('previous', 'Previous'),
                ('next', 'Next'),
                ('includes', 'Includes'),
                ('included-in', 'Is Included In'),
                ('story', 'Story'),
                ('book', 'Book'),
                ('chapter', 'Chapter'),
                ('scene', 'Scene'),
                ('prop', 'Prop'),
                ('character', 'Character'),
                ('image', 'Image'),
                ('video', 'Video'),
                ('text', 'Text'),
                ('html', 'HTML'),
                ('annotation', 'Annotation'),
                ('dialogue', 'Dialogue'),
                ('up', 'Up'),
                ('down', 'Down'),
                ('north', 'North'),
                ('north-east', 'Northeast'),
                ('east', 'East'),
                ('south-east', 'Southeast'),
                ('south', 'South'),
                ('south-west', 'Southwest'),
                ('west', 'West'),
                ('north-west', 'Northwest'),
                ('eng', 'English Language'),
                ('spa', 'Spanish Language'),
                ('deu', 'German Language'),
                ('ita', 'Italian Language'),
                ('fra', 'French Language'),
                ('nld', 'Dutch Language'),
                ('nob', 'Norwegian (Bokmål) Language')}

            for item in items:
                topic = Topic(identifier=item[TopicField.IDENTIFIER.value], base_name=item[TopicField.BASE_NAME.value])
                self.set_topic(topic_map_identifier, topic, OntologyMode.LENIENT)
