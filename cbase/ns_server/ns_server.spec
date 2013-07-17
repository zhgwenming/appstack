Name:           ns_server
Version:        1.8.0
Release:        901.1%{dist}
Epoch:          0
Summary:        vbucketmigrator for memcached
Group:          System Environment/Libraries
License:        DSAL
URL:            http://github.com/northscale/bucket_engine
Source0:        http://github.com/northscale/bucket_engine/downloads/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-%(%{__id_u} -n)
BuildRequires:	memcached-devel >= 1.4.4-902

%define pkgroot	/opt/%{pkgvendor}
%define prefix	%{pkgroot}/%{name}
%define cbuser	cbase

%description
This provides vbucketmigration feature in cluster

%prep
%setup -q -n %{name}-%{version}

%build
./configure --prefix=%{prefix}
#$(MAKE) -C ns_server install "PREFIX=$(PREFIX)"

#make %{?_smp_mflags} install PREFIX=
#make %{?_smp_mflags} 
#make

#%check
#make test

%install
make install DESTDIR=%{buildroot}
#make install "PREFIX=%{buildroot}/%{prefix}"
#rm -rf %{buildroot}
#make install PREFIX=%{buildroot}
#find $RPM_BUILD_ROOT -type f -name '*.la' -exec rm -f {} ';'

%clean
#rm -rf %{buildroot}

%files
%{_bindir}/sigar_port

%changelog
* Wed Jul 17 2013 Albert Zhang <zhgwenming@gmail.com>
- Initial import


