"""
initialise.py file. Part of the Contextualise (https://contextualise.dev) project.

February 25, 2017
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

import configparser
import os

from topicdb.core.store.topicstore import TopicStore

SETTINGS_FILE_PATH = os.path.join(os.path.dirname(__file__), "../settings.ini")
USER_IDENTIFIER_1 = 1

config = configparser.ConfigParser()
config.read(SETTINGS_FILE_PATH)

database_username = config["DATABASE"]["Username"]
database_password = config["DATABASE"]["Password"]
database_name = config["DATABASE"]["Database"]
database_host = config["DATABASE"]["Host"]
database_port = config["DATABASE"]["Port"]

# Instantiate and open topic store, create and subsequently populate topic maps
with TopicStore(
    database_username,
    database_password,
    host=database_host,
    port=database_port,
    dbname=database_name,
) as store:
    store.set_topic_map(
        USER_IDENTIFIER_1,
        "Bacon Ipsum Dolor",
        "Bacon ipsum dolor amet in ham esse sirloin turducken kevin occaecat qui kielbasa eiusmod cow anim andouille proident pig. Laborum tail id tempor voluptate.",
    )

    # Populate topic maps (with pre-defined topics) for 'USER_IDENTIFIER_1'
    for topic_map in store.get_topic_maps(USER_IDENTIFIER_1):
        store.initialise_topic_map(topic_map.identifier)
