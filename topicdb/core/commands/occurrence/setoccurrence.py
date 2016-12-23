"""
SetOccurrence class. Part of the StoryTechnologies project.

July 12, 2016
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

import sqlite3

from datetime import datetime

from topicdb.core.models.language import Language
from topicdb.core.models.datatype import DataType
from topicdb.core.models.attribute import Attribute
from topicdb.core.commands.attribute.setattributes import SetAttributes
from topicdb.core.topicstoreerror import TopicStoreError


class SetOccurrence:

    def __init__(self, database_path, map_identifier, occurrence=None):
        self.database_path = database_path
        self.map_identifier = map_identifier
        self.occurrence = occurrence

    def execute(self):
        if self.occurrence is None:
            raise TopicStoreError("Missing 'occurrence' parameter")
        elif self.occurrence.topic_identifier == '':
            raise TopicStoreError("Occurrence has an empty 'topic identifier' property")

        connection = sqlite3.connect(self.database_path)

        try:
            with connection:  # https://docs.python.org/3/library/sqlite3.html#using-the-connection-as-a-context-manager
                connection.execute("INSERT INTO occurrence (topicmap_identifier, identifier, instance_of, scope, resource_ref, resource_data, topic_identifier_fk, language) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                                   (self.map_identifier,
                                    self.occurrence.identifier,
                                    self.occurrence.instance_of,
                                    self.occurrence.scope,
                                    self.occurrence.resource_ref,
                                    self.occurrence.resource_data,
                                    self.occurrence.topic_identifier,
                                    self.occurrence.language.name))
            if not self.occurrence.get_attribute_by_name('creation-timestamp'):
                timestamp = str(datetime.now())
                timestamp_attribute = Attribute('creation-timestamp', timestamp, self.occurrence.identifier,
                                                data_type=DataType.timestamp,
                                                scope='*',
                                                language=Language.eng)
                self.occurrence.add_attribute(timestamp_attribute)
            SetAttributes(self.database_path, self.map_identifier, self.occurrence.attributes).execute()
        except sqlite3.Error as error:
            raise TopicStoreError(error)
        finally:
            if connection:
                connection.close()
