Name:	cbase
Version: 1.8.1
Release:	903.1%{?dist}
Summary:	A memcached cache cluster
Group:		System Environment/Daemons
License:	BSD
URL:		http://northscale.com
Source0:	http://northscale.com/cbase/dist/%{name}-%{version}.tar.gz
Source1:	cbase_init.d.tmpl
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	automake
BuildRequires:	autoconf
BuildRequires:	libtool
BuildRequires:	openssl-devel
BuildRequires:  libevent-devel
BuildRequires:  pkgconfig
BuildRequires:  sqlite-devel
BuildRequires:  check-devel
BuildRequires:  erlang
BuildRequires:  sigar-devel
BuildRequires:  memcached-devel >= 1.4.4-902
#BuildRequires:  libmemcached-devel
#BuildRequires:  libvbucket-devel
#BuildRequires:  libconflate-devel
Requires:       openssl
Requires:	libevent
Requires:	memcached
Requires:	bucket-engine
Requires:	ep-engine
Requires:	moxi
Requires:       sqlite
Requires:       erlang
Requires:       sigar


Patch0:  workload-generator-destdir.patch

%define pkgroot	/opt/letv
%define prefix	%{pkgroot}/%{name}
%define cbuser	couchbase

%description
cbase is a memcached cluster with several optimizations to bring efficiency to
many memcached deployments, especially those with heavy workloads or
complex network topologies.  Optimizations include handling timeouts for
the client, deduplication of requests, a 'front' cache and protocol
(ascii to binary) conversion.  These optimizations keep the 'contract'
of the memcached protocol whole for clients.

%prep
%setup -q

%patch0 -p1

%build
rm -rf %{prefix}

%{__make} %{_smp_mflags} PREFIX=%{prefix} DISABLE_COUCH=1 PRODUCT_VERSION=1.8.1

%install

## Default configs
#mkdir -p %{buildroot}/%{_sysconfdir}/sysconfig

mkdir -p %{buildroot}%{pkgroot}
mkdir -p %{buildroot}%{_initrddir}
mv %{prefix} %{buildroot}%{pkgroot}

mkdir -p %{buildroot}%{prefix}/var/lib/couchbase/logs

sed 's/@@PRODUCT@@/couchbase-server/; s/@@PRODUCT_BASE@@/couchbase/;
	s,@@PREFIX@@,%{prefix},'	\
	%{SOURCE1} > %{buildroot}%{_initrddir}/%{name}

chmod +x %{buildroot}%{_initrddir}/%{name}

