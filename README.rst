TopicDB from StoryTechnologies
==============================

TopicDB is a topic map-based graph library (using `PostgreSQL`_ for persistence).

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

    from topicdb.core.store.topicstore import TopicStore
    from topicdb.core.store.retrievaloption import RetrievalOption

    from topicdb.core.models.topic import Topic
    from topicdb.core.models.language import Language

    TOPIC_MAP_IDENTIFIER = 1

    # Instantiate and open topic store.
    store = TopicStore("localhost", "username", "password")
    store.open()

    # Create the topic map and bootstrap default topics.
    store.set_topic_map(TOPIC_MAP_IDENTIFIER, "Topic Map Test")

    topic1 = Topic(identifier='test-topic1',
                   base_name='Tópico de Prueba',
                   language=Language.SPA)

    # Persist topic to store.
    if not store.topic_exists(TOPIC_MAP_IDENTIFIER, 'test-topic1'):
        store.set_topic(TOPIC_MAP_IDENTIFIER, topic1)

    # Retrieve topic from store (with the accompanying topic attributes).
    topic2 = store.get_topic(TOPIC_MAP_IDENTIFIER, 'test-topic1',
                             resolve_attributes=RetrievalOption.RESOLVE_ATTRIBUTES)

    store.close()

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

.. _PostgreSQL: https://www.postgresql.org/
.. _An Introduction to Topic Maps: https://msdn.microsoft.com/en-us/library/aa480048.aspx
.. _ISO/IEC 13250 Topic Maps: http://www.iso.org/iso/home/store/catalogue_tc/catalogue_detail.htm?csnumber=38068
.. _Story Engine: https://github.com/brettkromkamp/story_engine
.. _Interactive Scene Browser for Stories: http://www.storytechnologies.com/2016/10/interactive-scene-browser-for-stories/
.. _the repository: https://github.com/brettkromkamp/topic_db
.. _AUTHORS: https://github.com/brettkromkamp/topic_db/blob/master/AUTHORS.rst
.. _TopicDB Tutorial: https://github.com/brettkromkamp/topic_db/blob/master/TUTORIAL.rst
