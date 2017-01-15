"""
GetTopicMap class. Part of the StoryTechnologies project.

January 07, 2017
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

import sqlite3

from topicdb.core.commands.topicstoreerror import TopicStoreError
from topicdb.core.models.topicmap import TopicMap


class GetTopicMap:

    def __init__(self, database_path, identifier=''):
        self.database_path = database_path
        self.identifier = identifier

    def execute(self):
        if self.identifier == '':
            raise TopicStoreError("Missing 'identifier' parameter")
        result = None

        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row

        cursor = connection.cursor()
        try:
            cursor.execute("SELECT * FROM topicmap WHERE topicmap_identifier_fk = ?", (self.identifier, ))
            record = cursor.fetchone()
            if record:
                result = TopicMap(
                    record['title'],
                    record['topicmap_identifier_fk'],
                    record['entry_identifier_fk'],
                    record['description'])
                result.identifier = record['identifier']
        except sqlite3.Error as error:
            raise TopicStoreError(error)
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
        return result
