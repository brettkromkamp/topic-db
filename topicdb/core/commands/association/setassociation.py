"""
SetAssociation class. Part of the StoryTechnologies project.

July 12, 2016
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

import sqlite3

from datetime import datetime

from topicdb.core.models.language import Language
from topicdb.core.models.datatype import DataType
from topicdb.core.models.attribute import Attribute
from topicdb.core.topicstoreerror import TopicStoreError
from topicdb.core.commands.attribute.setattributes import SetAttributes


class SetAssociation:

    def __init__(self, database_path, map_identifier, association=None):
        self.database_path = database_path
        self.map_identifier = map_identifier
        self.association = association

    def execute(self):
        if self.association is None:
            raise TopicStoreError("Missing 'association' parameter")

        connection = sqlite3.connect(self.database_path)

        try:
            with connection:  # https://docs.python.org/3/library/sqlite3.html#using-the-connection-as-a-context-manager
                connection.execute("INSERT INTO topic (topicmap_identifier, identifier, instance_of, scope) VALUES (?, ?, ?, ?)", (self.map_identifier, self.association.identifier, self.association.instance_of, self.association.scope))
                for base_name in self.association.base_names:
                    connection.execute("INSERT INTO basename (topicmap_identifier, identifier, name, topic_identifier_fk, language) VALUES (?, ?, ?, ?, ?)",
                                       (self.map_identifier,
                                        base_name.identifier,
                                        base_name.name,
                                        self.association.identifier,
                                        base_name.language.name))
                for member in self.association.members:
                    connection.execute("INSERT INTO member (topicmap_identifier, identifier, role_spec, association_identifier_fk) VALUES (?, ?, ?, ?)", (self.map_identifier, member.identifier, member.role_spec, self.association.identifier))
                    for topic_ref in member.topic_refs:
                        connection.execute("INSERT INTO topicref (topicmap_identifier, topic_ref, member_identifier_fk) VALUES (?, ?, ?)", (self.map_identifier, topic_ref, member.identifier))

            if not self.association.get_attribute_by_name('creation-timestamp'):
                timestamp = str(datetime.now())
                timestamp_attribute = Attribute('creation-timestamp', timestamp, self.association.identifier,
                                                data_type=DataType.timestamp,
                                                scope='*',
                                                language=Language.eng)
                self.association.add_attribute(timestamp_attribute)
            SetAttributes(self.database_path, self.map_identifier, self.association.attributes).execute()
        except sqlite3.Error as error:
            raise TopicStoreError(error)
        finally:
            if connection:
                connection.close()
