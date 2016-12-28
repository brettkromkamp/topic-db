"""
setup.py file. Part of the StoryTechnologies project.

December 21, 2016
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

from setuptools import setup, find_packages

setup(name='topic-db',
      version='0.2.0',  # Bump version number *after* starting (git flow) release.
      description='TopicDB is a topic map-based graph (NoSQL) database',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: English',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: Implementation :: CPython',
          'Topic :: Database :: Database Engines/Servers',
          'Topic :: Software Development :: Libraries :: Python Modules'
      ],
      keywords='topic map, graph database, nosql, semantic, concept map, knowledge management',
      url='https://github.com/brettkromkamp/topic_db',
      author='Brett Alistair Kromkamp',
      author_email='brett.kromkamp@gmail.com',
      license='MIT',
      packages=find_packages(exclude=['docs', 'tests*', 'scripts']),
      install_requires=['python-slugify'],
      include_package_data=True,
      zip_safe=False)
