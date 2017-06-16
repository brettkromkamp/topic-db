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

username = config['DATABASE']['Username']
password = config['DATABASE']['Password']

# Instantiate and open topic store.
with TopicStore(username, password) as store:

    store.set_topic_map(1, "The Doomsday Weapon", "A soldier has to infiltrate behind enemy lines to steal the plans for a secret doomsday weapon.")
    store.set_topic_map(2, "An Unexpected Meeting", "Two people meet ever so briefly. A chance encounter that changes their lives forever.")
