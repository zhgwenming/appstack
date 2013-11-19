SPEC_FILE := mysql.spec
TARBALL := mysql-5.5.34.tar.gz
SRCDIR ?= ./
DESTDIR ?= ./

.PHONY: srpm

SCL_DEF =	\
	--define 'scl mcluster'				\
	--define '_scl_prefix /opt/%{pkgvendor}'

srpm: $(TARBALL) $(SPEC_FILE)
	rpmbuild --define '_sourcedir $(SRCDIR)'	\
	--define '_srcrpmdir $(DESTDIR)'		\
	$(SCL_DEF)					\
	-bs $(SPEC_FILE)

$(TARBALL): mysql-5.5.29
	tar zcf $@ $^

clean:
	rm -fv *gz *rpm

build: srpm
	rpmbuild	$(SCL_DEF)			\
		--rebuild *.src.rpm 
