"""
GetOccurrence class. Part of the StoryTechnologies project.

July 05, 2016
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

import sqlite3

from topicmapengine.core.topicstoreerror import TopicStoreError
from topicmapengine.core.retrievaloption import RetrievalOption
from topicmapengine.core.commands.occurrence.getoccurrencedata import GetOccurrenceData
from topicmapengine.core.commands.attribute.getattributes import GetAttributes
from topicmapengine.core.models.occurrence import Occurrence
from topicmapengine.core.models.language import Language


class GetOccurrence:

    def __init__(self, database_path, map_identifier,
                 identifier='',
                 inline_resource_data=RetrievalOption.dont_inline_resource_data,
                 resolve_attributes=RetrievalOption.dont_resolve_attributes,
                 language=Language.eng):
        self.database_path = database_path
        self.map_identifier = map_identifier
        self.identifier = identifier
        self.inline_resource_data = inline_resource_data
        self.resolve_attributes = resolve_attributes
        self.language = language

    def execute(self):
        if self.identifier == '':
            raise TopicStoreError("Missing 'identifier' parameter")
        result = None

        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row

        cursor = connection.cursor()
        try:
            cursor.execute("SELECT identifier, instance_of, scope, resource_ref, topic_identifier_fk, language FROM occurrence WHERE topicmap_identifier = ? AND identifier = ?", (self.map_identifier, self.identifier))
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
                    Language[record['language']])
                if self.resolve_attributes is RetrievalOption.resolve_attributes:
                    # TODO: Optimize.
                    result.add_attributes(GetAttributes(self.database_path, self.map_identifier, self.identifier, self.language).execute())
        except sqlite3.Error as error:
            raise TopicStoreError(error)
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
        return result
