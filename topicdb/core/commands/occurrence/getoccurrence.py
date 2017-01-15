"""
GetOccurrence class. Part of the StoryTechnologies project.

July 05, 2016
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

import sqlite3

from topicdb.core.commands.attribute.getattributes import GetAttributes
from topicdb.core.commands.occurrence.getoccurrencedata import GetOccurrenceData
from topicdb.core.commands.retrievaloption import RetrievalOption
from topicdb.core.commands.topicstoreerror import TopicStoreError
from topicdb.core.models.language import Language
from topicdb.core.models.occurrence import Occurrence


class GetOccurrence:

    def __init__(self, database_path, topic_map_identifier,
                 identifier='',
                 inline_resource_data=RetrievalOption.DONT_INLINE_RESOURCE_DATA,
                 resolve_attributes=RetrievalOption.DONT_RESOLVE_ATTRIBUTES,):
        self.database_path = database_path
        self.topic_map_identifier = topic_map_identifier
        self.identifier = identifier
        self.inline_resource_data = inline_resource_data
        self.resolve_attributes = resolve_attributes

    def execute(self):
        if self.identifier == '':
            raise TopicStoreError("Missing 'identifier' parameter")
        result = None

        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row

        cursor = connection.cursor()
        try:
            cursor.execute("SELECT identifier, instance_of, scope, resource_ref, topic_identifier_fk, language FROM occurrence WHERE topicmap_identifier = ? AND identifier = ?", (self.topic_map_identifier, self.identifier))
            record = cursor.fetchone()
            if record:
                resource_data = None
                if self.inline_resource_data:
                    resource_data = GetOccurrenceData(self.database_path, self.identifier).execute()
                result = Occurrence(
                    record['identifier'],
                    record['instance_of'],
                    record['topic_identifier_fk'],
                    record['scope'],
                    record['resource_ref'],
                    resource_data,
                    Language[record['language'].upper()])
                if self.resolve_attributes is RetrievalOption.RESOLVE_ATTRIBUTES:
                    result.add_attributes(GetAttributes(self.database_path,
                                                        self.topic_map_identifier,
                                                        self.identifier).execute())
        except sqlite3.Error as error:
            raise TopicStoreError(error)
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
        return result
