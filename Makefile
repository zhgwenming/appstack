#NAME ?= $(MAKECMDGOALS)
SPEC_FILE := $(NAME)/$(NAME).spec
SRCDIR ?= $(NAME)/
DESTDIR ?= $(NAME)/

.PHONY: srpm

srpm: $(SPEC_FILE)
	echo $(SPEC_FILE)
	rpmbuild --define '_sourcedir $(SRCDIR)' --define '_srcrpmdir $(DESTDIR)' -bs $(SPEC_FILE)

clean:
	rm -fv *gz *rpm

build: srpm
	rpmbuild --rebuild $(DESTDIR)/$(NAME)-*.src.rpm
