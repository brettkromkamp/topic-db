"""
OccurrenceExists class. Part of the StoryTechnologies project.

July 10, 2016
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

import sqlite3

from topicdb.core.topicstoreerror import TopicStoreError


class OccurrenceExists:

    def __init__(self, database_path, map_identifier, identifier=''):
        self.database_path = database_path
        self.map_identifier = map_identifier
        self.identifier = identifier

    def execute(self):
        if self.identifier == '':
            raise TopicStoreError("Missing 'identifier' parameter")
        result = False

        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row

        cursor = connection.cursor()
        try:
            cursor.execute("SELECT identifier FROM occurrence WHERE topicmap_identifier = ? AND identifier = ?", (self.map_identifier, self.identifier))
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
