TopicDB Tutorial
================

**Last update: January 15, 2017**

The diagram below represents a simple topic map consisting of five topics and seven associations
(that is, the relationships between the topics).

.. image:: http://www.storytechnologies.com/wp-content/uploads/2017/01/tutorial2.png

The five topics represent a family of four (Jane, Peter, John, and Mary) and the company that
employs Jane (Acme Corporation), respectively.

Let's create the accompanying topic models with TopicDB. First of all, we'll need to import the
appropriate ``Topic`` model class and subsequently create the topic objects themselves. Here goes:

.. code-block:: python

    from topicdb.core.models.topic import Topic

    acme = Topic(identifier='acme', base_name='Acme Corporation')
    jane = Topic(identifier='jane', base_name='Jane')
    john = Topic(identifier='john', base_name='John')
    peter = Topic(identifier='peter', base_name='Peter')
    mary = Topic(identifier='mary', base_name='Mary')

That's it. The accompanying topic objects have been created. The next step would be to create the
associations to establish the different kind of relationships between the topics and the roles each
topic plays in the accompanying relationship.
