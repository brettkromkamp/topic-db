TopicDB by Brett Kromkamp
=========================

TopicDB is a topic map-based graph library (using `SQLite`_ for persistence). Topic maps provide a way to describe complex relationships between abstract concepts and real-world (information) resources.

.. image:: resources/topic-maps.png
   :alt: Topic maps with topics, associations and occurrences

*Topic maps with topics, associations and occurrences*

For a more in-depth introduction to topic maps, I recommend reading the introductory article on topic maps over at MSDN: `An Introduction to Topic Maps`_. With that being said, although TopicDB is inspired by the topic maps
paradigm, it is not (and never will be) an implementation of the `ISO/IEC 13250 Topic Maps`_ data model standard.

TopicDB is intended to be used by other Python applications and does not provide its own user interface to the API. `Contextualise`_, currently in active development, will provide a complete web-based user interface for TopicDB.

Why?
----

I build (story) worlds and knowledge management systems. TopicDB plays a crucial role in both those endeavours.

Feature Support
---------------

- Pending

Installation
------------

TopicDB officially supports Python 3.6–3.10. To install TopicDB, simply::

    $ pip install topic-db

Install the Development Version
-------------------------------

If you have `Git <https://git-scm.com/>`_ installed on your system, it is possible to install the development version of TopicDB.

Before installing the development version, you may need to uninstall the standard version of TopicDB using
``pip``::

    $ pip uninstall topic-db

Then do::

    $ git clone https://github.com/brettkromkamp/topic-db
    $ cd topic-db
    $ pip install -e .

The ``pip install -e .`` command allows you to follow the development branch as it changes by creating links in the right places and installing the command line scripts to the appropriate locations.

Then, if you want to update TopicDB at any time, in the same directory do::

    $ git pull

Documentation
-------------

Documentation will be available soon.

How to Contribute
-----------------

#. Check for open issues or open a fresh issue to start a discussion around a feature idea or a bug.
#. Fork `the repository`_ on GitHub to start making your changes to the **master** branch (or branch off of it).
#. Write a test which shows that the bug was fixed or that the feature works as expected.
#. Send a pull request and bug the maintainer until it gets merged and published. :) Make sure to add yourself to AUTHORS_.

.. _SQLite: https://www.sqlite.org/index.html
.. _An Introduction to Topic Maps: https://msdn.microsoft.com/en-us/library/aa480048.aspx
.. _ISO/IEC 13250 Topic Maps: http://www.iso.org/iso/home/store/catalogue_tc/catalogue_detail.htm?csnumber=38068
.. _the repository: https://github.com/brettkromkamp/topic-db
.. _Contextualise: https://github.com/brettkromkamp/contextualise
.. _AUTHORS: https://github.com/brettkromkamp/topic-db/blob/master/AUTHORS.rst
