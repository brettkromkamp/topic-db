"""
bootstrap.py file. Part of the StoryTechnologies project.

February 25, 2017
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

import configparser
import os

from topicdb.core.store.topicstore import TopicStore


SETTINGS_FILE_PATH = os.path.join(os.path.dirname(__file__), '../settings.ini')
USER_IDENTIFIER_1 = 1
USER_IDENTIFIER_2 = 4

config = configparser.ConfigParser()
config.read(SETTINGS_FILE_PATH)

database_username = config['DATABASE']['Username']
database_password = config['DATABASE']['Password']
database_name = config['DATABASE']['Database']

# Instantiate and open topic store, create and subsequently populate topic maps.
with TopicStore(database_username, database_password, dbname=database_name) as store:
    store.set_topic_map(USER_IDENTIFIER_1, "Topic Map 1", "Topic Map 1 description.")
    store.set_topic_map(USER_IDENTIFIER_1, "Topic Map 2", "Topic Map 2 description.", public=True)
    store.set_topic_map(USER_IDENTIFIER_2, "Topic Map 3", "Topic Map 3 description.")

    # Populate topic maps (with pre-defined topics) for "USER_IDENTIFIER_1".
    for topic_map in store.get_topic_maps(USER_IDENTIFIER_1):
        store.populate_topic_map(topic_map.identifier)

    # Populate topic maps (with pre-defined topics) for "USER_IDENTIFIER_2".
    for topic_map in store.get_topic_maps(USER_IDENTIFIER_2):
        store.populate_topic_map(topic_map.identifier)
