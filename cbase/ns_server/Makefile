NAME ?= ns_server
VERSION ?= 1.8.0
NV = $(NAME)-$(VERSION)
SPEC_FILE := $(NAME).spec
TARBALL := $(NV).tar.gz
SRCDIR ?= ./
DESTDIR ?= ./

.PHONY: srpm

srpm: $(TARBALL) $(SPEC_FILE)
	rpmbuild --define '_sourcedir $(SRCDIR)' --define '_srcrpmdir $(DESTDIR)' -bs $(SPEC_FILE)

$(TARBALL): $(NV)
	tar zcf $@ $^

clean:
	rm -fv *gz *rpm

build: srpm
	rpmbuild --rebuild $(NV)*.src.rpm
