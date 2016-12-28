TopicDB from StoryTechnologies
==============================

TopicDB is a topic map-based graph (NoSQL) database.

Why?
----

I want to build my own (virtual) worlds. TopicDB is a crucial component to allow me to do just that: `Interactive Scene Browser for Stories <http://www.storytechnologies.com/2016/10/interactive-scene-browser-for-stories/>`_.

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

    from topicdb.core.commands.map.createmap import CreateMap
    from topicdb.core.commands.map.initmap import InitMap
    from topicdb.core.commands.topic.topicexists import TopicExists
    from topicdb.core.commands.topic.gettopic import GetTopic


    # Set constants.
    DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'test-topicmap.db')
    MAP_IDENTIFIER = 1

    # Create database schema.
    if not os.path.isfile(DATABASE_PATH):
        CreateMap(DATABASE_PATH).execute()

    # Bootstrap default topics.
    if not TopicExists(DATABASE_PATH, MAP_IDENTIFIER, 'genesis').execute():
        InitMap(DATABASE_PATH, MAP_IDENTIFIER).execute()

    # Retrieve "Genesis" topic (with the accompanying topic identifier in lower case
    # for the purpose of testing).
    topic = GetTopic(DATABASE_PATH, MAP_IDENTIFIER, 'genesis').execute()
    print(topic.identifier)
    print(topic.instance_of)
    print(topic.first_base_name.name)

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
.. _`story engine`: https://github.com/brettkromkamp/story_engine
.. _`story engine`: http://www.storytechnologies.com/2016/10/interactive-scene-browser-for-stories/
