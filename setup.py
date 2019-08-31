"""
setup.py file. Part of the StoryTechnologies project.

December 21, 2016
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    README = f.read()

with open(os.path.join(here, 'HISTORY.rst'), encoding='utf-8') as f:
    HISTORY = f.read()

setup(name='topic-db',
      version='1.0.0',  # Bump version NUMBER *after* starting (git flow) release.
      description='TopicDB is a topic map-based graph library (using PostgreSQL for persistence).',
      long_description=README + '\n\n' + HISTORY,
      keywords='topic map, concept map, graph database, semantic, knowledge management, unstructured data',
      url='https://github.com/brettkromkamp/topic_db',
      author='Brett Alistair Kromkamp',
      author_email='brett.kromkamp@gmail.com',
      license='MIT',
      packages=find_packages(exclude=['docs', 'tests*', 'scripts']),
      package_data={'': ['LICENSE']},
      install_requires=['psycopg2', 'python-slugify', 'typed-tree'],
      include_package_data=True,
      zip_safe=False,
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: English',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: Implementation :: CPython',
          'Topic :: Software Development :: Libraries :: Python Modules'
      ])
