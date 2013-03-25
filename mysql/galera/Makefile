SPEC_FILE := mysql-cluster-galera.spec
TARBALL := mysql-cluster-galera.tar.gz
SRCDIR ?= ./
DESTDIR ?= ./

.PHONY: srpm

srpm: $(TARBALL) $(SPEC_FILE)
	rpmbuild --define '_sourcedir $(SRCDIR)' --define '_srcrpmdir $(DESTDIR)' -bs $(SPEC_FILE)

$(TARBALL): mysql-cluster-galera
	tar zcf $@ $^

clean:
	rm -fv *gz *rpm

build: srpm
	rpmbuild --rebuild *.src.rpm