ln -s /usr/bin/moxi %{buildroot}%{prefix}/bin/moxi
ln -s /usr/bin/memcached %{buildroot}%{prefix}/bin/memcached
ln -s %{_libdir}/memcached %{buildroot}%{prefix}/lib/memcached

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_initrddir}/%{name}
%dir %{pkgroot}
%dir %attr(-,%{cbuser},%{cbuser}) %{prefix}
%dir %{prefix}/bin
%dir %{prefix}/etc
%dir %{prefix}/etc/couchbase
%dir %{prefix}/lib
%dir %{prefix}/lib/memcached
%dir %{prefix}/lib/python
%dir %{prefix}/lib/python/simplejson
%dir %{prefix}/lib/python/couchbase
%dir %{prefix}/lib/python/couchbase/migrator
%dir %{prefix}/lib/python/couchbase/tests
%dir %{prefix}/lib/python/couchbase/utils
%dir %{prefix}/lib/python/httplib2
%dir %{prefix}/lib/ns_server
%dir %{prefix}/lib/ns_server/erlang
%dir %{prefix}/lib/ns_server/erlang/lib
%dir %{prefix}/lib/ns_server/erlang/lib/erlwsh
%dir %{prefix}/lib/ns_server/erlang/lib/erlwsh/priv
%dir %{prefix}/lib/ns_server/erlang/lib/erlwsh/priv/www
%dir %{prefix}/lib/ns_server/erlang/lib/erlwsh/ebin
%dir %{prefix}/lib/ns_server/erlang/lib/gen_smtp
%dir %{prefix}/lib/ns_server/erlang/lib/gen_smtp/ebin
%dir %{prefix}/lib/ns_server/erlang/lib/mochiweb
%dir %{prefix}/lib/ns_server/erlang/lib/mochiweb/ebin
%dir %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1
%dir %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv
%dir %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public
%dir %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/css
%dir %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/js
%dir %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images
%dir %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/no-preload
%dir %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/spinner
%dir %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/ui-theme
%dir %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin
%dir %{prefix}/lib/ns_server/erlang/lib/ale
%dir %{prefix}/lib/ns_server/erlang/lib/ale/ebin
#%dir %{prefix}/share
#%dir %{prefix}/share/bucket_engine
%dir %{prefix}/share/man
%dir %{prefix}/share/man/man1
%dir %{prefix}/var
%dir %{prefix}/var/lib
%dir %{prefix}/var/lib/couchbase
%dir %{prefix}/var/lib/couchbase/mnesia
#%dir %{prefix}/include
%config(noreplace) %{prefix}/etc/couchbase/init.sql
%config(noreplace) %{prefix}/etc/couchbase/static_config
%config(noreplace) %{prefix}/etc/couchbase/config
#%doc %{prefix}/share/man/man1/cbadm-online-update.1m
%doc %{prefix}/share/man/man1/vbucketmigrator.1m
#%doc %{prefix}/share/man/man1/cbbackup-incremental.1m
%attr(-,root,root) %{prefix}/lib/python/cbworkloadgen
#%attr(-,root,root) %{prefix}/lib/python/collectd_memcached_buckets.py
%attr(-,root,root) %{prefix}/lib/python/cbclusterstats
#%attr(-,root,root) %{prefix}/lib/python/collectd.py
#%attr(-,root,root) %{prefix}/lib/python/cbbackup-merge-incremental
#%attr(-,root,root) %{prefix}/lib/python/cbvbucketctl
#%attr(-,root,root) %{prefix}/lib/python/cbbackup-incremental
#%attr(-,root,root) %{prefix}/lib/python/cbdbmaint
#%attr(-,root,root) %{prefix}/lib/python/cbadm-online-update
%attr(-,root,root) %{prefix}/lib/python/couchbase-cli
#%attr(-,root,root) %{prefix}/lib/python/clitool.py
#%attr(-,root,root) %{prefix}/lib/python/cbadm-tap-registration
%attr(-,root,root) %{prefix}/lib/python/couchbase/migrator/migrator_dir.py
%attr(-,root,root) %{prefix}/lib/python/couchbase/migrator/migrator_couchbase.py
%attr(-,root,root) %{prefix}/lib/python/couchbase/migrator/migrator_csv.py
%attr(-,root,root) %{prefix}/lib/python/couchbase/migrator/migrator_zip.py
%attr(-,root,root) %{prefix}/lib/python/couchbase/migrator/migrator.py
%attr(-,root,root) %{prefix}/lib/python/couchbase/migrator/migrator_couchdb.py
%attr(-,root,root) %{prefix}/lib/python/couchbase/migrator/__init__.py
%attr(-,root,root) %{prefix}/lib/python/couchbase/migrator/migrator_json.py
%attr(-,root,root) %{prefix}/lib/python/couchbase/exception.py
%attr(-,root,root) %{prefix}/lib/python/couchbase/tests/test_couchbaseclient.py
%attr(-,root,root) %{prefix}/lib/python/couchbase/tests/test_restclient.py
%attr(-,root,root) %{prefix}/lib/python/couchbase/tests/__init__.py
%attr(-,root,root) %{prefix}/lib/python/couchbase/tests/warnings_catcher.py
%attr(-,root,root) %{prefix}/lib/python/couchbase/tests/test_client.py
%attr(-,root,root) %{prefix}/lib/python/couchbase/__init__.py
%attr(-,root,root) %{prefix}/lib/python/couchbase/util.py
%attr(-,root,root) %{prefix}/lib/python/couchbase/rest_client.py
%attr(-,root,root) %{prefix}/lib/python/couchbase/couchbaseclient.py
%attr(-,root,root) %{prefix}/lib/python/couchbase/utils/couchbase-migrator.py
%attr(-,root,root) %{prefix}/lib/python/couchbase/utils/__init__.py
%attr(-,root,root) %{prefix}/lib/python/couchbase/client.py
%attr(-,root,root) %{prefix}/lib/python/couchbase/logger.py
#%attr(-,root,root) %{prefix}/lib/python/cbstats
#%attr(-,root,root) %{prefix}/lib/python/capture.py
#%attr(-,root,root) %{prefix}/lib/python/util.py
#%attr(-,root,root) %{prefix}/lib/python/tap_example.py
#%attr(-,root,root) %{prefix}/lib/python/cbadm-online-restore
#%attr(-,root,root) %{prefix}/lib/python/cbflushctl
#%attr(-,root,root) %{prefix}/lib/python/backup_util.py
#%attr(-,root,root) %{prefix}/lib/python/memcacheConstants.py
#%attr(-,root,root) %{prefix}/lib/python/mc_bin_server.py
#%attr(-,root,root) %{prefix}/lib/python/mc_bin_client.py
#%attr(-,root,root) %{prefix}/lib/python/cbdbconvert
%attr(-,root,root) %{prefix}/lib/python/cluster_stats.py
#%attr(-,root,root) %{prefix}/lib/python/cbdbupgrade
#%attr(-,root,root) %{prefix}/lib/python/cbrestore
#%attr(-,root,root) %{prefix}/lib/python/types.db
#%attr(-,root,root) %{prefix}/lib/python/tap.py
#%attr(-,root,root) %{prefix}/lib/python/cbbackup
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/erlwsh/priv/www/index.html
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/erlwsh/priv/www/prototype.js
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/erlwsh/ebin/erlwsh.app
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/erlwsh/ebin/eshell.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/erlwsh/ebin/erlwsh_deps.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/erlwsh/ebin/erlwsh_web.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/erlwsh/ebin/erlwsh_sup.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/erlwsh/ebin/erlwsh_app.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/erlwsh/ebin/erlwsh.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/gen_smtp/ebin/mimemail.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/gen_smtp/ebin/gen_smtp_server_session.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/gen_smtp/ebin/gen_smtp_client.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/gen_smtp/ebin/smtp_util.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/gen_smtp/ebin/gen_smtp_server.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/gen_smtp/ebin/gen_smtp.app
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/gen_smtp/ebin/binstr.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/gen_smtp/ebin/smtp_server_example.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/gen_smtp/ebin/socket.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/mochiweb/ebin/mochiweb_cookies.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/mochiweb/ebin/mochijson2.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/mochiweb/ebin/mochiweb_sup.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/mochiweb/ebin/mochiweb_app.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/mochiweb/ebin/mochiweb_socket_server.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/mochiweb/ebin/mochinum.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/mochiweb/ebin/mochiweb_html.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/mochiweb/ebin/mochiweb_echo.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/mochiweb/ebin/mochiweb_charref.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/mochiweb/ebin/mochiweb_response.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/mochiweb/ebin/reloader.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/mochiweb/ebin/mochiweb_http.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/mochiweb/ebin/mochifmt_std.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/mochiweb/ebin/mochihex.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/mochiweb/ebin/mochiweb_multipart.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/mochiweb/ebin/mochifmt_records.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/mochiweb/ebin/mochiweb_util.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/mochiweb/ebin/mochiweb_request.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/mochiweb/ebin/mochiweb_skel.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/mochiweb/ebin/mochiweb_headers.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/mochiweb/ebin/mochiweb.app
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/mochiweb/ebin/mochifmt.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/mochiweb/ebin/mochijson.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/mochiweb/ebin/mochiweb.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/css/jquery-ui.couchbase.css
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/css/screen.css
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/css/print.css
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/favicon.ico
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/index.html
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/js/misc.js
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/js/core-data.js
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/js/app-ui-misc.js
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/js/jquery.js
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/js/overview.js
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/js/servers.js
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/js/analytics.js
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/js/app.js
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/js/buckets.js
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/js/json2.js
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/js/jquery.flot.js
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/js/jquery.sparkline.js
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/js/tools.tabs.js
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/js/app-misc.js
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/js/jquery-ui-1.8.10.custom.js
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/js/excanvas.min.js
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/js/hooks.js
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/js/jquery.cookie.js
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/js/underscore.js
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/js/all-images.js
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/js/base64.js
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/js/settings.js
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/js/cells.js
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/js/jquery.ba-bbq.js
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/config-top.png
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/footer_bg.png
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/crn_hdr_err.gif
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/lbox_t.png
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/tooltip_bg_777777.png
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/expander_2_bg.gif
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/button_gray_big.gif
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/button_blue_3.gif
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/blue-button.png
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/bg_h2.gif
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/lbox_lt.png
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/server_icon.gif
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/warning_bg_2.png
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/no-preload/mokugift-tree.gif
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/lbox_rt.png
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/button_red.gif
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/button_gray_medium.gif
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/btn_1_bg.png
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/btn_2_bg.png
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/add_btn.png
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/usage_small.gif
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/tooltip_bg.gif
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/large_buttons_bg.gif
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/usages.png
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/lbox_b.png
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/gray_box_bg.gif
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/lbox_rb.png
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/usage_big.gif
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/gong_rb_2.gif
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/usage_small_2.gif
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/sign_in_button.gif
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/shadow_box_side_bg.gif
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/spinner/spinner_1.gif
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/spinner/spinner_lightbox.gif
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/spinner/spinner_gr_nav.gif
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/spinner/spinner2_gr_nav.gif
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/spinner/spinner_3.gif
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/login_screen.png
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/bg_total.gif
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/add_back_bg.png
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/lbox_cent.png
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/header_bg.png
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/btn_cancel_bg.png
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/setup-button.png
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/welcome-setup-button.png
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/server_status_icons_solid_bg.png
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/background.png
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/membase-logo.png
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/vlabels.gif
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/couchbase_welcome_background.png
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/config-bottom.png
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/bg_time_act.gif
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/server_icon.png
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/button_blue.gif
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/alert_red.png
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/auth_form_bg.png
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/edit-button.png
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/couchbase_logo.png
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/bg_li_th.gif
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/button_gray_200.gif
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/attention_bg.gif
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/expander_bg.gif
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/gong_rb.gif
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/info_bg.gif
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/icons.png
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/ico_server_big.png
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/warning_bg.gif
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/elastro_cling_v22.png
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/mini_graph_bg.gif
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/alert_1.gif
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/devider_line_1.gif
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/devider_line_2.gif
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/lbox_lb.png
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/ui-theme/ui-icons_454545_256x240.png
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/ui-theme/ui-icons_222222_256x240.png
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/ui-theme/ui-bg_glass_55_fbf9ee_1x400.png
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/ui-theme/ui-bg_glass_75_dadada_1x400.png
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/ui-theme/ui-bg_flat_75_ffffff_40x100.png
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/ui-theme/ui-bg_highlight-soft_75_cccccc_1x100.png
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/ui-theme/ui-icons_2e83ff_256x240.png
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/ui-theme/ui-bg_flat_0_000000_40x100.png
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/ui-theme/ui-bg_glass_75_e6e6e6_1x400.png
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/ui-theme/ui-bg_glass_95_fef1ec_1x400.png
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/ui-theme/ui-icons_cd0a0a_256x240.png
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/ui-theme/ui-icons_888888_256x240.png
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/ui-theme/ui-bg_glass_65_ffffff_1x400.png
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/blue_block_bg.gif
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/alert_green.png
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/add_back_btn.png
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/server_status_icons.png
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/switcher_bg.png
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/shadow_box_bg.gif
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ebucketmigrator_srv.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_node_disco_rep_events.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_config_ets_dup.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/menelaus_stats.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_mail_sup.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/menelaus_util.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/menelaus_event.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/master_activity_events.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/mc_binary.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/menelaus_deps.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_node_disco_sup.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/mc_client_binary.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_vbm_sup.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ringdict.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_replicas_builder.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/mock_gen_server.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_tick.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_server.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_rebalancer.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_node_disco.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_config_isasl_sync.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_error_messages.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/cucumberl.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/path_config.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/cb_init_loggers.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_single_vbucket_mover.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/system_stats_collector.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/single_bucket_sup.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/mb_mnesia.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/menelaus_rest.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/addr_util.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/mb_master_sup.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_mail_log.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/gen_sup.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_log_sink.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_port_sup.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_mail.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/supervisor_cushion.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/misc_tests.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/work_queue.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/menelaus_alert.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_vbucket_mover.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_server_sup.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_bucket.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ebucketmigrator.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_server.app
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/auto_failover.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_storage_conf.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/stats_archiver.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_pubsub.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_info.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_server_cluster_sup.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_cluster.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_memcached.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_moxi_sup.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_log.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/uuid.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/log_os_info.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/diag_handler.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_log_categorizing.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/hot_keys_keeper.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/master_activity_events_keeper.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ringbuffer.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_bucket_sup.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_heart.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_orchestrator.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_config_log.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/auto_failover_logic.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_process_registry.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_test_util.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/mb_master.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/menelaus_web_buckets.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_config_replica.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/mock.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/menelaus_sup.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_watchdog.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/stats_collector.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_janitor.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_cluster_membership.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_config_tests.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/t.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_config_sup.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_bootstrap.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_doctor.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/stats_reader.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_node_disco_log.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_log_browser.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/mb_grid.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/misc.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/timeout_diag_logger.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/master_activity_events_pids_watcher.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/mb_mnesia_sup.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/menelaus_web_alerts_srv.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_node_disco_conf_events.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_port_init.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_janitor_vis.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_cookie_manager.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/vclock.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_config_default.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_config.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/mb_map.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/dist_manager.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/failover_safeness_level.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_config_rep.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_port_server.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/menelaus_web.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/menelaus_auth.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ale/ebin/ale.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ale/ebin/ale_dynamic_sup.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ale/ebin/ale_transform.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ale/ebin/ale_error_logger_handler.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ale/ebin/ale_utils.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ale/ebin/ale.app
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ale/ebin/ale_app.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ale/ebin/ale_codegen.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ale/ebin/ale_stderr_sink.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ale/ebin/ale_sup.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ale/ebin/dynamic_compile.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ale/ebin/ale_disk_sink.beam
%attr(-,root,root) %{prefix}/lib/ns_server/erlang/lib/ale/ebin/ale_default_formatter.beam
#%attr(-,root,root) %{prefix}/share/bucket_engine/collectd_memcached_buckets.py
#%attr(-,root,root) %{prefix}/share/bucket_engine/collectd.py
#%attr(-,root,root) %{prefix}/share/bucket_engine/memcacheConstants.py
#%attr(-,root,root) %{prefix}/share/bucket_engine/mc_bin_client.py
#%attr(-,root,root) %{prefix}/share/bucket_engine/types.db
#%attr(-,root,root) %{prefix}/include/memcached/genhash.h
#%attr(-,root,root) %{prefix}/include/memcached/protocol_plugin.h
#%attr(-,root,root) %{prefix}/include/memcached/callback.h
#%attr(-,root,root) %{prefix}/include/memcached/config_parser.h
#%attr(-,root,root) %{prefix}/include/memcached/extension.h
#%attr(-,root,root) %{prefix}/include/memcached/engine.h
#%attr(-,root,root) %{prefix}/include/memcached/engine_common.h
#%attr(-,root,root) %{prefix}/include/memcached/vbucket.h
#%attr(-,root,root) %{prefix}/include/memcached/util.h
#%attr(-,root,root) %{prefix}/include/memcached/protocol_binary.h
#%attr(-,root,root) %{prefix}/include/memcached/engine_testapp.h
#%attr(-,root,root) %{prefix}/include/memcached/server_api.h
#%attr(-,root,root) %{prefix}/include/memcached/types.h
#%attr(-,root,root) %{prefix}/include/memcached/extension_loggers.h
#%attr(-,root,root) %{prefix}/include/memcached/visibility.h
#%attr(-,root,root) %{prefix}/include/memcached/allocator_hooks.h
%attr(-,root,root) %{prefix}/bin/cbworkloadgen
%attr(-,root,root) %{prefix}/bin/couchbase-server
%attr(-,root,root) %{prefix}/bin/sigar_port
%attr(-,root,root) %{prefix}/bin/cbcollect_info
%attr(-,root,root) %{prefix}/bin/cbdumpconfig.escript
%attr(-,root,root) %{prefix}/bin/cbbrowse_logs
#%attr(-,root,root) %{prefix}/bin/cbbackup-merge-incremental
#%attr(-,root,root) %{prefix}/bin/cbvbucketctl
%attr(-,root,root) %{prefix}/bin/moxi
#%attr(-,root,root) %{prefix}/bin/cbbackup-incremental
#%attr(-,root,root) %{prefix}/bin/cbdbmaint
#%attr(-,root,root) %{prefix}/bin/cbadm-online-update
%attr(-,root,root) %{prefix}/bin/couchbase-cli
#%attr(-,root,root) %{prefix}/bin/cbadm-tap-registration
%attr(-,root,root) %{prefix}/bin/memcached
#%attr(-,root,root) %{prefix}/bin/vbucketkeygen
#%attr(-,root,root) %{prefix}/bin/cbstats
%attr(-,root,root) %{prefix}/bin/ebucketmigrator
#%attr(-,root,root) %{prefix}/bin/cbadm-online-restore
#%attr(-,root,root) %{prefix}/bin/vbuckettool
#%attr(-,root,root) %{prefix}/bin/mcstat
#%attr(-,root,root) %{prefix}/bin/cbflushctl
#%attr(-,root,root) %{prefix}/bin/squasher.sql
%attr(-,root,root) %{prefix}/bin/vbucketmigrator
#%attr(-,root,root) %{prefix}/bin/mcbasher
#%attr(-,root,root) %{prefix}/bin/sqlite3
#%attr(-,root,root) %{prefix}/bin/cbdbconvert
#%attr(-,root,root) %{prefix}/bin/collectd
#%attr(-,root,root) %{prefix}/bin/engine_testapp
#%attr(-,root,root) %{prefix}/bin/cbdbupgrade
#%attr(-,root,root) %{prefix}/bin/isasladm
#%attr(-,root,root) %{prefix}/bin/cbrestore
#%attr(-,root,root) %{prefix}/bin/collectd_memcached_buckets
#%attr(-,root,root) %{prefix}/bin/analyze_core
#%attr(-,root,root) %{prefix}/bin/memcachetest
#%attr(-,root,root) %{prefix}/bin/cbbackup
#%{prefix}/lib/python/backup_util.pyc
#%{prefix}/lib/python/backup_util.pyo
%attr(-,root,root) %{prefix}/lib/python/buckets.py
%attr(-,root,root) %{prefix}/lib/python/buckets.pyc
%attr(-,root,root) %{prefix}/lib/python/buckets.pyo
#%{prefix}/lib/python/capture.pyc
#%{prefix}/lib/python/capture.pyo
#%{prefix}/lib/python/clitool.pyc
#%{prefix}/lib/python/clitool.pyo
%{prefix}/lib/python/cluster_stats.pyc
%{prefix}/lib/python/cluster_stats.pyo
#%{prefix}/lib/python/collectd.pyc
#%{prefix}/lib/python/collectd.pyo
#%{prefix}/lib/python/collectd_memcached_buckets.pyc
#%{prefix}/lib/python/collectd_memcached_buckets.pyo
%attr(-,root,root) %{prefix}/lib/python/collector.py
%attr(-,root,root) %{prefix}/lib/python/collector.pyc
%attr(-,root,root) %{prefix}/lib/python/collector.pyo
%{prefix}/lib/python/couchbase/__init__.pyc
%{prefix}/lib/python/couchbase/__init__.pyo
%{prefix}/lib/python/couchbase/client.pyc
%{prefix}/lib/python/couchbase/client.pyo
%{prefix}/lib/python/couchbase/couchbaseclient.pyc
%{prefix}/lib/python/couchbase/couchbaseclient.pyo
%{prefix}/lib/python/couchbase/exception.pyc
%{prefix}/lib/python/couchbase/exception.pyo
%{prefix}/lib/python/couchbase/logger.pyc
%{prefix}/lib/python/couchbase/logger.pyo
%{prefix}/lib/python/couchbase/migrator/__init__.pyc
%{prefix}/lib/python/couchbase/migrator/__init__.pyo
%{prefix}/lib/python/couchbase/migrator/migrator.pyc
%{prefix}/lib/python/couchbase/migrator/migrator.pyo
%{prefix}/lib/python/couchbase/migrator/migrator_couchbase.pyc
%{prefix}/lib/python/couchbase/migrator/migrator_couchbase.pyo
%{prefix}/lib/python/couchbase/migrator/migrator_couchdb.pyc
%{prefix}/lib/python/couchbase/migrator/migrator_couchdb.pyo
%{prefix}/lib/python/couchbase/migrator/migrator_csv.pyc
%{prefix}/lib/python/couchbase/migrator/migrator_csv.pyo
%{prefix}/lib/python/couchbase/migrator/migrator_dir.pyc
%{prefix}/lib/python/couchbase/migrator/migrator_dir.pyo
%{prefix}/lib/python/couchbase/migrator/migrator_json.pyc
%{prefix}/lib/python/couchbase/migrator/migrator_json.pyo
%{prefix}/lib/python/couchbase/migrator/migrator_zip.pyc
%{prefix}/lib/python/couchbase/migrator/migrator_zip.pyo
%{prefix}/lib/python/couchbase/rest_client.pyc
%{prefix}/lib/python/couchbase/rest_client.pyo
%{prefix}/lib/python/couchbase/tests/__init__.pyc
%{prefix}/lib/python/couchbase/tests/__init__.pyo
%{prefix}/lib/python/couchbase/tests/test_client.pyc
%{prefix}/lib/python/couchbase/tests/test_client.pyo
%{prefix}/lib/python/couchbase/tests/test_couchbaseclient.pyc
%{prefix}/lib/python/couchbase/tests/test_couchbaseclient.pyo
%{prefix}/lib/python/couchbase/tests/test_restclient.pyc
%{prefix}/lib/python/couchbase/tests/test_restclient.pyo
%{prefix}/lib/python/couchbase/tests/warnings_catcher.pyc
%{prefix}/lib/python/couchbase/tests/warnings_catcher.pyo
%{prefix}/lib/python/couchbase/util.pyc
%{prefix}/lib/python/couchbase/util.pyo
%{prefix}/lib/python/couchbase/utils/__init__.pyc
%{prefix}/lib/python/couchbase/utils/__init__.pyo
%{prefix}/lib/python/couchbase/utils/couchbase-migrator.pyc
%{prefix}/lib/python/couchbase/utils/couchbase-migrator.pyo
%attr(-,root,root) %{prefix}/lib/python/diskqueue_stats.py
%attr(-,root,root) %{prefix}/lib/python/diskqueue_stats.pyc
%attr(-,root,root) %{prefix}/lib/python/diskqueue_stats.pyo
%attr(-,root,root) %{prefix}/lib/python/httplib2/__init__.py
%attr(-,root,root) %{prefix}/lib/python/httplib2/__init__.pyc
%attr(-,root,root) %{prefix}/lib/python/httplib2/__init__.pyo
%attr(-,root,root) %{prefix}/lib/python/httplib2/iri2uri.py
%attr(-,root,root) %{prefix}/lib/python/httplib2/iri2uri.pyc
%attr(-,root,root) %{prefix}/lib/python/httplib2/iri2uri.pyo
%attr(-,root,root) %{prefix}/lib/python/info.py
%attr(-,root,root) %{prefix}/lib/python/info.pyc
%attr(-,root,root) %{prefix}/lib/python/info.pyo
%attr(-,root,root) %{prefix}/lib/python/listservers.py
%attr(-,root,root) %{prefix}/lib/python/listservers.pyc
%attr(-,root,root) %{prefix}/lib/python/listservers.pyo
#%{prefix}/lib/python/mc_bin_client.pyc
#%{prefix}/lib/python/mc_bin_client.pyo
#%{prefix}/lib/python/mc_bin_server.pyc
#%{prefix}/lib/python/mc_bin_server.pyo
#%{prefix}/lib/python/memcacheConstants.pyc
#%{prefix}/lib/python/memcacheConstants.pyo
%attr(-,root,root) %{prefix}/lib/python/node.py
%attr(-,root,root) %{prefix}/lib/python/node.pyc
%attr(-,root,root) %{prefix}/lib/python/node.pyo
%attr(-,root,root) %{prefix}/lib/python/node_stats.py
%attr(-,root,root) %{prefix}/lib/python/node_stats.pyc
%attr(-,root,root) %{prefix}/lib/python/node_stats.pyo
%attr(-,root,root) %{prefix}/lib/python/processor.py
%attr(-,root,root) %{prefix}/lib/python/processor.pyc
%attr(-,root,root) %{prefix}/lib/python/processor.pyo
%attr(-,root,root) %{prefix}/lib/python/restclient.py
%attr(-,root,root) %{prefix}/lib/python/restclient.pyc
%attr(-,root,root) %{prefix}/lib/python/restclient.pyo
%attr(-,root,root) %{prefix}/lib/python/simplejson/LICENSE.txt
%attr(-,root,root) %{prefix}/lib/python/simplejson/__init__.py
%attr(-,root,root) %{prefix}/lib/python/simplejson/__init__.pyc
%attr(-,root,root) %{prefix}/lib/python/simplejson/__init__.pyo
%attr(-,root,root) %{prefix}/lib/python/simplejson/decoder.py
%attr(-,root,root) %{prefix}/lib/python/simplejson/decoder.pyc
%attr(-,root,root) %{prefix}/lib/python/simplejson/decoder.pyo
%attr(-,root,root) %{prefix}/lib/python/simplejson/encoder.py
%attr(-,root,root) %{prefix}/lib/python/simplejson/encoder.pyc
%attr(-,root,root) %{prefix}/lib/python/simplejson/encoder.pyo
%attr(-,root,root) %{prefix}/lib/python/simplejson/scanner.py
%attr(-,root,root) %{prefix}/lib/python/simplejson/scanner.pyc
%attr(-,root,root) %{prefix}/lib/python/simplejson/scanner.pyo
%attr(-,root,root) %{prefix}/lib/python/stats_buffer.py
%attr(-,root,root) %{prefix}/lib/python/stats_buffer.pyc
%attr(-,root,root) %{prefix}/lib/python/stats_buffer.pyo
#%{prefix}/lib/python/tap.pyc
#%{prefix}/lib/python/tap.pyo
#%{prefix}/lib/python/tap_example.pyc
#%{prefix}/lib/python/tap_example.pyo
%attr(-,root,root) %{prefix}/lib/python/usage.py
%attr(-,root,root) %{prefix}/lib/python/usage.pyc
%attr(-,root,root) %{prefix}/lib/python/usage.pyo
#%{prefix}/lib/python/util.pyc
#%{prefix}/lib/python/util.pyo
%attr(-,root,root) %{prefix}/lib/python/util_cli.py
%attr(-,root,root) %{prefix}/lib/python/util_cli.pyc
%attr(-,root,root) %{prefix}/lib/python/util_cli.pyo
%attr(-,root,root) %{prefix}/lib/python/uuid.py
%attr(-,root,root) %{prefix}/lib/python/uuid.pyc
%attr(-,root,root) %{prefix}/lib/python/uuid.pyo
#%{prefix}/share/bucket_engine/collectd.pyc
#%{prefix}/share/bucket_engine/collectd.pyo
#%{prefix}/share/bucket_engine/collectd_memcached_buckets.pyc
#%{prefix}/share/bucket_engine/collectd_memcached_buckets.pyo
#%{prefix}/share/bucket_engine/mc_bin_client.pyc
#%{prefix}/share/bucket_engine/mc_bin_client.pyo
#%{prefix}/share/bucket_engine/memcacheConstants.pyc
#%{prefix}/share/bucket_engine/memcacheConstants.pyo
%{prefix}/var/lib/couchbase/logs
#%{prefix}/var/lib/couchbase/config/config.dat
#%{prefix}/var/lib/couchbase/couchbase-server.cookie
#%{prefix}/var/lib/couchbase/couchbase-server.node
#%{prefix}/var/lib/couchbase/couchbase-server.pid
#%{prefix}/var/lib/couchbase/data/isasl.pw
#%{prefix}/var/lib/couchbase/data/ns_log
#%{prefix}/var/lib/couchbase/erl_crash.dump
#%{prefix}/var/lib/couchbase/mnesia/DECISION_TAB.LOG
#%{prefix}/var/lib/couchbase/mnesia/LATEST.LOG
#%{prefix}/var/lib/couchbase/mnesia/cluster.DCD
#%{prefix}/var/lib/couchbase/mnesia/local_config.DCD
#%{prefix}/var/lib/couchbase/mnesia/schema.DAT
#%{prefix}/var/lib/couchbase/mnesia/stats_archiver-@system-day.DCD
#%{prefix}/var/lib/couchbase/mnesia/stats_archiver-@system-day.DCL
#%{prefix}/var/lib/couchbase/mnesia/stats_archiver-@system-hour.DCD
#%{prefix}/var/lib/couchbase/mnesia/stats_archiver-@system-hour.DCL
#%{prefix}/var/lib/couchbase/mnesia/stats_archiver-@system-minute.DCD
#%{prefix}/var/lib/couchbase/mnesia/stats_archiver-@system-minute.DCL
#%{prefix}/var/lib/couchbase/mnesia/stats_archiver-@system-month.DCD
#%{prefix}/var/lib/couchbase/mnesia/stats_archiver-@system-week.DCD
#%{prefix}/var/lib/couchbase/mnesia/stats_archiver-@system-week.DCL
#%{prefix}/var/lib/couchbase/mnesia/stats_archiver-@system-year.DCD

