"""
AttributeExists class. Part of the StoryTechnologies project.

December 28, 2016
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

import sqlite3

from topicdb.core.commands.topicstoreerror import TopicStoreError


class AttributeExists:

    def __init__(self, database_path, topic_map_identifier, entity_identifier='', name=''):
        self.database_path = database_path
        self.topic_map_identifier = topic_map_identifier
        self.entity_identifier = entity_identifier
        self.name = name

    def execute(self):
        if self.entity_identifier == '' or self.name == '':
            raise TopicStoreError("Missing 'entity identifier' or 'name' parameters")
        result = False

        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row

        cursor = connection.cursor()
        try:
            cursor.execute("SELECT identifier FROM attribute WHERE topicmap_identifier = ? AND parent_identifier_fk = ? AND name = ?", (self.topic_map_identifier, self.entity_identifier, self.name))
            record = cursor.fetchone()
            if record:
                result = True
        except sqlite3.Error as error:
            raise TopicStoreError(error)
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
        return result
