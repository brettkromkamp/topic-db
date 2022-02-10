"""
setup.py file. Part of the Contextualise (https://contextualise.dev) project.

December 21, 2016
Brett Alistair Kromkamp (brettkromkamp@gmail.com)
"""

import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "README.rst"), encoding="utf-8") as f:
    README = f.read()
with open(os.path.join(here, "HISTORY.rst"), encoding="utf-8") as f:
    HISTORY = f.read()
with open(os.path.join(here, "requirements.txt"), encoding="utf-8") as f:
    REQUIRED = f.read().splitlines()

setup(
    name="topic-db",
    version="2.0.0",  # Bump version NUMBER *after* starting (git flow) release.
    description="TopicDB is a topic map-based graph store (using SQLite for persistence).",
    long_description=README + "\n\n" + HISTORY,
    keywords="topic map, concept map, graph database, graph store, semantic, knowledge management, unstructured data, sqlite",
    url="https://github.com/brettkromkamp/topic-db",
    author="Brett Alistair Kromkamp",
    author_email="brett.kromkamp@gmail.com",
    license="MIT",
    packages=find_packages(exclude=["tests*", "tools"]),
    package_data={"": ["LICENSE"]},
    include_package_data=True,
    zip_safe=False,
    install_requires=REQUIRED,
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
