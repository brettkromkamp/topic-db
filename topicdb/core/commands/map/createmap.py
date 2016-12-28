"""
CreateMap class. Part of the StoryTechnologies project.

July 16, 2016
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

import sqlite3
import os

from topicdb.core.topicstoreerror import TopicStoreError


class CreateMap:

    def __init__(self, database_path):
        self.database_path = database_path

    def execute(self):
        connection = sqlite3.connect(self.database_path)
        definitions_file = open(
            os.path.join(os.path.dirname(__file__), '../../../conf/topicmap-definition.sql'))
        statements = definitions_file.read()

        try:
            with connection:
                for statement in statements.split(';'):
                    connection.execute(statement)
        except sqlite3.Error as error:
            raise TopicStoreError(error)
        finally:
            if connection:
                connection.close()
