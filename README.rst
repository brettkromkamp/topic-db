TopicDB from StoryTechnologies
==============================

TopicDB is a topic map-based graph library (and, currently using SQLite for persistence).

.. image:: http://www.storytechnologies.com/wp-content/uploads/2016/12/topic-db-logo.png

For a more in-depth introduction to topic maps, I recommend reading the excellent introductory
article on topic maps over at MSDN: `An Introduction to Topic Maps`_. With that being said, although
TopicDB is inspired by the topic maps paradigm, it is not (and never will be) an implementation of
the `ISO/IEC 13250 Topic Maps`_ data model standard.

TopicDB is intended to be used by other Python applications, and currently does not provide a web
interface to the API. `Story Engine`_ is a good example of TopicDB being used by another
application.

Why?
----

I build (story) worlds. TopicDB plays a crucial role in that endeavour: `Interactive Scene Browser for Stories`_.

Feature Support
---------------

- Pending

Installation
------------

TopicDB officially supports Python 3.3–3.6. To install TopicDB, simply:

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
    TOPIC_MAP_IDENTIFIER = 1
    TITLE = 'Topic Map'
    DESCRIPTION = 'Default topic map'

    print('Creating and initializing topic map')
    SetTopicMap(DATABASE_PATH, TOPIC_MAP_IDENTIFIER, TITLE, DESCRIPTION).execute()

    # Rest of the code is for testing purposes (e.g., to verify that the topic map has been created
    # and that the 'entry' topic can be retrieved.
    print("\nGetting topic map")
    topic_map = GetTopicMap(DATABASE_PATH, TOPIC_MAP_IDENTIFIER).execute()

    print("Map identifier: [{0}]".format(topic_map.identifier))
    print("Map title: [{0}]".format(topic_map.title))
    print("Map description: [{0}]".format(topic_map.description))
    print("Map entry topic: [{0}]".format(topic_map.entry_topic_identifier))

    print("\nGetting entry topic")
    topic = GetTopic(DATABASE_PATH, TOPIC_MAP_IDENTIFIER, 'genesis').execute()

    print("Topic identifier: [{0}]".format(topic.identifier))
    print("Topic 'instance of': [{0}]".format(topic.instance_of))
    print("Topic (base) name: [{0}]".format(topic.first_base_name.name))

Tutorial
--------

To get a better understanding of how to use TopicDB, check out the tutorial, here: `TopicDB Tutorial`_ (work-in-progress).

Documentation
-------------

Documentation will be available soon.

How to Contribute
-----------------

#. Fork `the repository`_ on GitHub to start making your changes to the **master** branch (or branch off of it).
#. Write a test which shows that the bug was fixed or that the feature works as expected.
#. Send a pull request and bug the maintainer until it gets merged and published. :) Make sure to add yourself to AUTHORS_.

.. _An Introduction to Topic Maps: https://msdn.microsoft.com/en-us/library/aa480048.aspx
.. _ISO/IEC 13250 Topic Maps: http://www.iso.org/iso/home/store/catalogue_tc/catalogue_detail.htm?csnumber=38068
.. _Story Engine: https://github.com/brettkromkamp/story_engine
.. _Interactive Scene Browser for Stories: http://www.storytechnologies.com/2016/10/interactive-scene-browser-for-stories/
.. _the repository: https://github.com/brettkromkamp/topic_db
.. _AUTHORS: https://github.com/brettkromkamp/topic_db/blob/master/AUTHORS.rst
.. _TopicDB Tutorial: https://github.com/brettkromkamp/topic_db/blob/master/TUTORIAL.rst
