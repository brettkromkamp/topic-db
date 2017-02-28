"""
bootstrap.py file. Part of the StoryTechnologies project.

February 25, 2017
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

from topicdb.core.store.topicstore import TopicStore

store = TopicStore("localhost", "storytech", "5t0ryt3ch!")
store.open()
store.set_topic_map(1, "The Doomsday Plans","A soldier has to steal the plans for a secret weapon.", entry_topic="outpost")
store.set_topic_map(2, "An Unexpected Meeting", "Two people meet ever so briefly.", entry_topic="cafeteria")
store.close()
