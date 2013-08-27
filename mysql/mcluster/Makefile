SPEC_FILE := mcluster.spec
SRCDIR ?= ./
DESTDIR ?= ./

.PHONY: srpm

SCL_DEF =	\
	--define 'scl mcluster'				\
	--define '_scl_prefix /opt/%{pkgvendor}'

srpm: $(SPEC_FILE)
	rpmbuild --define '_sourcedir $(SRCDIR)'	\
	--define '_srcrpmdir $(DESTDIR)'		\
	$(SCL_DEF)					\
	-bs $(SPEC_FILE)

clean:
	rm -fv *gz *rpm

build: srpm
	rpmbuild	$(SCL_DEF)			\
		--rebuild *.src.rpm 
