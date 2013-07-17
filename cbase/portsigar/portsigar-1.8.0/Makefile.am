ACLOCAL_AMFLAGS = -I m4

AM_CPPFLAGS = $(SIGAR_CPPFLAGS)
AM_LDFLAGS = $(SIGAR_LDFLAGS)

bin_PROGRAMS = sigar_port
sigar_port_SOURCES = sigar_port.c

check-syntax:
	$(COMPILE) -o /dev/null -S ${CHK_SOURCES}

%.s : %.c
	$(COMPILE) -S -fverbose-asm -o $@ $<
