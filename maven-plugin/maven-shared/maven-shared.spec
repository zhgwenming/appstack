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

%global shared_components_version 15
%global file_management_version 1.2.2

%global dependency_analyzer_version 1.2
%global downloader_version 1.2

%global invoker_version 2.0.12
%global osgi_version 0.3.0
%global plugin_testing_harness_version 1.2

#this model is not included in parent pom
%global reporting_api_version 3.0

%global reporting_impl_version 2.1
%global repository_builder_version 1.0

%global io_version 1.2
%global jar_version 1.1
%global monitor_version 1.0
### disabled by pom.xml default
#%global script_ant_version 2.1
#%global script_beanshell_version 2.1
#%global test_tools_version 1.0
#%global toolchain_version 1.0
%global verifier_version 1.3

Summary:        Maven Shared Components
URL:            http://maven.apache.org/shared/
Name:           maven-shared
Version:        15
Release:        28%{?dist}
License:        ASL 2.0
Group:          Development/Libraries

# svn export \
# http://svn.apache.org/repos/asf/maven/shared/tags/maven-shared-components-15/
# tar czf maven-shared-components-15.tar.gz maven-shared-components-15
Source0:        maven-shared-components-%{version}.tar.gz
Source1:        %{name}-jpp-depmap.xml

BuildRequires:  ant
BuildRequires:  aqute-bnd
BuildRequires:  easymock2
BuildRequires:  jpackage-utils >= 0:1.7.2
BuildRequires:  junit
BuildRequires:  maven
BuildRequires:  maven-artifact-manager
BuildRequires:  maven-compiler-plugin
BuildRequires:  maven-doxia
BuildRequires:  maven-doxia-sitetools
BuildRequires:  maven-doxia-tools
BuildRequires:  maven-install-plugin
BuildRequires:  maven-jar-plugin
BuildRequires:  maven-javadoc-plugin
BuildRequires:  maven-javadoc-plugin
BuildRequires:  maven-model
BuildRequires:  maven-monitor
BuildRequires:  maven-plugin-cobertura
BuildRequires:  maven-plugin-testing-tools
BuildRequires:  maven-profile
BuildRequires:  maven-project
BuildRequires:  maven-resources-plugin
BuildRequires:  maven-shared-file-management
BuildRequires:  maven-shared-reporting-impl
BuildRequires:  maven-site-plugin
BuildRequires:  maven-source-plugin
BuildRequires:  maven-surefire-plugin
BuildRequires:  maven-surefire-report-plugin
BuildRequires:  maven-test-tools
BuildRequires:  maven-wagon
BuildRequires:  modello
BuildRequires:  objectweb-asm
BuildRequires:  plexus-component-api
BuildRequires:  plexus-containers-component-metadata
BuildRequires:  plexus-digest
BuildRequires:  plexus-utils


Requires:       ant
Requires:       aqute-bnd
Requires:       jpackage-utils
Requires:       maven
Requires:       maven-wagon
Requires:       objectweb-asm
Requires:       plexus-digest
Requires:       plexus-utils
Requires:       plexus-utils

BuildArch:      noarch

# Obsoleting retired subpackages
Obsoletes:      maven-shared-ant < 1.0-27
Obsoletes:      maven-shared-model-converter < 2.3-27
Obsoletes:      maven-shared-ruhntime < 1.0-27

%description
Maven Shared Components

%package file-management
Summary:        Maven Shared File Management API
Group:          Development/Libraries
Version:        %{file_management_version}
Requires:  %{name} = 0:%{shared_components_version}-%{release}
Requires:  %{name}-io >= 0:%{io_version}
Requires:  maven
Requires:  plexus-containers-container-default
Requires:  plexus-utils

%description file-management
API to collect files from a given directory using
several include/exclude rules.

%package osgi
Summary:        Maven OSGi
Group:          Development/Libraries
Version:        %{osgi_version}
Requires:  %{name} = 0:%{shared_components_version}-%{release}
Requires:  aqute-bnd
Requires:  maven-project

%description osgi
Library for Maven-OSGi integration

%package downloader
Summary:        Maven Downloader
Group:          Development/Libraries
Version:        %{downloader_version}
Requires:  %{name} = 0:%{shared_components_version}-%{release}
Requires:  maven
Requires:  maven-artifact-manager

%description downloader
Provide a super simple interface for downloading a
single artifact.

