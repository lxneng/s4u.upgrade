Introduction
============

This package implements a very minimal upgrade framework for use in Python
applications. Its design consists of three parts:


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

Here is a basic context provider which configures SQLAlchemy::

   @upgrade_context('sql')
   def setup_sqlalchemy(options):
       engine = create_engine('postgresql:///projectA')
       return {'sql-engine': engine}

Here is an example upgrade step to add missing tables and indices in a project
using SQLALchemy::

   @upgrade_step(require=['sql'])
   def add_missing_tables(environment):
       meta.metadata.create_all(environment['sql-engline'])

And this is how you run the upgrade::

   $ bin/upgrade --scan my.package
