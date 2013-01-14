#NAME ?= $(MAKECMDGOALS)
SHELL := /bin/bash
SPEC_FILE := $(NAME)/$(NAME).spec
SRCDIR ?= $(NAME)
DESTDIR ?= $(NAME)

.PHONY: srpm

srpm: $(SPEC_FILE)
	echo $(SPEC_FILE)
	rpmbuild --define '_sourcedir $(SRCDIR)' --define '_srcrpmdir $(DESTDIR)' -bs $(SPEC_FILE) | tee $(DESTDIR)/srpm.list

clean:
	rm -fv *gz *rpm

build: srpm
	#rpmbuild --rebuild $(DESTDIR)/$(NAME)-*.src.rpm
	rpmbuild --rebuild `grep -ow $(DESTDIR).*src.rpm $(DESTDIR)/srpm.list`
