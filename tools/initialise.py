"""
initialise.py file. Part of the Contextualise (https://contextualise.dev) project.

February 25, 2017
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

from topicdb.core.store.topicstore import TopicStore

MAP_IDENTIFIER = 1
USER_IDENTIFIER_1 = 1


# Instantiate the topic store, create and subsequently populate a topic map
store = TopicStore("init.db")
store.create_database()
store.create_map(USER_IDENTIFIER_1, "Test Map", "A map for testing purposes.")
store.populate_map(MAP_IDENTIFIER, USER_IDENTIFIER_1)

home_topic = store.get_topic(MAP_IDENTIFIER, "home")
for base_name in home_topic.base_names:
    print(base_name.name)
