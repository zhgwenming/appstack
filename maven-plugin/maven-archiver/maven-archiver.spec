# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

Name:           maven-archiver
Version:        2.5
Release:        3%{?dist}
Epoch:          0
Summary:        Maven Archiver
License:        ASL 2.0
Group:          Development/Libraries
URL:            http://maven.apache.org/shared/maven-archiver/

Source0:        http://repo1.maven.org/maven2/org/apache/maven/%{name}/%{version}/%{name}-%{version}-source-release.zip

Patch0:         %{name}-maven-core-dep.patch

BuildArch:      noarch

BuildRequires:  java-devel >= 1:1.6.0
BuildRequires:  jpackage-utils >= 0:1.7.2
BuildRequires:  maven
BuildRequires:  maven-compiler-plugin
BuildRequires:  maven-install-plugin
BuildRequires:  maven-jar-plugin
BuildRequires:  maven-javadoc-plugin
BuildRequires:  maven-resources-plugin
BuildRequires:  maven-site-plugin
BuildRequires:  maven-surefire-plugin
BuildRequires:  maven-surefire-provider-junit
BuildRequires:  maven-doxia-sitetools
BuildRequires:  maven-shared-jar
BuildRequires:  plexus-interpolation
BuildRequires:  plexus-archiver >= 2.1-1
BuildRequires:  plexus-utils
BuildRequires:  apache-commons-parent

Requires:       maven
Requires:       plexus-archiver >= 2.1-1
Requires:       plexus-interpolation
Requires:       plexus-utils

Provides: maven-shared-archiver = %{version}-%{release}
Obsoletes: maven-shared-archiver < %{version}-%{release}

%description
The Maven Archiver is used by other Maven plugins
to handle packaging

%package javadoc
Summary:        Javadoc for %{name}
Group:          Documentation
Requires:       jpackage-utils

%description javadoc
Javadoc for %{name}.

%prep
%setup -q
%patch0 -p1

#tests don't compile with maven 2.2.1
rm -fr src/test/java/org/apache/maven/archiver/*.java

%build
mvn-rpmbuild -Dproject.build.sourceEncoding=UTF-8 install javadoc:aggregate


%install
# jars/poms
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}

# Copy file and create unversioned symlink
install -pm 644 target/%{name}-%{version}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

# Copy pom
install -dm 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -pm 644 pom.xml $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}.pom
%add_maven_depmap JPP-%{name}.pom %{name}.jar

# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -pr target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

%files
%{_javadir}/*
%{_mavenpomdir}/JPP-%{name}.pom
%{_mavendepmapfragdir}/%{name}

%files javadoc
%doc %{_javadocdir}/*

%changelog
* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Feb 16 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:2.5-2
- Add versioned BR/R on plexus-archiver and rebuild

* Wed Feb 15 2012 Alexander Kurtakov <akurtako@redhat.com> 0:2.5-1
- Update to latest upstream release.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Nov 6 2011 Alexander Kurtakov <akurtako@redhat.com> 0:2.4.2-1
- Update to 2.4.2 upstream release.

* Mon Sep 19 2011 Tomas Radej <tradej@redhat.com> - 0:2.4.1-7
- Fixed dep on maven-core artifact
- Minor fixes

* Wed Jun 8 2011 Alexander Kurtakov <akurtako@redhat.com> 0:2.4.1-6
- Build with maven 3.x.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov 8 2010 Alexander Kurtakov <akurtako@redhat.com> 0:2.4.1-4
- Add missing BR.

* Mon Nov 8 2010 Alexander Kurtakov <akurtako@redhat.com> 0:2.4.1-3
- Remove tests as they don't compile.

* Mon May 31 2010 Alexander Kurtakov <akurtako@redhat.com> 0:2.4.1-2
- BR java-devel >= 1:1.6.0.

* Sat May 29 2010 Alexander Kurtakov <akurtako@redhat.com> 0:2.4.1-1
- Update to 2.4.1.

* Wed Dec 23 2009 Alexander Kurtakov <akurtako@redhat.com> 0:2.4-1
- Update to 2.4.

* Mon Dec 21 2009 Alexander Kurtakov <akurtako@redhat.com> 0:2.2-3
- BR maven-surefire-provider-junit.

* Mon Aug 31 2009 Alexander Kurtakov <akurtako@redhat.com> 0:2.2-2
- Fix line length.
- Own only specific fragment and pom.

* Wed May 20 2009 Fernando Nasser <fnasser@redhat.com> 0:2.2-1
- Fix license
- Update instructions to obtain sources
- Refresh source tar ball

* Thu Jul 26 2007 Deepak Bhole <dbhole@redhat.com> 0:2.2-0jpp.1
- Initial build
