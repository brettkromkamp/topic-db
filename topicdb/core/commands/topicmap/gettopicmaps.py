"""
GetTopicMaps class. Part of the StoryTechnologies project.

January 07, 2017
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

import sqlite3

from topicdb.core.commands.topicstoreerror import TopicStoreError
from topicdb.core.models.topicmap import TopicMap


class GetTopicMaps:

    def __init__(self, database_path):
        self.database_path = database_path

    def execute(self):
        result = []

        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row

        cursor = connection.cursor()
        try:
            cursor.execute("SELECT * FROM topicmap ORDER BY identifier")
            records = cursor.fetchall()
            for record in records:
                topic_map = TopicMap(
                    record['title'],
                    record['topicmap_identifier_fk'],
                    record['entry_identifier_fk'],
                    record['description'])
                topic_map.identifier = record['identifier']
                result.append(topic_map)
        except sqlite3.Error as error:
            raise TopicStoreError(error)
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
        return result
