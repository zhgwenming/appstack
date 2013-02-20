Name:           maven-shade-plugin
Version:        2.0
Release:        1%{?dist}
Summary:        This plugin provides the capability to package the artifact in an uber-jar

Group:          Development/Libraries
License:        ASL 2.0
URL:            http://maven.apache.org/plugins/%{name}
Source0:        http://repo2.maven.org/maven2/org/apache/maven/plugins/%{name}/%{version}/%{name}-%{version}-source-release.zip

BuildArch: noarch

BuildRequires: java-devel >= 1:1.6.0
BuildRequires: jpackage-utils
BuildRequires: plexus-utils
BuildRequires: ant
BuildRequires: maven
BuildRequires: maven-wagon
BuildRequires: plexus-container-default
BuildRequires: plexus-containers-component-metadata
BuildRequires: maven-install-plugin
BuildRequires: maven-compiler-plugin
BuildRequires: maven-plugin-plugin
BuildRequires: maven-resources-plugin
BuildRequires: maven-surefire-plugin
BuildRequires: maven-surefire-provider-junit4
BuildRequires: maven-jar-plugin
BuildRequires: maven-javadoc-plugin
BuildRequires: maven-plugin-testing-harness
BuildRequires: jdependency >= 0.6
BuildRequires: xmlunit
Requires: ant
Requires: maven
Requires: jpackage-utils
Requires: java >= 1:1.6.0
Requires: jdependency >= 0.6

Obsoletes: maven2-plugin-shade <= 0:2.0.8
Provides: maven2-plugin-shade = 1:%{version}-%{release}

%description
This plugin provides the capability to package the artifact in an
uber-jar, including its dependencies and to shade - i.e. rename - the
packages of some of the dependencies.


%package javadoc
Group:          Documentation
Summary:        API documentation for %{name}
Requires:       jpackage-utils

%description javadoc
%{summary}.

%prep
%setup -q

rm src/test/jars/plexus-utils-1.4.1.jar
ln -s $(build-classpath plexus/utils) src/test/jars/plexus-utils-1.4.1.jar

%build
# A class from aopalliance is not found. Simply adding BR does not solve it
mvn-rpmbuild install javadoc:aggregate -Dmaven.test.skip

%install
# jars
install -Dpm 644 target/%{name}-%{version}.jar   %{buildroot}%{_javadir}/%{name}.jar

# poms
install -Dpm 644 pom.xml %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom

%add_maven_depmap

# javadoc
install -dm 755 %{buildroot}%{_javadocdir}/%{name}
cp -pr target/site/api*/* %{buildroot}%{_javadocdir}/%{name}/

%files
%{_javadir}/*
%{_mavenpomdir}/*
%{_mavendepmapfragdir}/*
%doc LICENSE NOTICE


%files javadoc
%{_javadocdir}/%{name}
%doc LICENSE NOTICE

%changelog
* Thu Dec 13 2012 Tomas Radej <tradej@redhat.com> - 2.0-1
- Update to upstream 2.0

* Wed Nov 14 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.7.1-3
- Install NOTICE file with javadoc package

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jul 5 2012 Alexander Kurtakov <akurtako@redhat.com> 1.7.1-1
- Update to upstream 1.7.1.

* Wed Jun 20 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.7-1
- Update to upstream 1.7

* Fri Apr 6 2012 Alexander Kurtakov <akurtako@redhat.com> 1.6-1
- Update to latest upstream release.

* Mon Mar 05 2012 Jaromir Capik <jcapik@redhat.com> - 1.5-4
- Migration to plexus-containers-component-metadata

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 23 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.5-2
- Fix depmap macro call

* Tue Nov 1 2011 Alexander Kurtakov <akurtako@redhat.com> 1.5-1
- Update to upstream 1.5 release.

* Thu Jun 9 2011 Alexander Kurtakov <akurtako@redhat.com> 1.4-4
- Build with maven 3.x.
- Use upstream source.
- Guidelines fixes.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 26 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.4-2
- Add jdependency also to Requires

* Thu Oct 14 2010 Pierre-Yves Chibon <pingou@pingoured.fr> - 1.4-1
- Update to 1.4
- Add BR on jdependency >= 0.6
- Add patch to add dependency on maven-artifact-manager

* Thu Jul  8 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.3.3-2
- Replace plexus utils jar with symlink
- Create MAVEN_REPO_LOCAL dir before calling maven

* Tue Jun 22 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.3.3-1
- Initial package
