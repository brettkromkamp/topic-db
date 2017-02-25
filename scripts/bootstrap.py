"""
bootstrap.py file. Part of the StoryTechnologies project.

February 25, 2017
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

from topicdb.core.store.topicstore import TopicStore

store = TopicStore("localhost", 5432, "5t0ryt3ch!")
store.open()
store.set_topic_map(1, "Test Topic Map", "This is a topic map set up for testing purposes")
store.close()