%package dependency-analyzer
Summary:        Maven Dependency Analyzer
Group:          Development/Libraries
Version:        %{dependency_analyzer_version}
Requires:  %{name} = 0:%{shared_components_version}-%{release}
Requires:  maven
Requires:  maven-project
Requires:  objectweb-asm
Requires:  plexus-utils

%description dependency-analyzer
%{summary}.

%package invoker
Summary:        Maven Process Invoker
Group:          Development/Libraries
Version:        %{invoker_version}
Requires:  %{name} = 0:%{shared_components_version}-%{release}
Requires:  %{name}-monitor >= 0:%{monitor_version}-%{release}
Requires:  maven
Requires:  plexus-utils

%description invoker
%{summary}.

%package reporting-impl
Summary:        Maven Reporting Implementation
Group:          Development/Libraries
Version:        %{reporting_impl_version}
Requires:  %{name} = 0:%{shared_components_version}-%{release}
Requires:  apache-commons-validator
Requires:  jakarta-oro
Requires:  maven
Requires:  maven-project
Requires:  maven-doxia
Requires:  apache-commons-validator
Requires:  plexus-utils

%description reporting-impl
%{summary}.

%package repository-builder
Summary:        Maven Repository Builder
Group:          Development/Libraries
Version:        %{repository_builder_version}
Requires:  %{name} = 0:%{shared_components_version}-%{release}
Requires:  %{name}-common-artifact-filters >= 0:%{common_artifact_filters_version}-%{release}
Requires:  maven
Requires:  maven-artifact-manager
Requires:  maven-project

%description repository-builder
%{summary}.

%package io
Summary:        Maven Shared I/O API
Group:          Development/Libraries
Version:        %{io_version}
Requires:  %{name} = 0:%{shared_components_version}-%{release}
Requires:  maven
Requires:  maven-artifact-manager
Requires:  maven-wagon
Requires:  plexus-utils
Requires:  plexus-containers-container-default

%description io
%{summary}.

%package jar
Summary:        Maven Shared Jar
Group:          Development/Libraries
Version:        %{jar_version}
Requires:  %{name} = 0:%{shared_components_version}-%{release}
Requires:  maven
Requires:  plexus-digest
Requires:  bcel
Requires:  apache-commons-collections

%description jar
Utilities that help identify the contents of a JAR,
including Java class analysis and Maven metadata
analysis.

%package monitor
Summary:        Maven Shared Monitor API
Group:          Development/Libraries
Version:        %{monitor_version}
Requires:  %{name} = 0:%{shared_components_version}-%{release}
Requires:  maven
Requires:  plexus-containers-container-default

%description monitor
%{summary}.

%package verifier
Summary:        Maven Verifier Component
Group:          Development/Libraries
Version:        %{verifier_version}
License:        ASL 2.0 and BSD and MIT
Requires:  %{name} = 0:%{shared_components_version}-%{release}
Requires:  junit

%description verifier
%{summary}.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Documentation
Requires:       jpackage-utils
Provides:       %{name}-file-management-javadoc = %{epoch}:%{file_management_version}-%{release}
Obsoletes:      %{name}-file-management-javadoc < %{epoch}:%{file_management_version}-%{release}
Provides:       %{name}-plugin-testing-harness-javadoc = %{epoch}:%{plugin_testing_harness_version}-%{release}
Obsoletes:      %{name}-plugin-testing-harness-javadoc < %{epoch}:%{plugin_testing_harness_version}-%{release}

%description javadoc
%{summary}.

%package reporting-api
Summary:        Maven Reporting API
Group:          Development/Libraries
Version:        %{reporting_api_version}
Requires:  %{name} = 0:%{shared_components_version}-%{release}
Requires:  ant
Requires:  maven
Requires:  maven-doxia

%description reporting-api
Maven Reporting API.


%prep
%setup -q -n %{name}-components-%{shared_components_version}
chmod -R go=u-w *

# Disable plugins that are not needed or are packaged separately
%pom_disable_module maven-ant
%pom_disable_module maven-archiver
%pom_disable_module maven-artifact-resolver
%pom_disable_module maven-dependency-tree
%pom_disable_module maven-doxia-tools
%pom_disable_module maven-filtering
%pom_disable_module maven-model-converter
%pom_disable_module maven-runtime

