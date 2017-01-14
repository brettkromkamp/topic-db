"""
SetAttribute class. Part of the StoryTechnologies project.

July 12, 2016
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

import sqlite3

from topicdb.core.commands.ontologymode import OntologyMode
from topicdb.core.commands.topic.topicexists import TopicExists
from topicdb.core.commands.topicstoreerror import TopicStoreError


class SetAttribute:

    def __init__(self, database_path, topic_map_identifier,
                 attribute=None, ontology_mode=OntologyMode.LENIENT):
        self.database_path = database_path
        self.topic_map_identifier = topic_map_identifier
        self.attribute = attribute
        self.ontology_mode = ontology_mode

    def execute(self):
        if self.attribute is None:
            raise TopicStoreError("Missing 'attribute' parameter")
        elif self.attribute.entity_identifier == '':
            raise TopicStoreError("Attribute has an empty 'entity identifier' property")

        if self.ontology_mode is OntologyMode.STRICT:
            scope_exists = TopicExists(self.database_path, self.topic_map_identifier,
                                       self.attribute.scope).execute()
            if not scope_exists:
                raise TopicStoreError("Ontology mode 'STRICT' violation: 'scope' topic does not exist")

        connection = sqlite3.connect(self.database_path)

        try:
            with connection:
                connection.execute("INSERT INTO attribute (topicmap_identifier, identifier, parent_identifier_fk, name, value, data_type, scope, language) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                                   (self.topic_map_identifier,
                                    self.attribute.identifier,
                                    self.attribute.entity_identifier,
                                    self.attribute.name,
                                    self.attribute.value,
                                    self.attribute.data_type.name.lower(),
                                    self.attribute.scope,
                                    self.attribute.language.name.lower()))
        except sqlite3.Error as error:
            raise TopicStoreError(error)
        finally:
            if connection:
                connection.close()
