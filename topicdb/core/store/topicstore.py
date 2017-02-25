"""
TopicStore class. Part of the StoryTechnologies project.

February 24, 2017
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

import psycopg2

from datetime import datetime

from topicdb.core.models.attribute import Attribute
from topicdb.core.models.datatype import DataType
from topicdb.core.models.language import Language
from topicdb.core.models.topic import Topic
from topicdb.core.store.ontologymode import OntologyMode
from topicdb.core.store.topicfield import TopicField
from topicdb.core.store.topicstoreerror import TopicStoreError


class TopicStore:

    def __init__(self, host, port, password):
        self.host = host
        self.port = port
        self.password = password

        self.connection = None

    def open(self):
        connection_string = f"dbname='storytech' user='storytech' host={self.host}:{self.port} password={self.password}"
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

    def attribute_exists(self):
        pass

    def delete_attribute(self):
        pass

    def delete_attributes(self):
        pass

    def get_attribute(self):
        pass

    def get_attributes(self):
        pass

    def set_attribute(self, topic_map_identifier,
                      attribute=None,
                      ontology_mode=OntologyMode.STRICT):
        if attribute is None:
            raise TopicStoreError("Missing 'attribute' parameter")
        elif attribute.entity_identifier == '':
            raise TopicStoreError("Attribute has an empty 'entity identifier' property")

        if ontology_mode is OntologyMode.STRICT:
            scope_exists = self.topic_exists(topic_map_identifier, attribute.scope)
            if not scope_exists:
                raise TopicStoreError("Ontology mode 'STRICT' violation: 'scope' topic does not exist")

        # http://initd.org/psycopg/docs/usage.html#with-statement
        with self.connection:
            self.connection.execute("INSERT INTO topicdb.attribute (topicmap_identifier, identifier, parent_identifier_fk, name, value, data_type, scope, language) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                                    (topic_map_identifier,
                                     attribute.identifier,
                                     attribute.entity_identifier,
                                     attribute.name,
                                     attribute.value,
                                     attribute.data_type.name.lower(),
                                     attribute.scope,
                                     attribute.language.name.lower()))

    def set_attributes(self, topic_map_identifier, attributes=None):
        if attributes is None:
            raise TopicStoreError("Missing 'attributes' parameter")

        for attribute in self.attributes:
            self.set_attribute(topic_map_identifier, attribute)

    # ========== METRIC ==========

    def get_metrics(self):
        pass

    # ========== OCCURRENCE ==========

    def delete_occurrence(self):
        pass

    def delete_occurrences(self):
        pass

    def get_occurrence(self):
        pass

    def get_occurrence_data(self):
        pass

    def get_occurrences(self):
        pass

    def occurrence_exists(self, topic_map_identifier, identifier=''):
        if identifier == '':
            raise TopicStoreError("Missing 'identifier' parameter")
        result = False

        # http://initd.org/psycopg/docs/usage.html#with-statement
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT identifier FROM topicdb.occurrence WHERE topicmap_identifier = ? AND identifier = ?", (topic_map_identifier, identifier))
                record = cursor.fetchone()
                if record:
                    result = True
        return result

    def set_occurrence(self, topic_map_identifier, occurrence=None, ontology_mode=OntologyMode.STRICT):
        if occurrence is None:
            raise TopicStoreError("Missing 'occurrence' parameter")
        elif occurrence.topic_identifier == '':
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
            self.connection.execute("INSERT INTO topicdb.occurrence (topicmap_identifier, identifier, instance_of, scope, resource_ref, resource_data, topic_identifier_fk, language) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
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

    def set_occurrence_data(self, topic_map_identifier, identifier='', resource_data=None):
        if identifier == '' or resource_data is None:
            raise TopicStoreError("Missing either or both 'identifier' and 'resource data' parameters")

        # http://initd.org/psycopg/docs/usage.html#with-statement
        with self.connection:
            self.connection.execute("UPDATE topicdb.occurrence SET resource_data = ? WHERE topicmap_identifier = ? AND identifier = ?", (resource_data, topic_map_identifier, identifier))

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

    def get_topic(self):
        pass

    def get_topic_associations(self):
        pass

    def get_topic_identifiers(self):
        pass

    def get_topic_occurrences(self):
        pass

    def get_topics(self):
        pass

    def get_topics_hierarchy(self):
        pass

    def set_topic(self, topic_map_identifier,
                  topic=None,
                  ontology_mode=OntologyMode.STRICT):
        if topic is None:
            raise TopicStoreError("Missing 'topic' parameter")

        if ontology_mode is OntologyMode.STRICT:
            instance_of_exists = self.topic_exists(topic_map_identifier, topic.instance_of)
            if not instance_of_exists:
                raise TopicStoreError("Ontology mode 'STRICT' violation: 'instance Of' topic does not exist")

        # http://initd.org/psycopg/docs/usage.html#with-statement
        with self.connection:
            self.connection.execute("INSERT INTO topicdb.topic (topicmap_identifier, identifier, instance_of) VALUES (?, ?, ?)",
                                    (topic_map_identifier,
                                     topic.identifier,
                                     topic.instance_of))
            for base_name in topic.base_names:
                self.connection.execute("INSERT INTO topicdb.basename (topicmap_identifier, identifier, name, topic_identifier_fk, language) VALUES (?, ?, ?, ?, ?)",
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
        if identifier == '':
            raise TopicStoreError("Missing 'identifier' parameter")
        result = False

        # http://initd.org/psycopg/docs/usage.html#with-statement
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT identifier FROM topicdb.topic WHERE topicmap_identifier = ? AND identifier = ?", (topic_map_identifier, identifier))
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