# Adding maven-reporting-api because otherwise it wouldn't build
%pom_xpath_inject pom:modules '<module>maven-reporting-api</module>'

# Adding missing dependencies to poms
%pom_add_dep org.apache.maven:maven-core:3.0.3              maven-downloader/pom.xml
%pom_add_dep org.apache.maven:maven-compat:3.0.3            maven-downloader/pom.xml
%pom_add_dep org.apache.maven:maven-compat:3.0.3            maven-repository-builder/pom.xml
%pom_add_dep org.apache.maven:maven-compat:3.0.3            maven-shared-io/pom.xml
%pom_add_dep org.codehaus.plexus:plexus-container-default   maven-shared-jar/pom.xml

# Replace plexus-maven-plugin with plexus-component-metadata
find -name 'pom.xml' -exec sed \
    -i 's/<artifactId>plexus-maven-plugin<\/artifactId>/<artifactId>plexus-component-metadata<\/artifactId>/' '{}' ';'
find -name 'pom.xml' -exec sed \
    -i 's/<goal>descriptor<\/goal>/<goal>generate-metadata<\/goal>/' '{}' ';'

# Fix aqute-bnd dependency
sed -i "s|<artifactId>bndlib|<artifactId>bnd|g" maven-osgi/pom.xml

# need namespace for new version modello
sed -i "s|<model>|<model xmlns=\"http://modello.codehaus.org/MODELLO/1.3.0\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xsi:schemaLocation=\"http://modello.codehaus.org/MODELLO/1.3.0 http://modello.codehaus.org/xsd/modello-1.3.0.xsd\" xml.namespace=\"..\" xml.schemaLocation=\"..\" xsd.namespace=\"..\" xsd.targetNamespace=\"..\">|" file-management/src/main/mdo/fileset.mdo

sed -i "s|<groupId>ant|<groupId>org.apache.ant|g" maven-ant/pom.xml
# Remove test that needs junit-addons until that makes it into Fedora
rm -f maven-reporting-impl/src/test/java/org/apache/maven/reporting/AbstractMavenReportRendererTest.java

# Remove tests that need jmock (for now)
rm -f maven-dependency-analyzer/src/test/java/org/apache/maven/shared/dependency/analyzer/InputStreamConstraint.java
rm -f maven-dependency-analyzer/src/test/java/org/apache/maven/shared/dependency/analyzer/ClassFileVisitorUtilsTest.java
rm -f maven-dependency-analyzer/src/test/java/org/apache/maven/shared/dependency/analyzer/AbstractFileTest.java

%build
export MAVEN_OPTS="-XX:MaxPermSize=256m"
mvn-rpmbuild \
        -Dmaven.local.depmap.file=%{SOURCE1} \
        -Dmaven.test.skip=true \
        install javadoc:aggregate

%install

# main package infrastructure
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}/maven-shared
install -d -m 755 $RPM_BUILD_ROOT/%{_mavenpomdir}

# poms and jars
install -pm 644 pom.xml $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP.maven-shared-components-parent.pom
%add_maven_depmap JPP.%{name}-components-parent.pom

install -pm 644 maven-downloader/pom.xml $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP.maven-shared-downloader.pom
install -p -m 0644 maven-downloader/target/maven-downloader-%{downloader_version}-SNAPSHOT.jar \
        $RPM_BUILD_ROOT%{_javadir}/maven-shared/downloader.jar
%add_maven_depmap -f downloader JPP.%{name}-downloader.pom %{name}/downloader.jar

install -pm 644 maven-dependency-analyzer/pom.xml $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP.maven-shared-dependency-analyzer.pom
install -p -m 0644 maven-dependency-analyzer/target/maven-dependency-analyzer-%{dependency_analyzer_version}-SNAPSHOT.jar \
        $RPM_BUILD_ROOT%{_javadir}/maven-shared/dependency-analyzer.jar
%add_maven_depmap -f dependency-analyzer JPP.%{name}-dependency-analyzer.pom %{name}/dependency-analyzer.jar

install -pm 644 maven-verifier/pom.xml $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP.maven-shared-verifier.pom
install -p -m 0644 maven-verifier/target/maven-verifier-%{verifier_version}-SNAPSHOT.jar \
        $RPM_BUILD_ROOT%{_javadir}/maven-shared/verifier.jar
