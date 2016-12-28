"""
GetTopic class. Part of the StoryTechnologies project.

July 04, 2016
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

import sqlite3

from topicdb.core.commands.attribute.getattributes import GetAttributes
from topicdb.core.commands.occurrence.getoccurrences import GetOccurrences
from topicdb.core.commands.retrievaloption import RetrievalOption
from topicdb.core.models.basename import BaseName
from topicdb.core.models.language import Language
from topicdb.core.models.topic import Topic
from topicdb.core.topicstoreerror import TopicStoreError


class GetTopic:

    def __init__(self, database_path, map_identifier,
                 identifier='',
                 resolve_attributes=RetrievalOption.dont_resolve_attributes,
                 resolve_occurrences=RetrievalOption.dont_resolve_occurrences,
                 language=Language.eng):
        self.database_path = database_path
        self.map_identifier = map_identifier
        self.identifier = identifier
        self.resolve_attributes = resolve_attributes
        self.resolve_occurrences = resolve_occurrences
        self.language = language

    def execute(self):
        if self.identifier == '':
            raise TopicStoreError("Missing 'identifier' parameter")
        result = None

        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row

        cursor = connection.cursor()
        try:
            cursor.execute("SELECT identifier, instance_of FROM topic WHERE topicmap_identifier = ? AND identifier = ? AND scope IS NULL", (self.map_identifier, self.identifier))
            topic_record = cursor.fetchone()
            if topic_record:
                result = Topic(topic_record['identifier'], topic_record['instance_of'])
                result.clear_base_names()
                cursor.execute("SELECT name, language, identifier FROM basename WHERE topicmap_identifier = ? AND topic_identifier_fk = ?",
                               (self.map_identifier,
                                self.identifier))
                base_name_records = cursor.fetchall()
                if base_name_records:
                    for base_name_record in base_name_records:
                        result.add_base_name(
                            BaseName(base_name_record['name'],
                                     Language[base_name_record['language']],
                                     base_name_record['identifier']))
                if self.resolve_attributes is RetrievalOption.resolve_attributes:
                    result.add_attributes(GetAttributes(self.database_path, self.map_identifier,
                                                        self.identifier).execute())
                if self.resolve_occurrences is RetrievalOption.resolve_occurrences:
                    result.add_occurrences(GetOccurrences(self.database_path, self.map_identifier,
                                                          self.identifier).execute())
        except sqlite3.Error as error:
            raise TopicStoreError(error)
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
        return result
