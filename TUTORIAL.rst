TopicDB Tutorial
================

TopicDB is a topic map-based graph library (using `PostgreSQL`_ for persistence).

**Last update: February 21, 2017**

Before starting with the tutorial, I recommend installing either the `iPython`_ or `Ptpython`_ REPLs
(if you haven't already). By no means are either of these REPLs a pre-requisite for doing the
tutorial. Nonetheless, using them does make Python's interactive experience much more pleasant. With
that said, let's start.

The five topics represent the four people that make up a family (that is, *Jane*, *Peter*, *John*,
and *Mary*) and a company (*Acme Corporation*), respectively.

Let's create the accompanying topic models with TopicDB. First of all, we'll need to import the
appropriate ``Topic`` class and subsequently create the topic objects. Here goes:

.. code-block:: python

    from topicdb.core.models.topic import Topic

    acme = Topic(identifier='acme', base_name='Acme Corporation')
    jane = Topic(identifier='jane', base_name='Jane')
    john = Topic(identifier='john', base_name='John')
    peter = Topic(identifier='peter', base_name='Peter')
    mary = Topic(identifier='mary', base_name='Mary')

The next step would be to create the associations to establish the different kinds of relationships
between the topics and the roles each topic plays in the accompanying relationship.

Associations, in many respects, are what make topic maps such a versatile and expressive tool to
model information and it makes sense to take a closer look at associations before we continue.

A topic map-based association is a multi-level concept. First of all, associations express a *type*
of relationship. What's more, each topic plays a role in a relationship. Actually, it's a bit more
nuanced than that: associations are made up of two or more members which in turn consist of one or
more topic references. Each member has a role indicating what role the topics it contains play
within the context of the association.

Let's take a closer look at the above diagram. Jane, for example, is part of four distinct
relationships:

- The relationship of type *family* between Jane (in her role as *mother*) and Peter (her *son*).
- The relationship of type *family* between Jane (again, in her role as *mother*) and Mary (her *daughter*).
- The relationship of type *family* between Jane (in her role as *wife*) and John (her *husband*).
- The relationship of type *employment* between Jane (in her role as *employee*) and Acme Corporation (her *employer*).

Let's create the above four relationships using the ``Association`` class:

.. code-block:: python

    from topicdb.core.models.association import Association

    association1 = Association(src_topic_ref='acme',
                               src_role_spec='employer',
                               dest_topic_ref='jane',
                               dest_role_spec='employee',
                               instance_of='employment')

We start by importing the ``Association`` class followed by creating an association
(``association1``) object by calling the constructor and passing in several keyword arguments. Let's
look at each keyword argument in turn:

* The ``src_topic_ref`` keyword indicates ...

**To be continued.**

.. _PostgreSQL: https://www.postgresql.org/
.. _iPython: https://ipython.org/
.. _Ptpython: https://github.com/jonathanslenders/ptpython
