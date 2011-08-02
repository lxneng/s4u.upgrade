Commandline tool
================

Upgrades can be run via the `upgrade` commandline tool. This tool provide a very
simple interface: it only requires a `--scan` parameter telling it which packages
to scan for context providers and upgrade steps. For example to run all upgrade
steps in the `s4u.site` package run this command::

   $ bin/upgrade --scan s4u.site --db-uri postgresql:///s4usite:secret@localhost/