%pre

CBUSER=%{cbuser}

getent group %{cbuser} >/dev/null || \
   groupadd -r %{cbuser} || exit 1
getent passwd %{cbuser} >/dev/null || \
   useradd -r -g %{cbuser} -d %{prefix} -s /bin/sh \
           -c "cbase system user" %{cbuser} || exit 1

if [ -x %{prefix}/%{name} ]
then
  echo "Stopping cbase-server ..."
  service %{name} stop || true
fi

if [ -d %{prefix} ]
then
  find %{prefix} -maxdepth 1 -type l | xargs rm -f || true
fi
exit 0


%post

if test X"$RPM_INSTALL_PREFIX0" = X"" ; then
  RPM_INSTALL_PREFIX0=%{prefix}
fi

if test X"$RPM_INSTALL_PREFIX1" = X"" ; then
  RPM_INSTALL_PREFIX1=/etc/init.d
fi

/sbin/chkconfig --add %{name}

# From http://www.rpm.org/max-rpm-snapshot/s1-rpm-inside-scripts.html
# The argument to the %post script is 2 on an upgrade.
if [ -n "$INSTALL_UPGRADE_CONFIG_DIR" -o "$1" == "2" ]
then
  if [ -z "$INSTALL_UPGRADE_CONFIG_DIR" ]
  then
    INSTALL_UPGRADE_CONFIG_DIR=$RPM_INSTALL_PREFIX0/var/lib/couchbase/config
  fi
  echo Upgrading cbase-server ...
  echo "  $RPM_INSTALL_PREFIX0/bin/cbupgrade -c $INSTALL_UPGRADE_CONFIG_DIR -a yes $INSTALL_UPGRADE_EXTRA"
  if [ "$INSTALL_DONT_AUTO_UPGRADE" != "1" ]
  then
    $RPM_INSTALL_PREFIX0/bin/cbupgrade -c $INSTALL_UPGRADE_CONFIG_DIR -a yes $INSTALL_UPGRADE_EXTRA
  else
    echo Skipping cbupgrade due to INSTALL_DONT_AUTO_UPGRADE ...
  fi
fi

chown  -R %{cbuser}: %{prefix}/var
service cbase start
exit 0


%preun

service cbase stop || true

#find $RPM_INSTALL_PREFIX0 -name '*.pyc' | xargs rm -f || true
#rm -f $RPM_INSTALL_PREFIX0/bin/*.bin

/sbin/chkconfig --del %{name}

exit 0


%changelog
* Tue Jun 18 2012 Albert Zhang <albertwzhang@gmail.com>
- Initial cbase repo