%add_maven_depmap -f verifier JPP.%{name}-verifier.pom %{name}/verifier.jar

install -pm 644 maven-shared-monitor/pom.xml $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP.maven-shared-monitor.pom
install -p -m 0644 maven-shared-monitor/target/maven-shared-monitor-%{monitor_version}-SNAPSHOT.jar \
        $RPM_BUILD_ROOT%{_javadir}/maven-shared/monitor.jar
%add_maven_depmap -f monitor JPP.%{name}-monitor.pom %{name}/monitor.jar

install -pm 644 maven-shared-io/pom.xml $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP.maven-shared-io.pom
install -p -m 0644 maven-shared-io/target/maven-shared-io-%{io_version}-SNAPSHOT.jar \
        $RPM_BUILD_ROOT%{_javadir}/maven-shared/io.jar
%add_maven_depmap -f io JPP.%{name}-io.pom %{name}/io.jar

install -pm 644 maven-shared-jar/pom.xml $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP.maven-shared-jar.pom
install -p -m 0644 maven-shared-jar/target/maven-shared-jar-%{jar_version}-SNAPSHOT.jar \
        $RPM_BUILD_ROOT%{_javadir}/maven-shared/jar.jar
%add_maven_depmap -f jar JPP.%{name}-jar.pom %{name}/jar.jar

install -pm 644 maven-repository-builder/pom.xml $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP.maven-shared-repository-builder.pom
install -p -m 0644 maven-repository-builder/target/maven-repository-builder-%{repository_builder_version}-alpha-3-SNAPSHOT.jar \
        $RPM_BUILD_ROOT%{_javadir}/maven-shared/repository-builder.jar
%add_maven_depmap -f repository-builder JPP.%{name}-repository-builder.pom %{name}/repository-builder.jar

install -pm 644 maven-reporting-impl/pom.xml $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP.maven-shared-reporting-impl.pom
install -p -m 0644 maven-reporting-impl/target/maven-reporting-impl-%{reporting_impl_version}-SNAPSHOT.jar \
        $RPM_BUILD_ROOT%{_javadir}/maven-shared/reporting-impl.jar
%add_maven_depmap -f reporting-impl JPP.%{name}-reporting-impl.pom %{name}/reporting-impl.jar

install -pm 644 maven-invoker/pom.xml $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP.maven-shared-invoker.pom
install -p -m 0644 maven-invoker/target/maven-invoker-%{invoker_version}-SNAPSHOT.jar \
        $RPM_BUILD_ROOT%{_javadir}/maven-shared/invoker.jar
%add_maven_depmap -f invoker JPP.%{name}-invoker.pom %{name}/invoker.jar

install -pm 644 maven-osgi/pom.xml $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP.maven-shared-osgi.pom
install -p -m 0644 maven-osgi/target/maven-osgi-%{osgi_version}-SNAPSHOT.jar \
        $RPM_BUILD_ROOT%{_javadir}/maven-shared/osgi.jar
%add_maven_depmap -f osgi JPP.%{name}-osgi.pom %{name}/osgi.jar

install -pm 644 file-management/pom.xml $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP.maven-shared-file-management.pom
install -p -m 0644 file-management/target/file-management-%{file_management_version}-SNAPSHOT.jar \
        $RPM_BUILD_ROOT%{_javadir}/maven-shared/file-management.jar
%add_maven_depmap -f file-management JPP.%{name}-file-management.pom %{name}/file-management.jar

install -pm 644 maven-reporting-api/pom.xml $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP.maven-shared-reporting-api.pom
install -p -m 0644 maven-reporting-api/target/maven-reporting-api-%{reporting_api_version}-SNAPSHOT.jar \
        $RPM_BUILD_ROOT%{_javadir}/maven-shared/reporting-api.jar
%add_maven_depmap -f reporting-api -a "org.apache.maven.reporting:maven-reporting-api" JPP.%{name}-reporting-api.pom %{name}/reporting-api.jar

# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -pr target/site/apidocs/* \
         $RPM_BUILD_ROOT%{_javadocdir}/%{name}

%pre javadoc
# workaround for rpm bug, can be removed in F-18
[ $1 -gt 1 ] && [ -L %{_javadocdir}/%{name} ] && \
rm -rf $(readlink -f %{_javadocdir}/%{name}) %{_javadocdir}/%{name} || :

