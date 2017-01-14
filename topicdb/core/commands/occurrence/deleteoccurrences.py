"""
DeleteOccurrences class. Part of the StoryTechnologies project.

July 13, 2016
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

import sqlite3

from topicdb.core.commands.occurrence.deleteoccurrence import DeleteOccurrence
from topicdb.core.commands.topicstoreerror import TopicStoreError


class DeleteOccurrences:

    def __init__(self, database_path, topic_map_identifier, topic_identifier=''):
        self.database_path = database_path
        self.topic_map_identifier = topic_map_identifier
        self.topic_identifier = topic_identifier

    def execute(self):
        if self.topic_identifier == '':
            raise TopicStoreError("Missing 'topic identifier' parameter")

        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row

        cursor = connection.cursor()
        try:
            connection.execute("SELECT identifier FROM occurrence WHERE topicmap_identifier = ? AND topic_identifier_fk = ?", (self.topic_map_identifier, self.topic_identifier))
            records = cursor.fetchall()
            for record in records:
                DeleteOccurrence(self.database_path, self.topic_map_identifier, record['identifier']).execute()
        except sqlite3.Error as error:
            raise TopicStoreError(error)
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
