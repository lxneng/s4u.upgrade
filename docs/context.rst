Context providers
=================

A context provider is responsible for configuring a part of the environment
in which upgrade steps are run. A context provider is a python function which
takes no parameters, and returns a dictionary of items to be added to the
environment dictionary for upgrade methods. The provider is registered with
the system using the :py:func:`s4u.bfgtools.upgrade.upgrade_context`
decorator function. A provider is registered under a name, which upgrade steps
need to use to specify which context providers they need.

As an example here is a context provides which configures `SQLAlchemy
<http://sqlalchemy.org/>`_ and adds the database engine to the environment.

.. code-block:: python

   @upgrade_context('sql')
   def setup_sqlalchemy():
       engine = create_engine_from_string('sqlite:///')
       sm = orm.sessionmaker(extension=ZopeTransactionExtension())
       meta.Session = scoped_session(sm)
       meta.Session.configure(bind=engine)
       return {'sql-engine': engine}

This example has one obvious flaw: it hardcodes the database connection
information. To allow context providers to take user input they can register
extra commandline arguments for the *commandline tool*. This is done by passing
a list of :py:meth:`argparse.ArgumentParser.add_argument` parameters to the
`upgrade_context` method. The parameters are passed as a tuple containing the
parameter name and a dictionary of keyword arguments. The resulting argparse
options object is passed as a parameter to the context provider. Here is our
SQLAlchemy example again, extended to define a `--db-uri` option:

.. code-block:: python

   @upgrade_context('sql', [('--db-uri',
                   {'type': 'string', 'required': True, 'dest': 'dburi'})])
   def setup_sqlalchemy(options):
       engine = create_engine_from_string(options.dburi)
       sm = orm.sessionmaker(extension=ZopeTransactionExtension())
       meta.Session = scoped_session(sm)
       meta.Session.configure(bind=engine)
       return {'sql-engine': engine}
