Upgrade steps
=============

Upgrade steps are python functions which perform a single upgrade step.
Upgrade steps are registered using the :py:func:`s4.bfgtools.upgrade_step`
decorator function.

.. note::

   It is important to write upgrade steps so they can be run multiple times
   without producing odd results. Generally this means you need to check the
   environment before making any changes.

Here is an example upgrade step which adds missing tables an indices to a
database managed by SQLAlchemy. 

.. code-block:: python

   @upgrade_step(require=['sql'])
   def add_missing_tables(environment):
       meta.metadata.create_all(environment['sql-engline'])
