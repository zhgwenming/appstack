SPEC_FILE := mysql-galera.spec
TARBALL := mysql-galera-5.5.29.tar.gz
SRCDIR ?= ./
DESTDIR ?= ./

.PHONY: srpm

srpm: $(TARBALL) $(SPEC_FILE)
	rpmbuild --define '_sourcedir $(SRCDIR)' --define '_srcrpmdir $(DESTDIR)' -bs $(SPEC_FILE)

$(TARBALL): mysql-galera-5.5.29
	tar zcf $@ $^

clean:
	rm -fv *gz *rpm

build: srpm
	rpmbuild --rebuild mysql-galera-5.5.29.src.rpm
