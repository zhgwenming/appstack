SPEC_FILE := percona-xtradb-cluster.spec
TARBALL := Percona-XtraDB-Cluster-5.5.29.tar.gz
SRCDIR ?= ./
DESTDIR ?= ./

.PHONY: srpm

srpm: $(TARBALL) $(SPEC_FILE)
	rpmbuild --define '_sourcedir $(SRCDIR)' --define '_srcrpmdir $(DESTDIR)' -bs $(SPEC_FILE)

$(TARBALL): Percona-XtraDB-Cluster-5.5.29
	tar zcf $@ $^

clean:
	rm -fv *gz *rpm

build: srpm
	rpmbuild --rebuild Percona-XtraDB-Cluster-5.5.29-%{wsrep_version}.1.rhel6.src.rpm
