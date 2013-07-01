%global with_tests       %{?_with_tests:1}%{!?_with_tests:0}

Name:      libmemcached
Summary:   Client library and command line tools for memcached server
Version:   1.0
Release:   900.1%{?dist}
License:   BSD
Group:     System Environment/Libraries
URL:       http://libmemcached.org/
# Original sources:
#   http://launchpad.net/libmemcached/1.0/%{version}/+download/libmemcached-%{version}.tar.gz
# The source tarball must be repackaged to remove the Hsieh hash
# code, since the license is non-free.  When upgrading, download the new
# source tarball, and run "./strip-hsieh.sh <version>" to produce the
# "-exhsieh" tarball.
Source0:   libmemcached-%{version}.tar.gz

Patch0: libmemcached-memslap-stats.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: cyrus-sasl-devel
BuildRequires: flex bison
%if %{with_tests}
BuildRequires: memcached
%endif
%if 0%{?fedora} >= 12 || 0%{?rhel} >= 6
BuildRequires: systemtap-sdt-devel
%endif
%if 0%{?fedora} >= 11 || 0%{?rhel} >= 5
BuildRequires: libevent-devel
%endif


%description
libmemcached is a C/C++ client library and tools for the memcached server
(http://memcached.org/). It has been designed to be light on memory
usage, and provide full access to server side methods.

It also implements several command line tools:

memcapable  Checking a Memcached server capibilities and compatibility
memcat      Copy the value of a key to standard output
memcp       Copy data to a server
memdump     Dumping your server
memerror    Translate an error code to a string
memexist    Check for the existance of a key
memflush    Flush the contents of your servers
memparse    Parse an option string
memping     Test to see if a server is available.
memrm       Remove a key(s) from the server
memslap     Generate testing loads on a memcached cluster
memstat     Dump the stats of your servers to standard output
memtouch    Touches a key


%package devel
Summary: Header files and development libraries for %{name}
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: pkgconfig
Requires: cyrus-sasl-devel%{?_isa}

%description devel
This package contains the header files and development libraries
for %{name}. If you like to develop programs using %{name}, 
you will need to install %{name}-devel.


%prep
%setup -q
%patch0 -p1

mkdir examples
cp -p tests/*.{cc,h} examples/

# Will be regenerated during build
%if 0%{?fedora} > 9 || 0%{?rhel} > 5
rm -f libmemcached/csl/{parser,scanner}.cc
%endif

# Temporary fix for SASL detection
#sed -i -e s/ax_cv_sasl/ac_enable_sasl/ configure


%build
# option --with-memcached=false to disable server binary check (as we don't run test)
./config/autorun.sh
%configure --disable-static \
%if ! %{with_tests}
   --with-memcached=false
%endif

make %{_smp_mflags}


%install
rm -rf %{buildroot}
make install  DESTDIR="%{buildroot}" AM_INSTALL_PROGRAM_FLAGS=""


%check
%if %{with_tests}
# test suite cannot run in mock (same port use for memcache servers on all arch)
# All tests completed successfully
# diff output.res output.cmp fails but result depend on server version
make test
%else
echo 'Test suite disabled (missing "--with tests" option)'
%endif


%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig
 

%files
%defattr (-,root,root,-) 
%doc AUTHORS COPYING README THANKS TODO ChangeLog
%{_bindir}/mem*
%exclude %{_libdir}/lib*.la
%{_libdir}/libhashkit.so.0*
%{_libdir}/libmemcached.so.6*
%{_libdir}/libmemcachedprotocol.so.0*
%{_libdir}/libmemcachedutil.so.1*
%{_mandir}/man1/mem*


%files devel
%defattr (-,root,root,-) 
%doc examples
%{_includedir}/libmemcached
%{_includedir}/libhashkit
%{_libdir}/libhashkit.so
%{_libdir}/libmemcached.so
%{_libdir}/libmemcachedprotocol.so
%{_libdir}/libmemcachedutil.so
%{_libdir}/pkgconfig/libmemcached.pc
%{_mandir}/man3/libmemcached*
%{_mandir}/man3/memcached*
%{_mandir}/man3/hashkit*


%changelog
* Tue Jun 30 2012 Albert Zhang <albertwzhang@gmail.com>
- Initial libmemcached repo from cbase repo
