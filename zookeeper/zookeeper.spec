Name:          zookeeper
Version:       3.3.6
Release:       8%{?dist}
Summary:       A high-performance coordination service for distributed applications
Group:         Development/Libraries
License:       ASL 2.0
URL:           http://zookeeper.apache.org/
Source0:       http://www.apache.org/dist/zookeeper/%{name}-%{version}/%{name}-%{version}.tar.gz
Source1:       zookeeper.upstart
Source2:       zookeeper.sysconfig
Source3:       zookeeper.init
Source4:       zoo.cfg
Source5:       log4j.properties
Source6:       myid
# remove non free clover references
# configure ivy to use system libraries
# disable rat-lib and jdiff support
Patch0:        %{name}-3.3.6-build.patch
# https://issues.apache.org/jira/browse/ZOOKEEPER-1557
Patch1:        https://issues.apache.org/jira/secure/attachment/12548109/ZOOKEEPER-1557.patch
Patch2:        %{name}-3.3.6-ivy.patch
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: cppunit-devel
BuildRequires: dos2unix
BuildRequires: doxygen
BuildRequires: graphviz
BuildRequires: java-devel
BuildRequires: java-javadoc
BuildRequires: jpackage-utils
BuildRequires: libtool

BuildRequires: ant
BuildRequires: ant-junit
BuildRequires: apache-ivy
#BuildRequires: checkstyle
BuildRequires: jline
BuildRequires: junit
BuildRequires: log4j
#BuildRequires: mockito
BuildRequires: slf4j

# BuildRequires: rat-lib
# BuildRequires: apache-rat-tasks
# BuildRequires: apache-commons-collections
# BuildRequires: apache-commons-lang
# BuildRequires: jdiff
# BuildRequires: xerces-j2

%description
ZooKeeper is a centralized service for maintaining configuration information,
naming, providing distributed synchronization, and providing group services.

%package server
Summary:       Zookeeper Server
Group:         System Environment/Daemons
Requires:      zookeeper-java
BuildArch:     noarch

%description server
Zookeeper Server.
For general information about Zookeeper please see %{url}

%package lib
Summary:       Zookeeper C client library
Group:         System Environment/Libraries

%description lib
This package provides a C client interface to Zookeeper server.
For general information about Zookeeper please see %{url}

%package lib-devel
Summary:       Development files for the %{name} library
Group:         Development/Libraries
Requires:      %{name}-lib = %{version}-%{release}

%description lib-devel
Development files for the %{name} library.

%package java
Group:         Development/Libraries
Summary:       Zookeeper Java client library
# Requires:      felix-framework
# Requires:      felix-osgi-compendium
Requires:      jline
Requires:      log4j
Requires:      slf4j
Requires:      jre >= 1.6.0

Requires:      java
Requires:      jpackage-utils
BuildArch:     noarch

%description java
This package provides a Java client interface to Zookeeper server.

%package javadoc
Group:         Documentation
Summary:       Javadoc for %{name}
Requires:      jpackage-utils
BuildArch:     noarch

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q
find -name "*.jar" -delete
find -name "*.class" -delete
find -name "*.cmd" -delete
find -name "*.so*" -delete
find -name "*.dll" -delete

%patch0 -p1
#%patch2 -p1
#%patch1 -p0
#%pom_remove_dep org.vafer:jdeb dist-maven/%{name}-%{version}.pom
## jdiff task deps
#%pom_remove_dep jdiff:jdiff dist-maven/%{name}-%{version}.pom
#%pom_remove_dep xerces:xerces dist-maven/%{name}-%{version}.pom
## rat-lib task deps
#%pom_remove_dep org.apache.rat:apache-rat-tasks dist-maven/%{name}-%{version}.pom
#%pom_remove_dep commons-collections:commons-collections dist-maven/%{name}-%{version}.pom
#%pom_remove_dep commons-lang:commons-lang dist-maven/%{name}-%{version}.pom

sed -i "s|<packaging>pom</packaging>|<packaging>jar</packaging>|" dist-maven/%{name}-%{version}.pom
sed -i "s|<groupId>checkstyle</groupId>|<groupId>com.puppycrawl.tools</groupId>|" dist-maven/%{name}-%{version}.pom
sed -i "s|<artifactId>mockito-all</artifactId>|<artifactId>mockito-core</artifactId>|" dist-maven/%{name}-%{version}.pom

iconv -f iso8859-1 -t utf-8 src/c/ChangeLog > src/c/ChangeLog.conv && mv -f src/c/ChangeLog.conv src/c/ChangeLog
sed -i 's/\r//' src/c/ChangeLog

# fix build problem on f18
sed -i 's|<exec executable="hostname" outputproperty="host.name"/>|<!--exec executable="hostname" outputproperty="host.name"/-->|' build.xml
sed -i 's|<attribute name="Built-On" value="${host.name}" />|<attribute name="Built-On" value="${user.name}" />|' build.xml

%build

%ant -Djavadoc.link.java=%{_javadocdir}/java build-generated jar javadoc

pushd src/c
rm -rf autom4te.cache
autoreconf -fis

%configure --disable-static --disable-rpath --with-syncapi
# Remove rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
%{__make} %{?_smp_mflags}
make doxygen-doc
popd

%install

