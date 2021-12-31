"""
initialise.py file. Part of the Contextualise (https://contextualise.dev) project.

February 25, 2017
Brett Alistair Kromkamp (brettkromkamp@gmail.com)
"""

import configparser
import os

from topicdb.core.store.topicstore import TopicStore

# Instantiate and open topic store, create and subsequently populate a topic map
store = TopicStore()
store.create_database()
store.initialise_map(
    name="Bacon Ipsum Dolor",
    description="Bacon ipsum dolor amet in ham esse sirloin turducken kevin occaecat qui kielbasa eiusmod cow anim andouille proident pig. Laborum tail id tempor voluptate.",
)
