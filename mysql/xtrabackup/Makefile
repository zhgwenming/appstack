SPEC_FILE := xtrabackup.spec
TARBALL := xtrabackup-2.0.6.tar.gz
SRCDIR ?= ./
DESTDIR ?= ./

.PHONY: srpm

srpm: $(TARBALL) $(SPEC_FILE)
	rpmbuild --define '_sourcedir $(SRCDIR)' --define '_srcrpmdir $(DESTDIR)' -bs $(SPEC_FILE)

$(TARBALL): xtrabackup-2.0.6
	tar zcf $@ $^

clean:
	rm -fv xtrabackup-2.0.6.tar.gz *rpm

build: srpm
	rpmbuild --rebuild *.src.rpm
