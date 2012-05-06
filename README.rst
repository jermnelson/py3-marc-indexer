=======================
py3 MARC Indexer README
=======================
The `py3-marc-indexer`_ project is an MARC 21 indexer using Python 3
along with a forked `pymarc`_ project that has been converted for use
in Python 3 as well.

When indexing a small academic college library's MARC records, I 
ran into more Unicode issues related to misencoded MARC records. Part of
these problems were a result of Python 2.6+ versions string verses unicode
handling that I was able to elimate because with Python 3 all strings are
Unicode.

License
-------
The `py3-marc-indexer`_ project is licensed under Apache 2 open source
license.

Installing
----------
The recommended way to install `py3-marc-indexer`_ is to first created a
Python 3 virtualenv first.

1. Clone the forked `pymarc`_ project and install pymarc with the following
   commands.(Assumes you running a Linux VM)

::
  $ git clone git@github.com:jermnelson/pymarc.git
  $ cd pymarc
  $ git branch py3
  $ python setup.py install

2. Clone the `py3-marc-indexer`_ project with the these commands.

::
  $ git clone git@github.com:jermnelson/py3-marc-indexer.git
  $ cd py3-marc-indexer
  $ git branch multiprocess

Indexing MARC Records
---------------------
To index MARC records, run the index command along with a path to you
MARC records file. If your Solr server resides on a different machine,
you'll need to change the stub_conf file located in index.py file. The
next refactoring of this code base will likely to be integrate it into
a Python 3 version of the `FRBR-Redis-Datastore`_'s Aristotle Django
environment.

::
  $ python index.py /path-to-marc-file/test.mrc


.. _`FRBR-Redis-Datastore`: https://github.com/jermnelson/FRBR-Redis-Datastore
.. _`py3-marc-indexer`: https://github.com/jermnelson/py3-marc-indexer
.. _`pymarc`: https://github.com/edsu/pymarc

