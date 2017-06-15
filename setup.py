"""
setup.py file. Part of the StoryTechnologies project.

December 21, 2016
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

from setuptools import setup, find_packages

with open('README.rst', encoding='utf-8') as f:
    readme = f.read()

with open('HISTORY.rst', encoding='utf-8') as f:
    history = f.read()

setup(name='topic-db',
      version='0.7.0',  # Bump version NUMBER *after* starting (git flow) release.
      description='TopicDB is a topic map-based graph library (using PostgreSQL for persistence).',
      long_description=readme + '\n\n' + history,
      keywords='topic map, concept map, graph database, semantic, knowledge management, unstructured data',
      url='https://github.com/brettkromkamp/topic_db',
      author='Brett Alistair Kromkamp',
      author_email='brett.kromkamp@gmail.com',
      license='MIT',
      packages=find_packages(exclude=['docs', 'tests*', 'scripts']),
      package_data={'': ['LICENSE']},
      install_requires=['psycopg2', 'python-slugify'],
      include_package_data=True,
      zip_safe=False,
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: English',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: Implementation :: CPython',
          'Topic :: Software Development :: Libraries :: Python Modules'
      ])
