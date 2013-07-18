Name:           cbase
Version:        1.8.1
Release:        905.1%{dist}
Epoch:          0
Summary:	A memcached cache cluster
Group:		System Environment/Daemons
License:	BSD
URL:            http://github.com/northscale
Source0:	http://northscale.com/cbase/dist/%{name}-%{version}.tar.gz
Source1:	cbase_init.d.tmpl
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-%(%{__id_u} -n)

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
Requires:	moxi
Requires:	memcached
Requires:	bucket-engine
Requires:	ep-engine
Requires:	vbucketmigrator
Requires:       sqlite
Requires:       erlang
Requires:       sigar

%define pkgroot	/opt/%{pkgvendor}
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
%setup -q -n %{name}-%{version}

%build
./configure --prefix=%{prefix}

#%check
#make test

%install
make %{?_smp_mflags} install DESTDIR=%{buildroot}
#make install "PREFIX=%{buildroot}/%{prefix}"
#rm -rf %{buildroot}
#make install PREFIX=%{buildroot}
#find $RPM_BUILD_ROOT -type f -name '*.la' -exec rm -f {} ';'

mkdir -p %{buildroot}%{_initrddir}
mkdir -p %{buildroot}%{prefix}/var/lib/couchbase/logs

sed 's/@@PRODUCT@@/couchbase-server/; s/@@PRODUCT_BASE@@/couchbase/;
	s,@@PREFIX@@,%{prefix},'	\
	%{SOURCE1} > %{buildroot}%{_initrddir}/%{name}

chmod +x %{buildroot}%{_initrddir}/%{name}

ln -s /usr/bin/moxi %{buildroot}%{prefix}/bin/moxi
ln -s /usr/bin/memcached %{buildroot}%{prefix}/bin/memcached
ln -s %{_libdir}/memcached %{buildroot}%{prefix}/lib/memcached


%clean
#rm -rf %{buildroot}

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

%files
%defattr(-,root,root,-)
%dir %{prefix}/bin
%dir %{prefix}/etc
%dir %{prefix}/etc/couchbase
%dir %{prefix}/lib
%dir %{prefix}/lib/memcached
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
%dir %{prefix}/var
%dir %{prefix}/var/lib
%dir %{prefix}/var/lib/couchbase
%dir %{prefix}/var/lib/couchbase/mnesia
%{_initrddir}/%{name}
%{prefix}/bin/moxi
%{prefix}/bin/memcached
%{prefix}/bin/cbbrowse_logs
%{prefix}/bin/cbcollect_info
%{prefix}/bin/cbdumpconfig.escript
%{prefix}/bin/couchbase-server
%{prefix}/bin/ebucketmigrator
%config(noreplace) %{prefix}/etc/couchbase/config
%config(noreplace) %{prefix}/etc/couchbase/init.sql
%config(noreplace) %{prefix}/etc/couchbase/static_config
%{prefix}/var/lib/couchbase/logs

