Summary: conflate library for Couchbase
Name: libconflate
Version: 1.7.0
Release: 1
Vendor: Couchbase, Inc.
Packager: Couchbase SDK Team <support@couchbase.com>
License: Apache-2
Group: System Environment/Libraries
URL: http://www.couchbase.com
Source: %{name}-%{version}.tar.gz
#BuildRoot: %{_topdir}/build/%{name}-%{version}_%{release}

BuildRequires:	automake
BuildRequires:	autoconf
BuildRequires:	libtool
BuildRequires:  pkgconfig
BuildRequires:	libcurl

Requires:       libcurl

%description
libconflate is a library providing conflate distribution layer for Couchbase
clients.

%package devel
Group: Development/Libraries
Summary: conflate library for Couchbase - Header files
Requires: %{name}

%description devel
Development files for the conflate library for Couchbase.

%prep
%setup -q -n %{name}-%{version}
echo 'm4_define([VERSION_NUMBER], [%{version}])' >m4/version.m4
echo 'm4_define([VERSION_NUMBER], [%{version}])' 
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

%files -n %{name}
%defattr(-, root, root)
%{_libdir}/libconflate.so.*

%files devel
%defattr(-, root, root)
%doc README.markdown
%{_includedir}/libconflate
%{_libdir}/libconflate.la
%{_libdir}/libconflate.so
%{_libdir}/pkgconfig/libconflate.pc

%changelog
* Tue Mar 06 2012 Albert Zhang <zhgwenming@gmail.com> - 1.8.0.3
- Initial libconfalte package.

