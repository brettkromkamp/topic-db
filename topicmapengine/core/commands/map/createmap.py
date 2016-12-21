"""
CreateMap class. Part of the StoryTechnologies project.

July 16, 2016
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

import sqlite3

from topicmapengine.core.topicstoreerror import TopicStoreError


class CreateMap:

    def __init__(self, database_path):
        self.database_path = database_path

    def execute(self):
        connection = sqlite3.connect(self.database_path)
        definitions_file = open('/home/brettk/Source/storytechnologies/story_engine/topicmap-definition.sql')
        statements = definitions_file.read()

        try:
            with connection:  # https://docs.python.org/3/library/sqlite3.html#using-the-connection-as-a-context-manager
                for statement in statements.split(';'):
                    print(statement)  # For debugging purposes.
                    connection.execute(statement)
        except sqlite3.Error as error:
            raise TopicStoreError(error)
        finally:
            if connection:
                connection.close()