mkdir -p %{buildroot}%{_javadir}
install -pm 644 build/%{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar

mkdir -p %{buildroot}%{_mavenpomdir}
install -pm 644 dist-maven/%{name}-%{version}.pom %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom
%add_maven_depmap JPP-%{name}.pom %{name}.jar

mkdir -p %{buildroot}%{_javadocdir}/%{name}
cp -pr build/docs/api/* %{buildroot}%{_javadocdir}/%{name}/

pushd src/c
%{__make} install DESTDIR=%{buildroot}
# cleanup
rm -f docs/html/*.map
mv %{buildroot}/usr/include/c-client-src/ %{buildroot}/usr/include/%{name}
popd

find %{buildroot} -name '*.la' -exec rm -f {} ';'

# TODO
# bin/zkCleanup.sh
# bin/zkCli.sh
# bin/zkEnv.sh
# bin/zkServer.sh
install -d -m 755 %{buildroot}%{_datadir}/%{name}/bin
install -d -m 755 %{buildroot}%{_sharedstatedir}/%{name}
install -d -m 755 %{buildroot}%{_localstatedir}/log/%{name}
#install -d -m 755 %{buildroot}%{_localstatedir}/run/%{name}

install -m 755 bin/zkCleanup.sh %{buildroot}%{_datadir}/%{name}/bin/zkCleanup.sh
install -m 755 bin/zkCli.sh %{buildroot}%{_datadir}/%{name}/bin/zkCli.sh
install -m 755 bin/zkEnv.sh %{buildroot}%{_datadir}/%{name}/bin/zkEnv.sh
install -m 755 bin/zkServer.sh %{buildroot}%{_datadir}/%{name}/bin/zkServer.sh
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_datadir}/%{name}/zookeeper.upstart
install -p -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/%{name}
install -p -D -m 755 %{SOURCE3} %{buildroot}%{_initddir}/%{name}

# configuration.xsl  log4j.properties  zoo_sample.cfg
install -p -D -m 644 conf/configuration.xsl %{buildroot}%{_defaultdocdir}/%{name}-%{version}/examples/conf/configuration.xsl
install -p -D -m 644 conf/log4j.properties %{buildroot}%{_defaultdocdir}/%{name}-%{version}/examples/conf/log4j.properties
install -p -D -m 644 conf/zoo_sample.cfg %{buildroot}%{_defaultdocdir}/%{name}-%{version}/examples/conf/zoo_sample.cfg

install -p -D -m 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/zookeeper/conf/zoo.cfg
install -p -D -m 644 %{SOURCE5} %{buildroot}%{_sysconfdir}/zookeeper/conf/log4j.properties
install -p -D -m 644 %{SOURCE6} %{buildroot}%{_sysconfdir}/zookeeper/conf/myid
install -p -D -m 644 conf/configuration.xsl %{buildroot}%{_sysconfdir}/zookeeper/conf/configuration.xsl
ln -nsf /etc/zookeeper/conf/myid %{buildroot}%{_sharedstatedir}/%{name}/myid

%check
pushd src/c
make check
popd
# skip for now
#%%ant test-core-java

%pre server
# 201:201 for zookeeper
getent group zookeeper >/dev/null || groupadd -r --gid 201 zookeeper
getent passwd zookeeper >/dev/null || \
useradd --uid 201 -r -g zookeeper -d %{_sharedstatedir}/%{name} -s /sbin/nologin \
-c "Zookeeper server" zookeeper

%preun server
/sbin/service %{name} stop >/dev/null 2>&1
/sbin/chkconfig --del %{name}

%post lib -p /sbin/ldconfig
%postun lib -p /sbin/ldconfig

%files 
%defattr(-,root,root,-)
%{_bindir}/cli_mt
%{_bindir}/cli_st
%{_bindir}/load_gen
%{_datadir}/%{name}/bin/zkCleanup.sh
%{_datadir}/%{name}/bin/zkCli.sh
%{_datadir}/%{name}/bin/zkEnv.sh
%{_datadir}/%{name}/bin/zkServer.sh

%doc src/c/ChangeLog src/c/LICENSE src/c/README

%files server
%config(noreplace) %attr(-, root, zookeeper) %{_sysconfdir}/sysconfig/zookeeper
%config(noreplace) %attr(-, root, zookeeper) %{_sysconfdir}/zookeeper/conf/configuration.xsl
%config(noreplace) %attr(-, root, zookeeper) %{_sysconfdir}/zookeeper/conf/log4j.properties
%config(noreplace) %attr(-, root, zookeeper) %{_sysconfdir}/zookeeper/conf/zoo.cfg
%config(noreplace) %attr(-, root, zookeeper) %{_sysconfdir}/zookeeper/conf/myid
#%doc conf/configuration.xsl conf/log4j.properties conf/zoo_sample.cfg
%doc conf/
%dir %attr(0755, zookeeper, root) %{_localstatedir}/log/%{name}
%dir %attr(0755, zookeeper, root) %{_sharedstatedir}/%{name}
%{_sharedstatedir}/%{name}/myid
%{_datadir}/%{name}/zookeeper.upstart
%{_initddir}/%{name}


%files lib
%defattr(-,root,root,-)
%{_libdir}/lib*.so.*
%doc src/c/LICENSE

%files lib-devel
%defattr(-,root,root,-)
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*.h
%{_libdir}/*.so
%doc src/c/LICENSE src/c/docs/html/*

%files java
%{_javadir}/%{name}.jar
%{_mavenpomdir}/JPP-%{name}.pom
%{_mavendepmapfragdir}/%{name}
%doc CHANGES.txt LICENSE.txt README.txt

%files javadoc
%{_javadocdir}/%{name}
%doc LICENSE.txt 

%changelog

* Fri Jan 14 2013 Albert Zhang <zhgwenming@gmail.com> 3.3.6
- initial rpm, permission fixes
