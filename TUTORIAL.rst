TopicDB Tutorial
================

**Last update: January 15, 2017**

The diagram below represents a simple topic map consisting of five topics and seven associations
(that is, the relationships between the topics).

.. image:: http://www.storytechnologies.com/wp-content/uploads/2017/01/tutorial2.png

The five topics represent the four people that make up a family (that is, *Jane*, *Peter*, *John*,
and *Mary*) and a company (*Acme Corporation*), respectively.

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
associations to establish the different kinds of relationships between the topics and the roles each
topic plays in the accompanying relationship.

Associations, in many respects, are what make topic maps such a versatile and expressive tool to model
information and it makes sense to take a closer look at associations before we continue.

A topic map-based association is a multi-level concept. First of all, associations express a *type* of
relationship. Take a closer look at the above diagram. Jane, for example, is part of four distinct
relationships:

- Between Jane (in her role as *mother*) and Peter (her *son*).
- Between Jane (again, in her role as *mother*) and Mary (her *daughter*).
- Between Jane (in her role as *wife*) and John (her *husband*).
- Between Jane (in her role as *employee*) and Acme Corporation (her *employer*).

Each of these relationships is of a given type. In this case, three relationships are of type *family*
and one is of type *employment*.

**To be continued.**
