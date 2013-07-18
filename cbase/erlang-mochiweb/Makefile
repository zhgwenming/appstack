NAME ?= erlang-mochiweb
SPEC_FILE := $(NAME).spec
TARBALL := mochi-mochiweb-1.4.1-0-g80571b9.tar.gz
SRCDIR ?= ./
DESTDIR ?= ./

.PHONY: srpm

srpm: $(TARBALL) $(SPEC_FILE)
	rpmbuild --define '_sourcedir $(SRCDIR)' --define '_srcrpmdir $(DESTDIR)' -bs $(SPEC_FILE)

clean:
	rm -fv *rpm

build: srpm
	rpmbuild --rebuild $(NAME)*.src.rpm
