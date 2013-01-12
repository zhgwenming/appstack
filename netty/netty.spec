Name:           netty
Version:        3.2.4
Release:        3%{?dist}
Summary:        An asynchronous event-driven network application framework and tools for Java

Group:          Development/Libraries
License:        ASL 2.0
URL:            http://www.jboss.org/netty
Source0:        http://sourceforge.net/projects/jboss/files/%{name}-%{version}.Final-dist.tar.bz2

Patch0:         0001-Remove-optional-deps.patch
Patch1:         0002-Replace-jboss-logger-with-jdk-logger.patch
Patch2:         0003-Fix-javadoc-plugin-configuration.patch
Patch3:         0004-Remove-antun-execution-for-removing-examples.patch
Patch4:         0005-Remove-eclipse-plugin.patch

BuildArch:     noarch

# This pulls in all of the required java and maven stuff
BuildRequires:  maven
#BuildRequires:  maven-antrun-plugin
#BuildRequires:  maven-assembly-plugin
#BuildRequires:  maven-compiler-plugin
#BuildRequires:  maven-javadoc-plugin
#BuildRequires:  maven-resources-plugin
#BuildRequires:  maven-release-plugin
#BuildRequires:  maven-source-plugin
#BuildRequires:  maven-surefire-plugin
#BuildRequires:  maven-plugin-bundle
#BuildRequires:  buildnumber-maven-plugin
BuildRequires:  ant-contrib
BuildRequires:  subversion
BuildRequires:  protobuf-java
#BuildRequires:  felix-osgi-compendium
#BuildRequires:  jboss-parent

Requires:       java
Requires:       protobuf-java

%description
Netty is a NIO client server framework which enables quick and easy
development of network applications such as protocol servers and
clients. It greatly simplifies and streamlines network programming
such as TCP and UDP socket server.

'Quick and easy' doesn't mean that a resulting application will suffer
from a maintainability or a performance issue. Netty has been designed
carefully with the experiences earned from the implementation of a lot
of protocols such as FTP, SMTP, HTTP, and various binary and
text-based legacy protocols. As a result, Netty has succeeded to find
a way to achieve ease of development, performance, stability, and
flexibility without a compromise.


%package javadoc
Summary:   API documentation for %{name}
Group:     Documentation
Requires:  jpackage-utils

%description javadoc
%{summary}.

%prep
%setup -q -n %{name}-%{version}.Final

# just to be sure, but not used anyway
rm -rf jar/

# example doesn't build with our protobuf
rm -rf src/main/java/org/jboss/netty/example/localtime


%patch0 -p1
%patch1 -p1

# we don't have jboss logging facilites so we replace it with jdk logger
rm src/main/java/org/jboss/netty/logging/JBossLogger*.java
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
# skipping tests because we don't have all dependencies in Fedora
mvn-rpmbuild -Dmaven.test.skip=true \
        install javadoc:javadoc


%install
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}

install -m 644 target/%{name}-%{version}.Final.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}.jar


install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -pr target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -pm 644 pom.xml $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP-%{name}.pom

%add_maven_depmap JPP-%{name}.pom %{name}.jar

%files
%doc LICENSE.txt NOTICE.txt
%{_javadir}/%{name}.jar
%{_mavendepmapfragdir}/%{name}
%{_mavenpomdir}/JPP-%{name}.pom

%files javadoc
%doc LICENSE.txt NOTICE.txt
%{_javadocdir}/%{name}

%changelog
* Wed Apr 18 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.2.4-3
- Remove eclipse plugin from BuildRequires

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Dec  5 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.2.4-1
- Update to latest upstream version

* Mon Jul 4 2011 Alexander Kurtakov <akurtako@redhat.com> 3.2.3-4
- Fix FTBFS.
- Adapt to current guidelines.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 17 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.2.3-2
- Use maven 3 to build
- Drop ant-contrib depmap (no longer needed)

* Thu Jan 13 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.2.3-1
- Initial version of the package
