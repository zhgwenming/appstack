Name:           maven-jar-plugin
Version:        2.4
Release:        3%{?dist}
Summary:        Maven JAR Plugin

Group:          Development/Libraries
License:        ASL 2.0
URL:            http://maven.apache.org/plugins/maven-jar-plugin/
Source0:        http://repo2.maven.org/maven2/org/apache/maven/plugins/%{name}/%{version}/%{name}-%{version}-source-release.zip

# Some classes from maven-artifact come in maven-core, added a dep in pom.xml
Patch0:         %{name}-maven-core-dep.patch

BuildArch: noarch

BuildRequires: java-devel >= 1:1.6.0
BuildRequires: javapackages-tools >= 0.7.0
BuildRequires: maven
BuildRequires: maven-plugin-plugin
BuildRequires: maven-jar-plugin
BuildRequires: maven-install-plugin
BuildRequires: maven-resources-plugin
BuildRequires: maven-compiler-plugin
BuildRequires: maven-javadoc-plugin
BuildRequires: maven-surefire-plugin
BuildRequires: maven-surefire-provider-junit
BuildRequires: maven-doxia-sitetools
BuildRequires: maven-plugin-testing-harness
BuildRequires: maven-archiver
BuildRequires: plexus-archiver
BuildRequires: apache-commons-lang
BuildRequires: plexus-utils
BuildRequires: junit
Requires: maven
Requires: maven-archiver
Requires: plexus-archiver
Requires: maven-archiver
Requires: apache-commons-lang
Requires: plexus-utils
Requires: maven-plugin-testing-harness
Requires: junit
Requires: java

Provides:       maven2-plugin-jar = %{version}-%{release}
Obsoletes:      maven2-plugin-jar <= 0:2.0.8

%description
Builds a Java Archive (JAR) file from the compiled
project classes and resources.

%package javadoc
Group:          Documentation
Summary:        Javadoc for %{name}
Requires:       jpackage-utils

%description javadoc
API documentation for %{name}.


%prep
%setup -q
%patch0 -p1

#let plexus-container-default be retrieved as a dependency
sed -i -e "s|plexus-container-default|plexus-container|g" pom.xml

%build
# Test class MockArtifact doesn't override method getMetadata
mvn-rpmbuild install javadoc:aggregate -Dmaven.test.skip

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

%files -f .mfiles
%doc LICENSE NOTICE

%files javadoc
%doc LICENSE NOTICE
%{_javadocdir}/%{name}

%changelog
* Tue Nov 13 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.4-3
- Install license files
- Use generated maven file lists

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Feb 15 2012 Alexander Kurtakov <akurtako@redhat.com> 2.4-1
- Update to 2.4.0.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Sep 19 2011 Tomas Radej <tradej@redhat.com> - 2.3.2-1
- Updated to 2.3.2

* Fri Jun 17 2011 Alexander Kurtakov <akurtako@redhat.com> 2.3.1-3
- Build with maven 3.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Sep 10 2010 Alexander Kurtakov <akurtako@redhat.com> 2.3.1-1
- Update to 2.3.1.
- Keep plexus-container-default on the dependency tree.
- Drop depmap - not needed now.

* Wed May 19 2010 Alexander Kurtakov <akurtako@redhat.com> 2.3-3
- Add depmap.

* Wed May 19 2010 Alexander Kurtakov <akurtako@redhat.com> 2.3-2
- Requires maven-shared-archiver.

* Thu May 13 2010 Alexander Kurtakov <akurtako@redhat.com> 2.3-1
- Initial package
