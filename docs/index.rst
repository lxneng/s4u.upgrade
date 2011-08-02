s4u.upgrade
===========

This package provides basic machinery to manage automated upgrades. Its
design consists of three parts:

1. *context providers*, which are responsible for setting up the context
   required for an upgrade step. For example establishing a connection to
   a SQL server or configuring SQLALchemy.
2. *upgrade steps*, which are functions that perform the actual upgrade
   steps.
3. a *commandline tool* to run the *upgrade steps* and required *context
   providers*.

In order to keep the framework minimal there are a few things which are
deliberately not supported:

* No versioning of the environment is done; the tool will always run all
  all upgrade steps. Each step must support being run multiple times
  without unexpected results.
* Downgrades are not supported.
* Depdendencies between upgrade steps are not supported.

Table of contents
-----------------

.. toctree::
   :maxdepth: 1

   cli
   context
   step
   changes

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