%{prefix}/lib/memcached
%{prefix}/lib/ns_server/erlang/lib/ale/ebin/ale.app
%{prefix}/lib/ns_server/erlang/lib/ale/ebin/ale.beam
%{prefix}/lib/ns_server/erlang/lib/ale/ebin/ale_app.beam
%{prefix}/lib/ns_server/erlang/lib/ale/ebin/ale_codegen.beam
%{prefix}/lib/ns_server/erlang/lib/ale/ebin/ale_default_formatter.beam
%{prefix}/lib/ns_server/erlang/lib/ale/ebin/ale_disk_sink.beam
%{prefix}/lib/ns_server/erlang/lib/ale/ebin/ale_dynamic_sup.beam
%{prefix}/lib/ns_server/erlang/lib/ale/ebin/ale_error_logger_handler.beam
%{prefix}/lib/ns_server/erlang/lib/ale/ebin/ale_stderr_sink.beam
%{prefix}/lib/ns_server/erlang/lib/ale/ebin/ale_sup.beam
%{prefix}/lib/ns_server/erlang/lib/ale/ebin/ale_transform.beam
%{prefix}/lib/ns_server/erlang/lib/ale/ebin/ale_utils.beam
%{prefix}/lib/ns_server/erlang/lib/ale/ebin/dynamic_compile.beam
%{prefix}/lib/ns_server/erlang/lib/erlwsh/ebin/erlwsh.app
%{prefix}/lib/ns_server/erlang/lib/erlwsh/ebin/erlwsh.beam
%{prefix}/lib/ns_server/erlang/lib/erlwsh/ebin/erlwsh_app.beam
%{prefix}/lib/ns_server/erlang/lib/erlwsh/ebin/erlwsh_deps.beam
%{prefix}/lib/ns_server/erlang/lib/erlwsh/ebin/erlwsh_sup.beam
%{prefix}/lib/ns_server/erlang/lib/erlwsh/ebin/erlwsh_web.beam
%{prefix}/lib/ns_server/erlang/lib/erlwsh/ebin/eshell.beam
%{prefix}/lib/ns_server/erlang/lib/erlwsh/priv/www/index.html
%{prefix}/lib/ns_server/erlang/lib/erlwsh/priv/www/prototype.js
%{prefix}/lib/ns_server/erlang/lib/gen_smtp/ebin/binstr.beam
%{prefix}/lib/ns_server/erlang/lib/gen_smtp/ebin/gen_smtp.app
%{prefix}/lib/ns_server/erlang/lib/gen_smtp/ebin/gen_smtp_client.beam
%{prefix}/lib/ns_server/erlang/lib/gen_smtp/ebin/gen_smtp_server.beam
%{prefix}/lib/ns_server/erlang/lib/gen_smtp/ebin/gen_smtp_server_session.beam
%{prefix}/lib/ns_server/erlang/lib/gen_smtp/ebin/mimemail.beam
%{prefix}/lib/ns_server/erlang/lib/gen_smtp/ebin/smtp_server_example.beam
%{prefix}/lib/ns_server/erlang/lib/gen_smtp/ebin/smtp_util.beam
%{prefix}/lib/ns_server/erlang/lib/gen_smtp/ebin/socket.beam
%{prefix}/lib/ns_server/erlang/lib/mochiweb/ebin/mochifmt.beam
%{prefix}/lib/ns_server/erlang/lib/mochiweb/ebin/mochifmt_records.beam
%{prefix}/lib/ns_server/erlang/lib/mochiweb/ebin/mochifmt_std.beam
%{prefix}/lib/ns_server/erlang/lib/mochiweb/ebin/mochihex.beam
%{prefix}/lib/ns_server/erlang/lib/mochiweb/ebin/mochijson.beam
%{prefix}/lib/ns_server/erlang/lib/mochiweb/ebin/mochijson2.beam
%{prefix}/lib/ns_server/erlang/lib/mochiweb/ebin/mochinum.beam
%{prefix}/lib/ns_server/erlang/lib/mochiweb/ebin/mochiweb.app
%{prefix}/lib/ns_server/erlang/lib/mochiweb/ebin/mochiweb.beam
%{prefix}/lib/ns_server/erlang/lib/mochiweb/ebin/mochiweb_app.beam
%{prefix}/lib/ns_server/erlang/lib/mochiweb/ebin/mochiweb_charref.beam
%{prefix}/lib/ns_server/erlang/lib/mochiweb/ebin/mochiweb_cookies.beam
%{prefix}/lib/ns_server/erlang/lib/mochiweb/ebin/mochiweb_echo.beam
%{prefix}/lib/ns_server/erlang/lib/mochiweb/ebin/mochiweb_headers.beam
%{prefix}/lib/ns_server/erlang/lib/mochiweb/ebin/mochiweb_html.beam
%{prefix}/lib/ns_server/erlang/lib/mochiweb/ebin/mochiweb_http.beam
%{prefix}/lib/ns_server/erlang/lib/mochiweb/ebin/mochiweb_multipart.beam
%{prefix}/lib/ns_server/erlang/lib/mochiweb/ebin/mochiweb_request.beam
%{prefix}/lib/ns_server/erlang/lib/mochiweb/ebin/mochiweb_response.beam
%{prefix}/lib/ns_server/erlang/lib/mochiweb/ebin/mochiweb_skel.beam
%{prefix}/lib/ns_server/erlang/lib/mochiweb/ebin/mochiweb_socket_server.beam
%{prefix}/lib/ns_server/erlang/lib/mochiweb/ebin/mochiweb_sup.beam
%{prefix}/lib/ns_server/erlang/lib/mochiweb/ebin/mochiweb_util.beam
%{prefix}/lib/ns_server/erlang/lib/mochiweb/ebin/reloader.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/addr_util.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/auto_failover.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/auto_failover_logic.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/cb_init_loggers.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/cucumberl.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/diag_handler.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/dist_manager.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ebucketmigrator.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ebucketmigrator_srv.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/failover_safeness_level.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/gen_sup.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/hot_keys_keeper.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/log_os_info.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/master_activity_events.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/master_activity_events_keeper.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/master_activity_events_pids_watcher.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/mb_grid.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/mb_map.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/mb_master.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/mb_master_sup.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/mb_mnesia.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/mb_mnesia_sup.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/mc_binary.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/mc_client_binary.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/menelaus_alert.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/menelaus_auth.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/menelaus_deps.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/menelaus_event.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/menelaus_rest.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/menelaus_stats.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/menelaus_sup.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/menelaus_util.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/menelaus_web.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/menelaus_web_alerts_srv.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/menelaus_web_buckets.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/misc.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/misc_tests.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/mock.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/mock_gen_server.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_bootstrap.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_bucket.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_bucket_sup.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_cluster.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_cluster_membership.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_config.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_config_default.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_config_ets_dup.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_config_isasl_sync.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_config_log.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_config_rep.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_config_replica.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_config_sup.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_config_tests.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_cookie_manager.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_doctor.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_error_messages.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_heart.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_info.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_janitor.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_janitor_vis.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_log.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_log_browser.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_log_categorizing.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_log_sink.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_mail.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_mail_log.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_mail_sup.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_memcached.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_moxi_sup.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_node_disco.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_node_disco_conf_events.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_node_disco_log.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_node_disco_rep_events.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_node_disco_sup.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_orchestrator.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_port_init.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_port_server.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_port_sup.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_process_registry.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_pubsub.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_rebalancer.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_replicas_builder.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_server.app
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_server.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_server_cluster_sup.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_server_sup.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_single_vbucket_mover.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_storage_conf.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_test_util.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_tick.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_vbm_sup.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_vbucket_mover.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ns_watchdog.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/path_config.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ringbuffer.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/ringdict.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/single_bucket_sup.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/stats_archiver.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/stats_collector.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/stats_reader.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/supervisor_cushion.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/system_stats_collector.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/t.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/timeout_diag_logger.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/uuid.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/vclock.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/ebin/work_queue.beam
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/css/jquery-ui.couchbase.css
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/css/print.css
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/css/screen.css
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/favicon.ico
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/add_back_bg.png
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/add_back_btn.png
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/add_btn.png
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/alert_1.gif
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/alert_green.png
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/alert_red.png
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/attention_bg.gif
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/auth_form_bg.png
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/background.png
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/bg_h2.gif
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/bg_li_th.gif
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/bg_time_act.gif
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/bg_total.gif
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/blue-button.png
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/blue_block_bg.gif
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/btn_1_bg.png
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/btn_2_bg.png
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/btn_cancel_bg.png
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/button_blue.gif
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/button_blue_3.gif
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/button_gray_200.gif
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/button_gray_big.gif
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/button_gray_medium.gif
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/button_red.gif
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/config-bottom.png
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/config-top.png
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/couchbase_logo.png
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/couchbase_welcome_background.png
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/crn_hdr_err.gif
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/devider_line_1.gif
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/devider_line_2.gif
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/edit-button.png
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/elastro_cling_v22.png
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/expander_2_bg.gif
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/expander_bg.gif
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/footer_bg.png
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/gong_rb.gif
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/gong_rb_2.gif
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/gray_box_bg.gif
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/header_bg.png
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/ico_server_big.png
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/icons.png
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/info_bg.gif
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/large_buttons_bg.gif
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/lbox_b.png
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/lbox_cent.png
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/lbox_lb.png
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/lbox_lt.png
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/lbox_rb.png
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/lbox_rt.png
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/lbox_t.png
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/login_screen.png
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/membase-logo.png
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/mini_graph_bg.gif
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/no-preload/mokugift-tree.gif
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/server_icon.gif
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/server_icon.png
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/server_status_icons.png
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/server_status_icons_solid_bg.png
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/setup-button.png
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/shadow_box_bg.gif
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/shadow_box_side_bg.gif
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/sign_in_button.gif
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/spinner/spinner2_gr_nav.gif
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/spinner/spinner_1.gif
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/spinner/spinner_3.gif
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/spinner/spinner_gr_nav.gif
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/spinner/spinner_lightbox.gif
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/switcher_bg.png
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/tooltip_bg.gif
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/tooltip_bg_777777.png
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/ui-theme/ui-bg_flat_0_000000_40x100.png
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/ui-theme/ui-bg_flat_75_ffffff_40x100.png
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/ui-theme/ui-bg_glass_55_fbf9ee_1x400.png
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/ui-theme/ui-bg_glass_65_ffffff_1x400.png
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/ui-theme/ui-bg_glass_75_dadada_1x400.png
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/ui-theme/ui-bg_glass_75_e6e6e6_1x400.png
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/ui-theme/ui-bg_glass_95_fef1ec_1x400.png
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/ui-theme/ui-bg_highlight-soft_75_cccccc_1x100.png
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/ui-theme/ui-icons_222222_256x240.png
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/ui-theme/ui-icons_2e83ff_256x240.png
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/ui-theme/ui-icons_454545_256x240.png
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/ui-theme/ui-icons_888888_256x240.png
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/ui-theme/ui-icons_cd0a0a_256x240.png
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/usage_big.gif
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/usage_small.gif
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/usage_small_2.gif
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/usages.png
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/vlabels.gif
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/warning_bg.gif
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/warning_bg_2.png
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/images/welcome-setup-button.png
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/index.html
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/js/all-images.js
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/js/analytics.js
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/js/app-misc.js
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/js/app-ui-misc.js
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/js/app.js
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/js/base64.js
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/js/buckets.js
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/js/cells.js
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/js/core-data.js
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/js/excanvas.min.js
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/js/hooks.js
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/js/jquery-ui-1.8.10.custom.js
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/js/jquery.ba-bbq.js
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/js/jquery.cookie.js
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/js/jquery.flot.js
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/js/jquery.js
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/js/jquery.sparkline.js
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/js/json2.js
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/js/misc.js
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/js/overview.js
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/js/servers.js
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/js/settings.js
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/js/tools.tabs.js
%{prefix}/lib/ns_server/erlang/lib/ns_server-1.8.0_362_gf2930c1/priv/public/js/underscore.js

%changelog
* Wed Jul 17 2013 Albert Zhang <zhgwenming@gmail.com>
- Initial import


