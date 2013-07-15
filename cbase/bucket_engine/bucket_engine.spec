Name:           bucket_engine
Version:        1.8.0
Release:        1
Epoch:          0
Summary:        Bucket engine for memcached
Group:          System Environment/Libraries
License:        DSAL
URL:            http://github.com/northscale/bucket_engine
Source0:        http://github.com/northscale/bucket_engine/downloads/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-%(%{__id_u} -n)
BuildRequires:	memcached-devel >= 1.4.4-902

%description
This memcached engine provides multi-tenancy and isolation between other
memcached engine instances.

%prep
%setup -q -n %{name}-%{version}

%build
config/autorun.sh
%configure

make %{?_smp_mflags}

%check
make test

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
find $RPM_BUILD_ROOT -type f -name '*.la' -exec rm -f {} ';'

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_datadir}
%attr (-, root, bin) %{_libdir}/memcached/bucket_engine.so*
%attr (-, root, bin) %{_datadir}/bucket_engine/*

# extra files
%{_bindir}/collectd
%{_bindir}/collectd_memcached_buckets

%{_libdir}/memcached/bucket_engine.a

%{_libdir}/python/collectd.py
%{_libdir}/python/collectd.pyc
%{_libdir}/python/collectd.pyo
%{_libdir}/python/collectd_memcached_buckets.py
%{_libdir}/python/collectd_memcached_buckets.pyc
%{_libdir}/python/collectd_memcached_buckets.pyo
%{_libdir}/python/mc_bin_client.py
%{_libdir}/python/mc_bin_client.pyc
%{_libdir}/python/mc_bin_client.pyo
%{_libdir}/python/memcacheConstants.py
%{_libdir}/python/memcacheConstants.pyc
%{_libdir}/python/memcacheConstants.pyo
%{_libdir}/python/types.db


%changelog
* Mon Feb  8 2010 Trond Norbye <trond.norbye@gmail.com> - 1.0-1
- Initial
