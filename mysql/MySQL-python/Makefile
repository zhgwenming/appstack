SPEC_FILE := MySQL-python.spec
SRCDIR ?= ./
DESTDIR ?= ./

.PHONY: srpm

srpm: $(TARBALL) $(SPEC_FILE)
	rpmbuild --define '_sourcedir $(SRCDIR)' --define '_srcrpmdir $(DESTDIR)' -bs $(SPEC_FILE)

clean:
	rm -fv *gz *rpm

build: srpm
	rpmbuild --rebuild *.src.rpm
