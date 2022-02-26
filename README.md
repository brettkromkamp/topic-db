[![PyPI](https://img.shields.io/pypi/v/topic-db.svg)](https://pypi.org/project/topic-db/)
[![Python 3.x](https://img.shields.io/pypi/pyversions/topic-db.svg?logo=python&logoColor=white)](https://pypi.org/project/topic-db/)
[![GitHub open issues](https://img.shields.io/github/issues/brettkromkamp/topic-db)](https://github.com/brettkromkamp/topic-db/issues?q=is%3Aopen+is%3Aissue)
[![GitHub closed issues](https://img.shields.io/github/issues-closed/brettkromkamp/topic-db)](https://github.com/brettkromkamp/topic-db/issues?q=is%3Aissue+is%3Aclosed)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/brettkromkamp/topic-db/blob/master/LICENSE)

# TopicDB by Brett Kromkamp

TopicDB is a topic map-based graph library (using [SQLite](https://www.sqlite.org/index.html) for persistence). Topic maps provide a way to describe complex relationships between abstract concepts and real-world (information) resources.

For a more in-depth introduction to topic maps, I recommend reading the introductory article on topic maps over at MSDN: [An Introduction to Topic Maps](https://msdn.microsoft.com/en-us/library/aa480048.aspx). With that being said, although TopicDB is inspired by the topic maps paradigm, it is not (and never will be) an implementation of the [ISO/IEC 13250 Topic Maps](http://www.iso.org/iso/home/store/catalogue_tc/catalogue_detail.htm?csnumber=38068) data model standard.

TopicDB is intended to be used by other Python applications and does not provide its own user interface to the API. [Contextualise](https://github.com/brettkromkamp/contextualise), currently in active development, will provide a complete web-based user interface for TopicDB.

## Why?

I build (story) worlds and knowledge management systems. TopicDB plays a crucial role in both those endeavours.

## Feature Support

- Pending

## Installation

TopicDB officially supports Python 3.7–3.10. To install TopicDB, simply:

    $ pip install --upgrade topic-db

## Install the Development Version

If you have [Git](https://git-scm.com/) installed on your system, it is possible to install the development version of TopicDB.

Before installing the development version, you may need to uninstall the standard version of TopicDB using
``pip``:

    $ pip uninstall topic-db

Then do:

    $ git clone https://github.com/brettkromkamp/topic-db
    $ cd topic-db
    $ pip install -e .

The ``pip install -e .`` command allows you to follow the development branch as it changes by creating links in the right places and installing the command line scripts to the appropriate locations.

Then, if you want to update TopicDB at any time, in the same directory do:

    $ git pull


## How to Contribute

1. Check for open issues or open a fresh issue to start a discussion around a feature idea or a bug.
2. Fork [the repository](https://github.com/brettkromkamp/topic-db) on GitHub to start making your changes to the **master** branch (or branch off of it).
3. Write a test which shows that the bug was fixed or that the feature works as expected.
4. Send a pull request and bug the maintainer until it gets merged and published :)