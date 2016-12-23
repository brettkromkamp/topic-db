"""
Topic map API functions. Part of the StoryTechnologies project.

December 22, 2016
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

import os
import base64
import functools

from topicdb.core.commands.association.getassociation import GetAssociation
from topicdb.core.commands.association.getassociationgroups import GetAssociationGroups
from topicdb.core.commands.attribute.getattributes import GetAttributes
from topicdb.core.commands.attribute.getattribute import GetAttribute
from topicdb.core.commands.occurrence.getoccurrence import GetOccurrence
from topicdb.core.commands.occurrence.getoccurrences import GetOccurrences
from topicdb.core.commands.topic.gettopic import GetTopic
from topicdb.core.commands.topic.gettopicidentifiers import GetTopicIdentifiers
from topicdb.core.commands.topic.gettopics import GetTopics
from topicdb.core.commands.topic.gettopicshierarchy import GetTopicsHierarchy
from topicdb.core.retrievaloption import RetrievalOption


DATABASE_PATH = os.path.join(os.path.dirname(__file__), '../../data/topicmap.db')


def get_topic_identifiers(map_identifier, query, offset=0, limit=100, filter_entities=RetrievalOption.filter_entities):
    # TODO: Implement 'filter entities' switch.
    result = GetTopicIdentifiers(DATABASE_PATH, map_identifier, query, filter_entities, offset, limit).execute()
    if result:
        return result, 200
    else:
        return "Not found", 404


@functools.lru_cache(maxsize=64)
def get_topic(map_identifier, identifier):
    topic = GetTopic(DATABASE_PATH, map_identifier, identifier, RetrievalOption.resolve_attributes).execute()
    if topic:
        attributes = []
        base_names = []
        for attribute in topic.attributes:
            attributes.append({
                'identifier': attribute.identifier,
                'name': attribute.name,
                'value': attribute.value,
                'dataType': attribute.data_type.name,
                'scope': attribute.scope,
                'language': attribute.language.name
            })
        for base_name in topic.base_names:
            base_names.append({
                'identifier': base_name.identifier,
                'name': base_name.name,
                'language': base_name.language.name
            })
        result = {
            'topic': {
                'identifier': topic.identifier,
                'firstBaseName': topic.first_base_name.name,
                'baseNames': base_names,
                'instanceOf': topic.instance_of,
                'attributes': attributes
            }
        }
        return result, 200
    else:
        return "Not found", 404


def get_topics(map_identifier, instance_of='topic', offset=0, limit=100):
    topics = GetTopics(DATABASE_PATH, map_identifier, instance_of=instance_of, offset=offset, limit=limit).execute()
    if topics:
        result = []
        for topic in topics:
            attributes = []
            base_names = []
            for attribute in topic.attributes:
                attributes.append({
                    'identifier': attribute.identifier,
                    'name': attribute.name,
                    'value': attribute.value,
                    'dataType': attribute.data_type.name,
                    'scope': attribute.scope,
                    'language': attribute.language.name
                })
            for base_name in topic.base_names:
                base_names.append({
                    'identifier': base_name.identifier,
                    'name': base_name.name,
                    'language': base_name.language.name
                })
            topic_json = {
                'topic': {
                    'identifier': topic.identifier,
                    'firstBaseName': topic.first_base_name.name,
                    'baseNames': base_names,
                    'instanceOf': topic.instance_of,
                    'attributes': attributes
                }
            }
            result.append(topic_json)
        return result, 200
    else:
        return "Not found", 404


def get_topics_hierarchy(map_identifier, identifier):

    def build_topics_hierarchy(inner_identifier):
        # JSON data structure suitable for the RGraph visualization from the
        # JavaScript InfoViz Toolkit (https://philogb.github.io/jit/)

        parent_identifier = tree[inner_identifier].parent
        base_name = tree[inner_identifier].topic.first_base_name.name
        instance_of = tree[inner_identifier].topic.instance_of
        children = tree[inner_identifier].children

        if instance_of == 'scene':
            node_data = {
                '$color': '#00ff00'
            }
        elif instance_of == 'character':
            node_data = {
                '$color': '#ff0000'
            }
        elif instance_of == 'prop':
            node_data = {
                '$color': '#0000ff'
            }
        else:
            node_data = {
                '$color': '#a6a6a6'
            }

        node = {
            'id': inner_identifier,
            'name': base_name,
            'instanceOf': instance_of,
            'data': node_data,
            'children': []
        }
        result[inner_identifier] = node

        if parent_identifier is not None:
            parent = result[parent_identifier]
            parent_children = parent['children']
            parent_children.append(node)
            parent['children'] = parent_children

        for child in children:
            build_topics_hierarchy(child)

    tree = GetTopicsHierarchy(DATABASE_PATH, map_identifier, identifier).execute()
    if len(tree) > 1:
        result = {}
        build_topics_hierarchy(identifier)
        return result[identifier], 200
    else:
        return "Not found", 404


@functools.lru_cache(maxsize=64)
def get_occurrence(map_identifier, identifier, inline_resource_data=RetrievalOption.dont_inline_resource_data):
    occurrence = GetOccurrence(DATABASE_PATH, map_identifier, identifier, inline_resource_data).execute()
    if occurrence:
        # TODO: Implementation.
        return "Occurrence found", 200
    else:
        return "Not found", 404


def get_occurrences(map_identifier, identifier,
                    inline_resource_data=RetrievalOption.dont_inline_resource_data,
                    resolve_attributes=RetrievalOption.dont_resolve_attributes,
                    instance_of=''):
    occurrences = GetOccurrences(DATABASE_PATH, map_identifier, identifier, inline_resource_data, resolve_attributes, instance_of).execute()
    if occurrences:
        result = []
        for occurrence in occurrences:
            attributes = []
            for attribute in occurrence.attributes:
                attributes.append({
                    'identifier': attribute.identifier,
                    'name': attribute.name,
                    'value': attribute.value,
                    'dataType': attribute.data_type.name,
                    'scope': attribute.scope,
                    'language': attribute.language.name
                })
            if occurrence.resource_data is None:
                resource_data = None
            else:
                resource_data = base64.b64encode(occurrence.resource_data).decode('utf-8')
            occurrence_json = {
                'occurrence': {
                    'identifier': occurrence.identifier,
                    'instanceOf': occurrence.instance_of,
                    'scope': occurrence.scope,
                    'resourceRef': occurrence.resource_ref,
                    'resourceData': resource_data,
                    'language': occurrence.language.name,
                    'attributes': attributes
                }
            }
            result.append(occurrence_json)
        return result, 200
    else:
        return "Not found", 404


@functools.lru_cache(maxsize=64)
def get_association(map_identifier, identifier):
    association = GetAssociation(DATABASE_PATH, map_identifier, identifier).execute()
    if association:
        # TODO: Implementation.
        return "Association found", 200
    else:
        return "Not found", 404


def get_associations(map_identifier, identifier):
    associations = GetAssociationGroups(DATABASE_PATH, map_identifier, identifier).execute()
    if len(associations):
        level1 = []
        for instance_of in associations.dict:
            level2 = []
            for role in associations.dict[instance_of]:
                level3 = []
                for topic_ref in associations[instance_of, role]:
                    topic3 = GetTopic(DATABASE_PATH, map_identifier, topic_ref).execute()
                    level3.append({'text': topic3.first_base_name.name, 'href': topic_ref, 'instanceOf': instance_of})
                topic2 = GetTopic(DATABASE_PATH, map_identifier, role).execute()
                level2.append({'text': topic2.first_base_name.name, 'nodes': level3})
            topic1 = GetTopic(DATABASE_PATH, map_identifier, instance_of).execute()
            level1.append({'text': topic1.first_base_name.name, 'nodes': level2})
        return level1, 200
    else:
        return "Not found", 404


@functools.lru_cache(maxsize=64)
def get_attribute(map_identifier, identifier):
    attribute = GetAttribute(DATABASE_PATH, map_identifier, identifier).execute()
    if attribute:
        # TODO: Implementation.
        return "Attribute found", 200
    else:
        return "Not found", 404


def get_attributes(map_identifier, identifier):
    attributes = GetAttributes(DATABASE_PATH, map_identifier, identifier).execute()
    if attributes:
        # TODO: Implementation.
        return "Attributes found", 200
    else:
        return "Not found", 404
