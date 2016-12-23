"""
DeleteOccurrences class. Part of the StoryTechnologies project.

July 13, 2016
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

import sqlite3

from topicdb.core.topicstoreerror import TopicStoreError
from topicdb.core.commands.occurrence.deleteoccurrence import DeleteOccurrence


class DeleteOccurrences:

    def __init__(self, database_path, map_identifier, topic_identifier=''):
        self.database_path = database_path
        self.map_identifier = map_identifier
        self.topic_identifier = topic_identifier

    def execute(self):
        if self.topic_identifier == '':
            raise TopicStoreError("Missing 'topic identifier' parameter")

        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row

        cursor = connection.cursor()
        try:
            connection.execute("SELECT identifier FROM occurrence WHERE topicmap_identifier = ? AND topic_identifier_fk = ?", (self.map_identifier, self.topic_identifier))
            records = cursor.fetchall()
            for record in records:
                # TODO: Optimize.
                DeleteOccurrence(self.database_path, self.map_identifier, record['identifier']).execute()
        except sqlite3.Error as error:
            raise TopicStoreError(error)
        finally:
            if connection:
                connection.close()
