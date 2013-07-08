COUCHBASE_PYTHON_CLIENT = ../couchbase-python-client/couchbase \
                          ../couchbase-python-client/httplib2 \
                          ../couchbase-python-client/simplejson \
                          ../couchbase-python-client/uuid.py

default:

pythonlibdir=$(libdir)/python

pythonlib_SCRIPTS= cbworkloadgen

PYTHON_TOOLS= wrapper/cbworkloadgen

${PYTHON_TOOLS}: wrapper/wrapper
	cp $< $@

CLEANFILES = ${PYTHON_TOOLS}
bin_SCRIPTS = ${PYTHON_TOOLS}

EXTRA_DIST = $(pythonlib_SCRIPTS)

install-data-hook:
	cp -rf $(COUCHBASE_PYTHON_CLIENT) $(pythonlibdir)