%files
%doc LICENSE.txt NOTICE.txt
%dir %{_javadir}/%{name}
%{_mavenpomdir}/JPP.%{name}-components-parent.pom
%{_mavendepmapfragdir}/%{name}

%files file-management
%{_javadir}/%{name}/file-management.jar
%{_mavenpomdir}/JPP.%{name}-file-management.pom
%{_mavendepmapfragdir}/%{name}-file-management

%files osgi
%{_javadir}/%{name}/osgi.jar
%{_mavenpomdir}/JPP.%{name}-osgi.pom
%{_mavendepmapfragdir}/%{name}-osgi

%files dependency-analyzer
%{_javadir}/%{name}/dependency-analyzer.jar
%{_mavenpomdir}/JPP.%{name}-dependency-analyzer.pom
%{_mavendepmapfragdir}/%{name}-dependency-analyzer

%files downloader
%{_javadir}/%{name}/downloader.jar
%{_mavenpomdir}/JPP.%{name}-downloader.pom
%{_mavendepmapfragdir}/%{name}-downloader

%files invoker
%{_javadir}/%{name}/invoker.jar
%{_mavenpomdir}/JPP.%{name}-invoker.pom
%{_mavendepmapfragdir}/%{name}-invoker

%files reporting-impl
%{_javadir}/%{name}/reporting-impl.jar
%{_mavenpomdir}/JPP.%{name}-reporting-impl.pom
%{_mavendepmapfragdir}/%{name}-reporting-impl

%files repository-builder
%{_javadir}/%{name}/repository-builder.jar
%{_mavenpomdir}/JPP.%{name}-repository-builder.pom
%{_mavendepmapfragdir}/%{name}-repository-builder

%files io
%{_javadir}/%{name}/io.jar
%{_mavenpomdir}/JPP.%{name}-io.pom
%{_mavendepmapfragdir}/%{name}-io

%files jar
%{_javadir}/%{name}/jar.jar
%{_mavenpomdir}/JPP.%{name}-jar.pom
%{_mavendepmapfragdir}/%{name}-jar

%files monitor
%{_javadir}/%{name}/monitor.jar
%{_mavenpomdir}/JPP.%{name}-monitor.pom
%{_mavendepmapfragdir}/%{name}-monitor

%files verifier
%{_javadir}/%{name}/verifier.jar
%{_mavenpomdir}/JPP.%{name}-verifier.pom
%{_mavendepmapfragdir}/%{name}-verifier

%files reporting-api
%{_javadir}/%{name}/reporting-api.jar
%{_mavenpomdir}/JPP.%{name}-reporting-api.pom
%{_mavendepmapfragdir}/%{name}-reporting-api

%files javadoc
%doc LICENSE.txt NOTICE.txt
%{_javadocdir}/%{name}

%changelog
* Wed Dec 19 2012 Tomas Radej <tradej@redhat.com> - 15-28
- Obsoleted retired packages
- Sorted (B)Rs, added R on jpackage-utils

* Fri Nov 30 2012 Tomas Radej <tradej@redhat.com> - 15-27
- Removed ant, artifact-resolver, common-artifact-filters, dependency-tree, model-converter, runtime
- Replaced patches with pom macros

* Thu Nov 22 2012 Jaromir Capik <jcapik@redhat.com> - 15-26
- Migration to plexus-containers-container-default

* Mon Nov 19 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 15-25
- Fix verifier License tag
- Install licelse files

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 15-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Feb 29 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> 15-23
- Remove exact version dependency on artifact-filters
- Fix missing plexus-container-default in pom for shared-jar

* Sat Jan 14 2012 Ville Skyttä <ville.skytta@iki.fi> - 15-22
- Require apache-commons-validator instead of jakarta-* in reporting-impl.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 15-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Nov 27 2011 Ville Skyttä <ville.skytta@iki.fi> - 15-20
- Fix plugin-testing-harness dependency/obsoletes/provides versions.

* Wed Oct 12 2011 Jaromir Capik <jcapik@redhat.com> - 15-19
- aqute-bndlib renamed to aqute-bnd (fixing name conflict)

* Wed Aug 31 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 15-18
- Remove filtering subpackage (separate package now)

* Mon Aug 22 2011 Jaromir Capik <jcapik@redhat.com> - 15-17
- Migration from plexus-maven-plugin to plexus-containers-component-metadata
- Minor spec file changes according to the latest guidelines

