"""
initialise.py file. Part of the Contextualise (https://contextualise.dev) project.

February 25, 2017
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

import configparser
import os

from topicdb.core.store.topicstore import TopicStore

# Instantiate and open topic store, create and subsequently populate topic maps
with TopicStore() as store:
    store.set_topic_map(
        "Bacon Ipsum Dolor",
        "Bacon ipsum dolor amet in ham esse sirloin turducken kevin occaecat qui kielbasa eiusmod cow anim andouille proident pig. Laborum tail id tempor voluptate.",
    )

    store.initialise_map()
