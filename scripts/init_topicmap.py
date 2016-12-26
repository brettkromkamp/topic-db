#!/usr/bin/env python

"""
Initialize topic map (command-line) script. Part of the StoryTechnologies project.

December 22, 2016
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

import os

from topicdb.core.commands.map.createmap import CreateMap
from topicdb.core.commands.map.initmap import InitMap
from topicdb.core.commands.topic.topicexists import TopicExists


DATABASE_PATH = os.path.join(os.path.dirname(__file__), '../data/topicmap.db')
MAP_IDENTIFIER = 1

# Create database schema.
if not os.path.isfile(DATABASE_PATH):
    CreateMap(DATABASE_PATH).execute()

# Bootstrap default topic map (ontology).
if not TopicExists(DATABASE_PATH, MAP_IDENTIFIER, 'genesis').execute():
    InitMap(DATABASE_PATH, MAP_IDENTIFIER).execute()