* Thu Jun 23 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 15-16
- Add second groupId for reporting-api to add compatibility
- Versionless javadocs and remove defattr macros (not needed anymore)
- Use new maven2 compatibility packages
- Remove old patches

* Fri Jun 3 2011 Alexander Kurtakov <akurtako@redhat.com> 15-15
- Require maven not maven2 now.
- Adapt to current guidelines.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 15-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 17 2010 Alexander Kurtakov <akurtako@redhat.com> 15-13
- Drop versioned jars.
- Drop tomcat5 deps.

* Thu Sep 16 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 15-12
- Use %%global instead of %%define
- Use %%{_mavenpomdir}
- Remove plexus-registry from BR/R

* Tue Jun 01 2010 Yong Yang <yyang@redhat.com> 15-11
- Rebuld with maven221
- Add patches
- Use javadoc:aggregate

* Tue Jun 01 2010 Yong Yang <yyang@redhat.com> 15-10
- Fix installed jar name of artifact-resolver, filtering, reporting-api, runtime

* Mon May 31 2010 Alexander Kurtakov <akurtako@redhat.com> 15-9
- Reenable reporting api.
- Fix groups.
- Do not remove tests that run now.

* Mon May 31 2010 Alexander Kurtakov <akurtako@redhat.com> 15-8
- Fix maven-archiver depmap.

* Mon May 31 2010 Alexander Kurtakov <akurtako@redhat.com> 15-7
- Release should be bigger than version 8 release.

* Thu May 21 2010 Yong Yang <yyang@redhat.com> 15-1
- Upgrade to 15

* Thu May 20 2010 Yong Yang <yyang@redhat.com> 8-6
- Properly comment %%add_maven_depmap

* Thu May 20 2010 Yong Yang <yyang@redhat.com> 8-5
- Remove plugin-tools* and pluging-testing*
- Add BRs:  objectweb-asm, plexus-digest

* Thu Nov 26 2009 Lubomir Rintel <lkundrak@v3.sk> 8-4
- Fix build

* Tue Sep 01 2009 Andrew Overholt <overholt@redhat.com> 8-3
- Add tomcat5, easymock, and maven2-plugin-source BRs

* Tue Sep 01 2009 Andrew Overholt <overholt@redhat.com> 8-2
- Add tomcat5-servlet-2.4-api BR

* Mon Aug 31 2009 Andrew Overholt <overholt@redhat.com> 8-1
- Update to version 8 (courtesy Deepak Bhole)

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.0-4.6
- drop repotag

* Thu May 29 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.0-4jpp.5
- fix license tag

* Thu Feb 28 2008 Deepak Bhole <dbhole@redhat.com> 1.0-4jpp.4
- Rebuild

* Fri Sep 21 2007 Deepak Bhole <dbhole@redhat.com> 0:1.0-4jpp.3
- Rebuild with ppc64 excludearch'd
- Removed 'jpp' from a BR version

* Tue Mar 20 2007 Deepak Bhole <dbhole@redhat.com> 0:1.0-4jpp.2
- Fixed BRs and Reqa

* Tue Feb 27 2007 Tania Bento <tbento@redhat.com> 0:1.0-4jpp.1
- Fixed %%Release.
- Fixed %%BuildRoot.
- Removed %%Vendor.
- Removed %%Distribution.
- Removed %%post and %%postun sections for file-management-javadoc.
- Removed %%post and %%postun sections for plugin-testing-harness-javadoc.
- Defined _with_gcj_support and gcj_support.
- Fixed %%License.
- Fixed %%Group.
- Marked config file with %%config(noreplace) in %%files section.
- Fixed instructions on how to generate source drop.

* Fri Oct 27 2006 Deepak Bhole <dbhole@redhat.com> 1.0-4jpp
- Update for maven 9jpp

* Fri Sep 15 2006 Deepak Bhole <dbhole@redhat.com> 1.0-3jpp
- Removed the file-management-pom.patch (no longer required)
- Install poms

* Wed Sep 13 2006 Ralph Apel <r.apel@r-apel.de> 0:1.0-2jpp
- Add plugin-testing-harness subpackage

* Mon Sep 11 2006 Ralph Apel <r.apel@r-apel.de> 0:1.0-1jpp
- First release
- Add gcj_support option
- Add post/postun Requires for javadoc
