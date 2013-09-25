Name:           cbase-cli
Version:        1.8.0
Release:        1
Epoch:          0
Summary:        command line utils
Group:          System Environment/Utils
License:        DSAL
URL:            http://github.com/northscale/cbase-cli
Source0:        http://github.com/northscale/cbase-cli/downloads/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-%(%{__id_u} -n)

%description
Provides cbase cli tools

%prep
%setup -q -n %{name}-%{version}

%build
config/autorun.sh
%configure

make %{?_smp_mflags}

%check

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
find $RPM_BUILD_ROOT -type f -name '*.la' -exec rm -f {} ';'

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
#%dir %attr (0755, root, bin) %{_libdir}

# extra files
%{_libdir}/python/buckets.pyo
%{_libdir}/python/cluster_stats.pyo
%{_libdir}/python/collector.pyo
%{_libdir}/python/diskqueue_stats.pyo
%{_libdir}/python/info.pyo
%{_libdir}/python/listservers.pyo
%{_libdir}/python/node.pyo
%{_libdir}/python/node_stats.pyo
%{_libdir}/python/processor.pyo
%{_libdir}/python/restclient.pyo
%{_libdir}/python/stats_buffer.pyo
%{_libdir}/python/usage.pyo
%{_libdir}/python/util_cli.pyo
%{_libdir}/python/util_cli.pyc
%{_libdir}/python/usage.pyc
%{_libdir}/python/stats_buffer.pyc
%{_libdir}/python/restclient.pyc
%{_libdir}/python/processor.pyc
%{_libdir}/python/node_stats.pyc
%{_libdir}/python/node.pyc
%{_libdir}/python/listservers.pyc
%{_libdir}/python/info.pyc
%{_libdir}/python/diskqueue_stats.pyc
%{_libdir}/python/collector.pyc
%{_libdir}/python/cluster_stats.pyc
%{_libdir}/python/buckets.pyc
%{_libdir}/python/cbclusterstats
%{_libdir}/python/couchbase-cli
%{_libdir}/python/util_cli.py
%{_libdir}/python/usage.py
%{_libdir}/python/stats_buffer.py
%{_libdir}/python/restclient.py
%{_libdir}/python/processor.py
%{_libdir}/python/node_stats.py
%{_libdir}/python/node.py
%{_libdir}/python/listservers.py
%{_libdir}/python/info.py
%{_libdir}/python/diskqueue_stats.py
%{_libdir}/python/collector.py
%{_libdir}/python/cluster_stats.py
%{_libdir}/python/buckets.py
%dir %{_libdir}/python/simplejson/
%{_libdir}/python/simplejson/decoder.pyo
%{_libdir}/python/simplejson/encoder.pyo
%{_libdir}/python/simplejson/scanner.pyo
%{_libdir}/python/simplejson/scanner.pyc
%{_libdir}/python/simplejson/encoder.pyc
%{_libdir}/python/simplejson/decoder.pyc
%{_libdir}/python/simplejson/scanner.py
%{_libdir}/python/simplejson/encoder.py
%{_libdir}/python/simplejson/decoder.py
%{_libdir}/python/simplejson/__init__.py
%{_libdir}/python/simplejson/__init__.pyo
%{_libdir}/python/simplejson/__init__.pyc
%{_libdir}/python/simplejson/LICENSE.txt
%{_bindir}/couchbase-cli

%changelog
* Wed Sep 25 2013 Albert Zhang <zhgwenming@gmail.com> - 1.0-1
- Initial
