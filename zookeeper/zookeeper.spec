Name:          zookeeper
Version:       3.4.5
Release:       1%{?dist}
Summary:       A high-performance coordination service for distributed applications
Group:         Development/Libraries
License:       ASL 2.0
URL:           http://zookeeper.apache.org/
Source0:       http://www.apache.org/dist/zookeeper/%{name}-%{version}/%{name}-%{version}.tar.gz
# remove non free clover references
# configure ivy to use system libraries
# disable rat-lib and jdiff support
Patch0:        %{name}-3.4.4-build.patch
# https://issues.apache.org/jira/browse/ZOOKEEPER-1557
Patch1:        https://issues.apache.org/jira/secure/attachment/12548109/ZOOKEEPER-1557.patch
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
BuildRequires: checkstyle
BuildRequires: jline
BuildRequires: junit
BuildRequires: log4j
BuildRequires: mockito
BuildRequires: netty
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
Requires:      netty
Requires:      slf4j

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
%patch1 -p0
%pom_remove_dep org.vafer:jdeb dist-maven/%{name}-%{version}.pom
# jdiff task deps
%pom_remove_dep jdiff:jdiff dist-maven/%{name}-%{version}.pom
%pom_remove_dep xerces:xerces dist-maven/%{name}-%{version}.pom
# rat-lib task deps
%pom_remove_dep org.apache.rat:apache-rat-tasks dist-maven/%{name}-%{version}.pom
%pom_remove_dep commons-collections:commons-collections dist-maven/%{name}-%{version}.pom
%pom_remove_dep commons-lang:commons-lang dist-maven/%{name}-%{version}.pom

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
popd

find %{buildroot} -name '*.la' -exec rm -f {} ';'

# TODO
# bin/zkCleanup.sh
# bin/zkCli.sh
# bin/zkEnv.sh
# bin/zkServer.sh

%check
pushd src/c
make check
popd
# skip for now
#%%ant test-core-java

%post lib -p /sbin/ldconfig
%postun lib -p /sbin/ldconfig

%files 
%defattr(-,root,root,-)
%{_bindir}/cli_mt
%{_bindir}/cli_st
%{_bindir}/load_gen
%doc src/c/ChangeLog src/c/LICENSE src/c/NOTICE.txt src/c/README

%files lib
%defattr(-,root,root,-)
%{_libdir}/lib*.so.*
%doc src/c/LICENSE src/c/NOTICE.txt

%files lib-devel
%defattr(-,root,root,-)
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*.h
%{_libdir}/*.so
%doc src/c/LICENSE src/c/NOTICE.txt src/c/docs/html/*

%files java
%{_javadir}/%{name}.jar
%{_mavenpomdir}/JPP-%{name}.pom
%{_mavendepmapfragdir}/%{name}
%doc CHANGES.txt LICENSE.txt NOTICE.txt README.txt

%files javadoc
%{_javadocdir}/%{name}
%doc LICENSE.txt NOTICE.txt

%changelog
* Sun Dec 02 2012 gil cattaneo <puntogil@libero.it> 3.4.5-1
- update to 3.4.5

* Tue Oct 30 2012 gil cattaneo <puntogil@libero.it> 3.4.4-3
- fix missing hostname

* Fri Oct 12 2012 gil cattaneo <puntogil@libero.it> 3.4.4-2
- add ant-junit as BR

* Fri Oct 12 2012 gil cattaneo <puntogil@libero.it> 3.4.4-1
- update to 3.4.4

* Fri May 18 2012 gil cattaneo <puntogil@libero.it> 3.4.3-1
- initial rpm