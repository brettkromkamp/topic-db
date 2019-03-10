.. :changelog:

Release History
---------------

0.8.0 (2019-03-10)
++++++++++++++++++

**Improvements**

- Extended functionality in relation to the management of the top-level topic map objects. This resulted in changes in both the ``TopicMap`` and ``TopicStore`` classes, respectively.
- Refactored and cleaned-up the definition of the database schema (including a change in the naming convention of field names).
- Updated dependencies (to latest versions).

0.7.1 (2017-06-16)
++++++++++++++++++

**Improvements**

- Refactored code base (specifically, the unit tests) to use the topic store as a context manager.
- Updated ``pytest`` dependency (to latest version).

**Bugs**

- Fixed a context manager-related bug (in the ``TopicStore`` class).

0.7.0 (2017-06-15)
++++++++++++++++++

**Improvements**

- Various (API) improvements and fixes throughout the codebase (specifically, the ``TopicStore`` class) resulting in the bump of the project's development status (now *Beta*).

0.6.0 (2017-03-04)
++++++++++++++++++

**Improvements**

- Moved away from SQLite to PostgreSQL as the persistence store.
- Moved away from the 'command' pattern to the 'repository' pattern.

0.5.0 (2017-01-15)
++++++++++++++++++

**Improvements**

- Refactored ``Get*`` command classes (i.e., ``instance_of``, ``scope``, and ``language`` parameters) for the purposes of consistency and flexibility.
- Removed hard-code ``maximum-depth`` in ``GetTopicsHierarchy`` command class.
- Renamed several command classes to more accurately reflect their purpose.
- Refactored code to ensure better compliance with PEP 8 (Style Guide for Python Code).

**Bugs**

- Fixed several command classes with regards to not closing SQLite ``cursor`` objects.

0.4.0 (2017-01-08)
++++++++++++++++++

**Improvements**

- Renamed ``GetAssociations`` command class to ``GetTopicAssociations``.
- Refactored topic map-related commands and models, including changes to the topic map definition (SQL).
- Renamed several (important) variables for the purpose of improving clarity and consistency.

0.3.0 (2016-12-30)
++++++++++++++++++

**Improvements**

- Added functionality to delete associations (i.e., ``DeleteAssociation`` command class).

0.2.0 (2016-12-28)
++++++++++++++++++

**Improvements**

- Provided ``OntologyMode`` (either ``STRICT`` or ``LENIENT``).
- Sanitized backing store (SQLite) indexes.

0.1.1 (2016-12-26)
++++++++++++++++++

**Miscellaneous**

- Initial release on PyPI (https://pypi.python.org/pypi/topic-db).
