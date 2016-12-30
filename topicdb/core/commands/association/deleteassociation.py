"""
DeleteAssociation class. Part of the StoryTechnologies project.

December 30, 2016
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

import sqlite3


class DeleteAssociation:

    def __init__(self, database_path, map_identifier):
        self.database_path = database_path
        self.map_identifier = map_identifier

    def execute(self):
        pass
