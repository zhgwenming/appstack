SPEC_FILE := percona-xtradb-cluster-galera.spec
TARBALL := percona-xtradb-cluster-galera.tar.gz
SRCDIR ?= ./
DESTDIR ?= ./

.PHONY: srpm

srpm: $(TARBALL) $(SPEC_FILE)
	rpmbuild --define '_sourcedir $(SRCDIR)' --define '_srcrpmdir $(DESTDIR)' -bs $(SPEC_FILE)

$(TARBALL): percona-xtradb-cluster-galera
	tar zcf $@ $^

clean:
	rm -fv *gz *rpm

build: srpm
	rpmbuild --rebuild *.src.rpm
