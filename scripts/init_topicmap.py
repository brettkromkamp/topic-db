#!/usr/bin/env python

"""
Initialize topic topicmap (command-line) script. Part of the StoryTechnologies project.

December 22, 2016
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

import os

from topicdb.core.commands.topic.gettopic import GetTopic
from topicdb.core.commands.topicmap.gettopicmap import GetTopicMap
from topicdb.core.commands.topicmap.settopicmap import SetTopicMap


DATABASE_PATH = os.path.join(os.path.dirname(__file__), '../data/topicmap.db')
TOPIC_MAP_IDENTIFIER = 1
TITLE = 'Topic Map'
DESCRIPTION = 'Default topic map'

print('Creating and initializing topic map')
SetTopicMap(DATABASE_PATH, TOPIC_MAP_IDENTIFIER, TITLE, DESCRIPTION).execute()

print("\nGetting topic map")
topic_map = GetTopicMap(DATABASE_PATH, TOPIC_MAP_IDENTIFIER).execute()

print("Map identifier: [{0}]".format(topic_map.identifier))
print("Map title: [{0}]".format(topic_map.title))
print("Map description: [{0}]".format(topic_map.description))
print("Map entry topic: [{0}]".format(topic_map.entry_topic_identifier))

print("\nGetting entry topic")
topic = GetTopic(DATABASE_PATH, TOPIC_MAP_IDENTIFIER, 'genesis').execute()

print("Topic identifier: [{0}]".format(topic.identifier))
print("Topic 'instance of': [{0}]".format(topic.instance_of))
print("Topic (base) name: [{0}]".format(topic.first_base_name.name))

