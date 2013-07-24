Summary: couchstore lib
Name: couchstore
Version: 2.1.1
Release: 1.1
Vendor: cbase, Inc
Packager: <zhgwenming@gmail.com>
License: Apache-2
Group: System Environment/Libraries
URL: http://www.couchbase.com
Source: %{name}-%{version}.tar.gz
BuildRequires: snappy-devel
#BuildRoot: %{_topdir}/build/%{name}-%{version}-%{release}

%description
Couchdb c library

%package devel
Group: Development/Libraries
Summary: couchstore Header files
Requires: %{name} = %{version}-%{release}

%description devel
Development files for the couchstore.

%prep
%setup -q -n %{name}-%{version}
echo 'm4_define([VERSION_NUMBER], [%{version}])' >m4/version.m4
config/autorun.sh
%configure

%build
%{__make} %{_smp_mflags}

%install
%{__make} install DESTDIR="%{buildroot}" AM_INSTALL_PROGRAM_FLAGS=""

%clean
%{__rm} -rf %{buildroot}

%post -n %{name} -p /sbin/ldconfig

%postun -n %{name} -p /sbin/ldconfig

%files
%defattr(-, root, root)
%{_bindir}/couch_compact
%{_bindir}/couch_dbdump
%{_bindir}/couch_dbinfo
%{_bindir}/couch_viewgen
%{_libdir}/libcouchstore.la
%{_libdir}/libcouchstore.so
%{_libdir}/libcouchstore.so.1
%{_libdir}/libcouchstore.so.1.0.0
%{_libdir}/pkgconfig/libcouchstore.pc
%{_libdir}/python/couchstore.py
%{_libdir}/python/couchstore.pyc
%{_libdir}/python/couchstore.pyo

%files devel
%defattr(-, root, root)
%doc README.md LICENSE
%{_includedir}/libcouchstore/*

%changelog
* Wed Jul 24 2013 Albert Zhang <zhgwenming@gmail.com> - 2.1.1
- couchstore initial import
