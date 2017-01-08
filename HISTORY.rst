.. :changelog:

Release History
---------------

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

- Provided ``OntologyMode`` (either ``strict`` or ``lenient``).
- Sanitized backing store (SQLite) indexes.

0.1.1 (2016-12-26)
++++++++++++++++++

**Miscellaneous**

- Initial release on PyPI (https://pypi.python.org/pypi/topic-db).
