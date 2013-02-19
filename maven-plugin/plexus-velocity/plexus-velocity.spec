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

%define parent plexus
%define subname velocity

Name:           plexus-velocity
Version:        1.1.8
Release:        11%{?dist}
Epoch:          0
Summary:        Plexus Velocity Component
License:        ASL 2.0
Group:          Development/Java
URL:            http://plexus.codehaus.org/
# svn export http://svn.codehaus.org/plexus/plexus-components/tags/plexus-velocity-1.1.8/
# tar czf plexus-velocity-1.1.8-src.tar.gz plexus-velocity-1.1.8/
Source0:        plexus-velocity-%{version}-src.tar.gz
Source1:        http://www.apache.org/licenses/LICENSE-2.0.txt

BuildArch:      noarch
BuildRequires:  jpackage-utils >= 0:1.7.2
BuildRequires:  ant >= 0:1.6
BuildRequires:  java-devel >= 1:1.6.0
BuildRequires:  maven
BuildRequires:  maven-compiler-plugin
BuildRequires:  maven-install-plugin
BuildRequires:  maven-jar-plugin
BuildRequires:  maven-javadoc-plugin
BuildRequires:  maven-resources-plugin
BuildRequires:  maven-surefire-plugin
BuildRequires:  maven-surefire-provider-junit
BuildRequires:  maven-doxia-sitetools
BuildRequires:  ant-contrib
BuildRequires:  classworlds >= 0:1.1
BuildRequires:  apache-commons-collections
BuildRequires:  plexus-container-default
BuildRequires:  plexus-utils
BuildRequires:  velocity
Requires:  classworlds >= 0:1.1
Requires:  apache-commons-collections
Requires:  plexus-container-default
Requires:  plexus-utils
Requires:  velocity

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

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -n plexus-velocity-%{version}
cp -p %{SOURCE1} LICENSE
for j in $(find . -name "*.jar"); do
        mv $j $j.no
done

%build
    # Use normal pom for now
    rm -f release-pom.xml
    mvn-rpmbuild \
        -e \
        install javadoc:aggregate

%install
# jars
install -Dpm 644 target/%{name}-%{version}.jar \
   %{buildroot}/%{_javadir}/%{parent}/%{subname}.jar

# poms
install -Dpm 644 pom.xml %{buildroot}/%{_mavenpomdir}/JPP.%{name}.pom
%add_maven_depmap JPP.%{name}.pom %{parent}/%{subname}.jar

# javadoc
install -d -m 755 %{buildroot}/%{_javadocdir}/%{name}
cp -pr target/site/apidocs/* %{buildroot}/%{_javadocdir}/%{name}

%files
%doc LICENSE
%{_javadir}/%{parent}/*
%{_mavendepmapfragdir}/*
%{_mavenpomdir}/*

%files javadoc
%doc LICENSE
%doc %{_javadocdir}/*

%changelog
* Wed Nov 21 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.1.8-11
- Install LICENSE file
- Resolves: rhbz#878833

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.1.8-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.1.8-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Sep 7 2011 Alexander Kurtakov <akurtako@redhat.com> 0:1.1.8-8
- Drop ant build.
- Further cleanups.

* Thu Jul 28 2011 Jaromir Capik <jcapik@redhat.com> - 0:1.1.8-7
- Migration to maven3
- Removal of plexus-maven-plugin (not needed)
- Minor spec file changes according to the latest guidelines

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.1.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 22 2009 Alexander Kurtakov <akurtako@redhat.com> 0:1.1.8-5
- BR java-devel 1.6.

* Tue Dec 22 2009 Alexander Kurtakov <akurtako@redhat.com> 0:1.1.8-4
- BR maven-surefire-provider-junit.

* Tue Dec 22 2009 Alexander Kurtakov <akurtako@redhat.com> 0:1.1.8-3
- BR maven-doxia-sitetools.

* Tue Dec 22 2009 Alexander Kurtakov <akurtako@redhat.com> 0:1.1.8-2
- BR plexus-maven-plugin.

* Tue Dec 22 2009 Alexander Kurtakov <akurtako@redhat.com> 0:1.1.8-1
- Update to upstream 1.1.8.

* Fri Aug 21 2009 Andrew Overholt <overholt@redhat.com> 1.1.7-3.3
- Add ant-nodeps BR

* Fri Aug 21 2009 Andrew Overholt <overholt@redhat.com> 1.1.7-3.2
- Add ant-contrib BR

* Fri Aug 21 2009 Andrew Overholt <overholt@redhat.com> 0:1.1.7-3.1
- Import from Deepak Bhole's work (import from JPackage, update to 1.1.7)
- Remove gcj support

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.1.2-5.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.1.2-4.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:1.1.2-3.2
- drop repotag

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0:1.1.2-3jpp.1
- Autorebuild for GCC 4.3

* Sat Mar 24 2007 Ralph Apel <r.apel at r-apel.de> - 0:1.1.2-3jpp
- Build with maven2 by default
- Add gcj_support options

* Fri Feb 16 2007 Tania Bento <tbento@redhat.com> - 0:1.1.2-2jpp.1
- Fixed %%License.
- Fixed %%BuildRoot.
- Fixed %%Release.
- Removed the %%post and %%postun for javadoc.
- Removed %%Vendor.
- Removed %%Distribution.
- Removed "%%define section free".
- Added the gcj support option.
- Added BR for jakarta-commons-logging.

* Wed May 17 2006 Ralph Apel <r.apel at r-apel.de> - 0:1.1.2-2jpp
- First JPP-1.7 release

* Mon Nov 07 2005 Ralph Apel <r.apel at r-apel.de> - 0:1.1.2-1jpp
- First JPackage build
