# Copyright (c) 2000-2007, JPackage Project
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

%global parent plexus
%global subname cli

Name:           %{parent}-%{subname}
Version:        1.2
Release:        13%{?dist}
Epoch:          0
Summary:        Command Line Interface facilitator for Plexus
License:        ASL 2.0
Group:          Development/Libraries
URL:            http://plexus.codehaus.org/
# svn export http://svn.codehaus.org/plexus/archive/plexus-tools/tags/plexus-cli-1.2
# tar czf plexus-cli-%{version}-src.tar.gz plexus-cli-%{version}
# Note: Exported revision 8188.
Source0:        %{name}-%{version}-src.tar.gz

# License headers missing from some files
# http://jira.codehaus.org/browse/PLX-418
Patch0:         plexus-cli-licenseheaders.patch

BuildArch:      noarch

BuildRequires:  jpackage-utils >= 0:1.7.3
BuildRequires:  junit
BuildRequires:  maven
BuildRequires:  maven-compiler-plugin
BuildRequires:  maven-install-plugin
BuildRequires:  maven-jar-plugin
BuildRequires:  maven-javadoc-plugin
BuildRequires:  maven-resources-plugin
BuildRequires:  maven-surefire-plugin
BuildRequires:  maven-surefire-provider-junit 
BuildRequires:  maven-doxia
BuildRequires:  maven-doxia-sitetools
BuildRequires:  maven-release
BuildRequires:  plexus-classworlds
BuildRequires:  plexus-containers-container-default
BuildRequires:  plexus-utils 
BuildRequires:  apache-commons-cli

Requires:  plexus-classworlds
Requires:  plexus-containers-container-default
Requires:  plexus-utils 

%description
The Plexus project seeks to create end-to-end developer tools for
writing applications. At the core is the container, which can be
embedded or for a full scale application server. There are many
reusable components for hibernate, form processing, jndi, i18n,
velocity, etc. Plexus also includes an application server which
is like a J2EE application server, without all the baggage.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Documentation
Requires:       jpackage-utils

%description javadoc
Javadoc for %{name}.

%prep
%setup -q
find . -name "*.jar" -exec rm -f {} \;

%patch0 -p3

%build
mvn-rpmbuild install javadoc:javadoc

%install
# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}/plexus
install -pm 644 target/%{name}-%{version}.jar \
  $RPM_BUILD_ROOT%{_javadir}/plexus/%{subname}.jar

# pom
install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -pm 644 pom.xml $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{parent}-%{subname}.pom

%add_maven_depmap JPP.%{parent}-%{subname}.pom plexus/%{subname}.jar

# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -pr target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

%files -f .mfiles

%files javadoc
%doc %{_javadocdir}/*


%changelog
* Fri Nov 16 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.2-13
- Fix license tag to be ASL 2.0 (no plexus licensing anywhere)
- Update to new guidelines

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jun 12 2011 Alexander Kurtakov <akurtako@redhat.com> 0:1.2-10
- Build with maven 3.x

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Aug 21 2009 Andrew Overholt <overholt@redhat.com> 0:1.2-8
- Add jakarta-commons-cli BR

* Thu Aug 20 2009 Andrew Overholt <overholt@redhat.com> 0:1.2-7
- Remove gcj support
- Default to building with ant
- Add patch to include fixed file headers
  (http://jira.codehaus.org/browse/PLX-418)

* Sun May 17 2009 Fernando Nasser <fnasser@redhat.com> 0:1.2-6
- Fix license and source URL

* Tue Apr 30 2009 Yong Yang <yyang@redhat.com> 0:1.2-5
- Add BRs maven-doxia*
- Rebuild with new maven2 2.0.8 built in non-bootstrap mode

* Tue Mar 17 2009 Yong Yang <yyang@redhat.com> 0:1.2-4
- rebuild with new maven2 2.0.8 built in bootstrap mode

* Thu Feb 05 2009 Yong Yang <yyang@redhat.com> 0:1.2-3
- fix release tag

* Wed Jan 14 2009 Yong Yang <yyang@redhat.com> 0:1.2-2jpp.2
-re-build with gcj

* Wed Jan 14 2009 Yong Yang <yyang@redhat.com> 0:1.2-2jpp.1
- Import from maven 2.0.8 packages, initial bulding

* Wed Jan 30 2008 Deepak Bhole <dbhole@redhat.com> 0:1.2-1jpp.1
- Initial build with merge from JPackage
