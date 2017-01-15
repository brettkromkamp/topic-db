TopicDB Tutorial
================

**Last update: January 15, 2017**

Before starting with the tutorial, I strongly recommend doing the tutorial using either the
`iPython`_ REPL or `Ptpython`_ REPL. With that said, let's start.

The diagram below represents a simple topic map consisting of five topics and seven associations
(that is, the relationships between the topics).

.. image:: http://www.storytechnologies.com/wp-content/uploads/2017/01/tutorial2.png

The five topics represent the four people that make up a family (that is, *Jane*, *Peter*, *John*,
and *Mary*) and a company (*Acme Corporation*), respectively.

Let's create the accompanying topic models with TopicDB. First of all, we'll need to import the
appropriate ``Topic`` class and subsequently create the topic objects themselves. Here goes:

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

Associations, in many respects, are what make topic maps such a versatile and expressive tool to
model information and it makes sense to take a closer look at associations before we continue.

A topic map-based association is a multi-level concept. First of all, associations express a *type*
of relationship. What's more, each topic plays a role in a relationship. Actually, it's a bit more
nuanced than this: that is, associations are made up of two or more members which in turn consist of
one or more topic references. Each member has a role indicating what role the topics it contains
play within the context of the association.

Let's take a closer look at the above diagram. Jane, for example, is part of four distinct
relationships:

- The relationship of type *family* between Jane (in her role as *mother*) and Peter (her *son*).
- The relationship of type *family* between Jane (again, in her role as *mother*) and Mary (her *daughter*).
- The relationship of type *family* between Jane (in her role as *wife*) and John (her *husband*).
- The relationship of type *employment* between Jane (in her role as *employee*) and Acme Corporation (her *employer*).

Let's create the above four relationships using the ``Association`` class continuing where we left
off in the code above:

.. code-block:: python

    from topicdb.core.models.association import Association

    association1 = Association(src_topic_ref='acme',
                               src_role_spec='employer',
                               dest_topic_ref='jane',
                               dest_role_spec='employee',
                               instance_of='employment')

There is quite a lot going on in that last statement in particular. What does it all mean? We start
by importing the ``Association`` class followed by creating the actual association itself
(``association1``) by calling the constructor and passing in several keyword arguments:

* The ``src_topic_ref`` keyword indicates ...

**To be continued.**

.. _iPython: https://ipython.org/
.. _Ptpython: https://github.com/jonathanslenders/ptpython
