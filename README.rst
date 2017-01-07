TopicDB from StoryTechnologies
==============================

TopicDB is a topic map-based graph (NoSQL) database.

Feature Support
---------------

- Pending

TopicDB officially supports Python 3.3–3.6.

Installation
------------

To install TopicDB, simply:

.. code-block:: bash

    $ pip install topic-db

First-Time Use
--------------

.. code-block:: python

    import os

    from topicdb.core.commands.topic.gettopic import GetTopic
    from topicdb.core.commands.topicmap.gettopicmap import GetTopicMap
    from topicdb.core.commands.topicmap.settopicmap import SetTopicMap


    DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'test-topicmap.db')
    MAP_IDENTIFIER = 1
    TITLE = 'Topic Map'
    DESCRIPTION = 'Default topic map'

    print('Creating and initializing topic map')
    SetTopicMap(DATABASE_PATH, MAP_IDENTIFIER, TITLE, DESCRIPTION).execute()

    # Rest of the code is for testing purposes (e.g., to verify that the topic map has been created
    # and that the 'entry' topic can be retrieved.
    print("\nGetting topic map")
    topic_map = GetTopicMap(DATABASE_PATH, MAP_IDENTIFIER).execute()

    print("Map identifier: [{0}]".format(topic_map.identifier))
    print("Map title: [{0}]".format(topic_map.title))
    print("Map description: [{0}]".format(topic_map.description))
    print("Map entry topic: [{0}]".format(topic_map.entry_topic_identifier))

    print("\nGetting entry topic")
    topic = GetTopic(DATABASE_PATH, MAP_IDENTIFIER, 'genesis').execute()

    print("Topic identifier: [{0}]".format(topic.identifier))
    print("Topic 'instance of': [{0}]".format(topic.instance_of))
    print("Topic (base) name: [{0}]".format(topic.first_base_name.name))

Documentation
-------------

Documentation will be available soon.

Tutorial
--------

A tutorial will be available soon.

How to Contribute
-----------------

#. Fork `the repository`_ on GitHub to start making your changes to the **master** branch (or branch off of it).
#. Write a test which shows that the bug was fixed or that the feature works as expected.
#. Send a pull request and bug the maintainer until it gets merged and published. :) Make sure to add yourself to AUTHORS_.

.. _`the repository`: https://github.com/brettkromkamp/topic_db
.. _AUTHORS: https://github.com/brettkromkamp/topic_db/blob/master/AUTHORS.rst
