Name:	moxi
Version: 1.8.0_8_g52a5fa8
Release:	902.2%{?dist}
Summary:	a memcached proxy with energy and pep
Group:		System Environment/Daemons
License:	BSD
URL:		http://northscale.com
Source0:	http://northscale.com/moxi/dist/%{name}-%{version}.tar.gz
Source1:	moxi.conf
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	automake
BuildRequires:	autoconf
BuildRequires:	libtool
BuildRequires:	openssl-devel
BuildRequires:  libevent-devel
BuildRequires:  pkgconfig
BuildRequires:  sqlite-devel
BuildRequires:  check-devel
BuildRequires:  libmemcached-devel
BuildRequires:  libvbucket-devel
BuildRequires:  libconflate-devel
Requires:       openssl
Requires:	libevent
Requires:	libvbucket >= 1.8.0-901.1
Requires:	libmemcached
Requires:	libconflate
Requires:       sqlite

Patch0:  moxi-cfg.patch

%description
moxi is a memcached proxy with several optimizations to bring efficiency to
many memcached deployments, especially those with heavy workloads or
complex network topologies.  Optimizations include handling timeouts for
the client, deduplication of requests, a 'front' cache and protocol
(ascii to binary) conversion.  These optimizations keep the 'contract'
of the memcached protocol whole for clients.

%prep
%setup -q
%patch0 -p1

%build
[ -x config/autorun.sh ] && config/autorun.sh
CONFLATE_DB_PATH=/var/lib/moxi %configure --disable-coverage --disable-debug --disable-shared \
	--without-memcached --without-check	\
	--enable-moxi-libvbucket	\
	--enable-moxi-libmemcached

make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR="%{buildroot}" AM_INSTALL_PROGRAM_FLAGS=""
# don't include libs and headers for conflate & strophe
rm -rf %{buildroot}/usr/lib
rm -rf %{buildroot}/usr/include

# Init script
sed -e 's/%%{version}/%{version}/g' < scripts/moxi-init.rhat.in > scripts/moxi-init.rhat
install -Dp -m0755 scripts/moxi-init.rhat %{buildroot}%{_initrddir}/moxi
install -D -p -m 0600 %{SOURCE1} %{buildroot}%{_sysconfdir}/%{name}.conf
# Default configs
mkdir -p %{buildroot}/%{_sysconfdir}/sysconfig
cat <<EOF >%{buildroot}/%{_sysconfdir}/sysconfig/%{name}
# Change this with the cbase server info
# use host1,host2 form for a multi-server configuration
CBASE_HOST='host1,host2'
CBASE_BUCKET=''
CBASE_PWD=''
USER="nobody"
MAXCONN="1024"
CPROXY_ARG="/etc/moxi.conf"
OPTIONS=""

EOF

# pid directory
mkdir -p %{buildroot}/%{_localstatedir}/run/moxi
mkdir -p %{buildroot}/%{_localstatedir}/lib/moxi

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README doc/CONTRIBUTORS scripts/examples/
%doc /usr/share/man/man1/moxi.1.gz
%config(noreplace) %attr(600,nobody,nobody) %{_sysconfdir}/sysconfig/%{name}
%config(noreplace) %attr(600,nobody,nobody) %{_sysconfdir}/%{name}.conf
%dir %attr(750,nobody,nobody) %{_localstatedir}/run/moxi
%dir %attr(750,nobody,nobody) %{_localstatedir}/lib/moxi
%{_bindir}/moxi
%{_initrddir}/moxi

%changelog
* Mon Jul 8 2013 Albert Zhang <zhgwenming@gmail.com>
- fix mem leak issue
* Tue Jul 1 2013 Albert Zhang <zhgwenming@gmail.com>
- new format of sysconfig file
* Tue Jul 28 2009 Aliaksey Kandratsenka <alk@tut.by>
- packaged documentation and config-file examples
* Mon Jul 27 2009 Aliaksey Kandratsenka <alk@tut.by>
- startup script
* Fri Jul 17 2009 Matt Ingenthron <ingenthr@cep.net>
- Updated install locations and removed memcached dependency
* Fri Jul 17 2009 Aliaksey Kandratsenka <alk@tut.by>
- initial
