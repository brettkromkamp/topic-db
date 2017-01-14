"""
SetTopic class. Part of the StoryTechnologies project.

July 12, 2016
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

import sqlite3
from datetime import datetime

from topicdb.core.commands.attribute.setattributes import SetAttributes
from topicdb.core.commands.ontologymode import OntologyMode
from topicdb.core.commands.topic.topicexists import TopicExists
from topicdb.core.commands.topicstoreerror import TopicStoreError
from topicdb.core.models.attribute import Attribute
from topicdb.core.models.datatype import DataType
from topicdb.core.models.language import Language


class SetTopic:

    def __init__(self, database_path, topic_map_identifier,
                 topic=None,
                 language=Language.ENG,
                 ontology_mode=OntologyMode.STRICT):
        self.database_path = database_path
        self.topic_map_identifier = topic_map_identifier
        self.topic = topic
        self.language = language
        self.ontology_mode = ontology_mode

    def execute(self):
        if self.topic is None:
            raise TopicStoreError("Missing 'topic' parameter")

        if self.ontology_mode is OntologyMode.STRICT:
            instance_of_exists = TopicExists(self.database_path, self.topic_map_identifier, self.topic.instance_of).execute()
            if not instance_of_exists:
                raise TopicStoreError("Ontology mode 'STRICT' violation: 'instance Of' topic does not exist")

        connection = sqlite3.connect(self.database_path)

        try:
            with connection:
                connection.execute("INSERT INTO topic (topicmap_identifier, identifier, instance_of) VALUES (?, ?, ?)",
                                   (self.topic_map_identifier,
                                    self.topic.identifier,
                                    self.topic.instance_of))
                for base_name in self.topic.base_names:
                    connection.execute("INSERT INTO basename (topicmap_identifier, identifier, name, topic_identifier_fk, language) VALUES (?, ?, ?, ?, ?)",
                                       (self.topic_map_identifier,
                                        base_name.identifier,
                                        base_name.name,
                                        self.topic.identifier,
                                        base_name.language.name.lower()))
            if not self.topic.get_attribute_by_name('creation-timestamp'):
                timestamp = str(datetime.now())
                timestamp_attribute = Attribute('creation-timestamp', timestamp, self.topic.identifier,
                                                data_type=DataType.TIMESTAMP,
                                                scope='*',
                                                language=Language.ENG)
                self.topic.add_attribute(timestamp_attribute)
            SetAttributes(self.database_path, self.topic_map_identifier, self.topic.attributes).execute()
        except sqlite3.Error as error:
            raise TopicStoreError(error)
        finally:
            if connection:
                connection.close()
