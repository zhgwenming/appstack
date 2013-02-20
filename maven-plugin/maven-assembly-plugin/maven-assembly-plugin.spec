Name:           maven-assembly-plugin
Version:        2.3
Release:        2%{?dist}
Summary:        Maven Assembly Plugin

Group:          Development/Libraries
License:        ASL 2.0
URL:            http://maven.apache.org/plugins/maven-assembly-plugin/
Source0:        http://repo2.maven.org/maven2/org/apache/maven/plugins/%{name}/%{version}/%{name}-%{version}-source-release.zip

BuildArch: noarch

Obsoletes: maven2-plugin-assembly <= 0:2.0.8
Provides:  maven2-plugin-assembly = 1:%{version}-%{release}

BuildRequires: java >= 1:1.6.0
BuildRequires: jpackage-utils >= 0:1.7.2
BuildRequires:  ant
BuildRequires:  maven
BuildRequires:  maven-assembly-plugin
BuildRequires:  maven-compiler-plugin
BuildRequires:  maven-install-plugin
BuildRequires:  maven-jar-plugin
BuildRequires:  maven-resources-plugin
BuildRequires:  maven-site-plugin
BuildRequires:  maven-plugin-plugin
BuildRequires:  maven-surefire-plugin
BuildRequires:  maven-surefire-provider-junit
BuildRequires:  maven-javadoc-plugin
BuildRequires:  maven-doxia
BuildRequires:  maven-doxia-sitetools

BuildRequires: plexus-container-default
BuildRequires: plexus-utils
BuildRequires: plexus-active-collections
BuildRequires: plexus-containers-component-metadata
BuildRequires: plexus-io
BuildRequires: plexus-interpolation
BuildRequires: plexus-archiver

BuildRequires: maven-shared-file-management
BuildRequires: maven-shared-repository-builder
BuildRequires: maven-shared-filtering
BuildRequires: maven-shared-file-management
BuildRequires: maven-shared-io

BuildRequires: easymock
BuildRequires: jdom
BuildRequires: jaxen
BuildRequires: saxpath
BuildRequires: junit
BuildRequires: modello

Requires: java >= 1:1.6.0
Requires: easymock
Requires: jdom
Requires: jaxen
Requires: saxpath
Requires: plexus-container-default
Requires: plexus-utils
Requires: plexus-active-collections
Requires: plexus-containers-component-metadata
Requires: plexus-io
Requires: plexus-interpolation
Requires: plexus-archiver
Requires: maven-shared-repository-builder
Requires: maven-shared-filtering
Requires: maven-shared-file-management
Requires: maven-shared-io
Requires: jpackage-utils >= 0:1.7.2

%description
A Maven 2 plugin to create archives of your project's sources, classes, 
dependencies etc. from flexible assembly descriptors.

%package javadoc
Group:          Documentation
Summary:        Javadoc for %{name}
Requires:       jpackage-utils >= 0:1.7.2

%description javadoc
API documentation for %{name}.


%prep
%setup -q


%build
# seems koji don't have easymockclassextension
mvn-rpmbuild \
        -Dmaven.test.skip=true \
        install javadoc:aggregate

%install
# jars
install -d -m 0755 %{buildroot}%{_javadir}
install -m 644 target/%{name}-%{version}.jar   %{buildroot}%{_javadir}/%{name}.jar

# poms
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -pm 644 pom.xml \
    %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom

%add_maven_depmap JPP-%{name}.pom %{name}.jar

# javadoc
install -d -m 0755 %{buildroot}%{_javadocdir}/%{name}
cp -pr target/site/api*/* %{buildroot}%{_javadocdir}/%{name}/
rm -rf target/site/api*

%files
%{_javadir}/*
%{_mavenpomdir}/*
%{_mavendepmapfragdir}/*

%files javadoc
%{_javadocdir}/%{name}

%changelog
* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Mar 07 2012 Tomas Radej <tradej@redhat.com> - 2.3-1
- Update to latest upstream vresion.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Dec 12 2011 Tomas Radej <tradej@redhat.com> - 2.2.2-3
- Added R on plexus-containers-component-metadata

* Mon Dec 12 2011 Alexander Kurtakov <akurtako@redhat.com> 2.2.2-2
- Remove plexus-maven-plugin require.

* Tue Dec 6 2011 Alexander Kurtakov <akurtako@redhat.com> 2.2.2-1
- Update to latest upstream version.

* Sun Oct 2 2011 Alexander Kurtakov <akurtako@redhat.com> 2.2.1-4
- Add missing BR/R.

* Thu Jul 15 2011 Jaromir Capik <jcapik@redhat.com> 2.2.1-3
- modello removed from requires
- %update_maven_depmap removed

* Thu May 23 2011 Jaromir Capik <jcapik@redhat.com> 2.2.1-2
- Migration from plexus-maven-plugin to plexus-containers-component-metadata
- Missing modello dependency added
- Minor spec file changes according to the latest guidelines

* Thu Mar 17 2011 Alexander Kurtakov <akurtako@redhat.com> 2.2.1-1
- Update to upstream 2.2.1 release.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 29 2010 Alexander Kurtakov <akurtako@redhat.com> 2.2-1
- Update to final release.

* Tue Jun 15 2010 Alexander Kurtakov <akurtako@redhat.com> 2.2-0.4.beta5
- Add missing BuildRequires.

* Tue Jun 15 2010 Alexander Kurtakov <akurtako@redhat.com> 2.2-0.3.beta5
- Add missing Requires.

* Thu Jun 03 2010 Yong Yang <yyang@redhat.com> - 2.2-0.2.beta5
- Chmod 0644 for depmap.xml
- Fix Obsoletes and Provides
- Change to BR java

* Thu May 20 2010 Yong Yang <yyang@redhat.com> - 2.2-0.1.beta5
- Initial build
