TopicDB Tutorial
================

The diagram below represents a simple topic map consisting of five topics and seven associations
(that is, the relationships between the topics).

.. image:: http://www.storytechnologies.com/wp-content/uploads/2017/01/tutorial2.png

The five topics represent a family of four (Jane, Peter, John, and Mary) and the company that
employs Jane (Acme Corporation), respectively.

Let's create the accompanying topic models with TopicDB. First of all, we'll need to import the appropriate
model classes and create (all of) the topic objects. Here goes:

.. code-block:: python

    from topicdb.core.models.topic import Topic

    acme = Topic(identifier='acme', base_name='Acme Corporation')
    jane = Topic(identifier='jane', base_name='Jane')
    acme = Topic(identifier='john', base_name='John')
    acme = Topic(identifier='peter', base_name='Peter')
    acme = Topic(identifier='mary', base_name='Mary')

That's it. The accompanying topic models have been created. The ``identifier`` parameter is what we'll
be using to reference the accompanying topic model when establishing one or more relationships between
topics (by means of associations, in topic map terminology).
