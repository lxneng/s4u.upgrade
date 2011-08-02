PYTHON		:= python
NOSEFLAGS	:=

bin/buildout: 
	$(PYTHON) bootstrap.py

bin/python bin/sphinx-build:  bin/buildout buildout.cfg versions.cfg
	bin/buildout

check:: bin/sphinx-build
	$(MAKE) -C docs linkcheck

check:: bin/python
	bin/python setup.py nosetests $(NOSEFLAGS)

docs: bin/sphinx-build
	$(MAKE) -C docs html

jenkins: bin/python
	$(MAKE) NOSEFLAGS=--with-xunit check
	bin/coverage xml --include="src/s4u/upgrade/*" --omit="src/s4u/upgrade/tests/tst-pkg/*"

.PHONY: check docs jenkins
