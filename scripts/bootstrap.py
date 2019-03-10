"""
bootstrap.py file. Part of the StoryTechnologies project.

February 25, 2017
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

import configparser
import os

from topicdb.core.store.topicstore import TopicStore


SETTINGS_FILE_PATH = os.path.join(os.path.dirname(__file__), '../settings.ini')

config = configparser.ConfigParser()
config.read(SETTINGS_FILE_PATH)

database_username = config['DATABASE']['Username']
database_password = config['DATABASE']['Password']
database_name = config['DATABASE']['Database']

# Instantiate and open topic store.
with TopicStore(database_username, database_password, dbname=database_name) as store:
    store.set_topic_map(1, 1, "Topic Map 1", "Topic Map 1 description.")
    store.set_topic_map(1, 2, "Topic Map 2", "Topic Map 2 description.", public=True)

