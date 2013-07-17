Name:           vbucketmigrator
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

%description
This provides vbucketmigration feature in cluster

%prep
%setup -q -n %{name}-%{version}

%build
config/autorun.sh
%configure

make %{?_smp_mflags}

#%check
#make test

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
#find $RPM_BUILD_ROOT -type f -name '*.la' -exec rm -f {} ';'

%clean
rm -rf %{buildroot}

%files
%{_bindir}/vbucketmigrator
%{_mandir}/man1/vbucketmigrator.1m.gz

%changelog
* Wed Jul 17 2013 Albert Zhang <zhgwenming@gmail.com>
- Initial import


