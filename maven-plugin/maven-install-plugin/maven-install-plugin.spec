Name:           maven-install-plugin
Version:        2.3.1
Release:        7%{?dist}
Summary:        Maven Install Plugin

Group:          Development/Libraries
License:        ASL 2.0
URL:            http://maven.apache.org/plugins/maven-install-plugin
Source0:        http://repo2.maven.org/maven2/org/apache/maven/plugins/%{name}/%{version}/%{name}-%{version}-source-release.zip

BuildArch:      noarch

BuildRequires: java-devel >= 1:1.6.0
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
BuildRequires: plexus-utils
BuildRequires: plexus-digest
BuildRequires: junit
BuildRequires: maven-archiver
BuildRequires: maven-shared-reporting-impl
BuildRequires: maven-artifact

Requires: maven
Requires: jpackage-utils
Requires: java
Requires: maven-archiver
Requires: plexus-digest

Provides:       maven2-plugin-install = %{version}-%{release}
Obsoletes:      maven2-plugin-install <= 0:2.0.8

%description
Copies the project artifacts to the user's local repository.

%package javadoc
Group:          Documentation
Summary:        Javadoc for %{name}
Requires:       jpackage-utils

%description javadoc
API documentation for %{name}.


%prep
%setup -q

%build
mvn-rpmbuild \
        -Dmaven.test.failure.ignore=true \
        install javadoc:javadoc

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

%files
%doc LICENSE NOTICE
%{_javadir}/%{name}.jar
%{_mavenpomdir}/JPP-%{name}.pom
%{_mavendepmapfragdir}/%{name}
%doc LICENSE NOTICE

%files javadoc
%doc LICENSE
%{_javadocdir}/%{name}
%doc LICENSE NOTICE

%changelog
* Mon Dec 10 2012 Weinan Li <weli@redhat.com> 2.3.1-7
- Install license files

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Dec  5 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.3.1-4
- Fixes for pure maven 3 build without maven 2 in buildroot
- Guideline fixes

* Fri Jun 3 2011 Alexander Kurtakov <akurtako@redhat.com> 2.3.1-3
- Build with maven v3.
- Guidelines fixes.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Oct 14 2010 Alexander Kurtakov <akurtako@redhat.com> 2.3.1-1
- Update to 2.3.1.
- Install License.

* Thu Sep 09 2010 Hui Wang <huwang@redhat.com> 2.3-8
- Add pom.patch

* Fri May 21 2010 Alexander Kurtakov <akurtako@redhat.com> 2.3-7
- BR: plexus-digest.

* Fri May 21 2010 Alexander Kurtakov <akurtako@redhat.com> 2.3-6
- Requires: plexus-digest.

* Wed May 19 2010 Hui Wang <huwang@redhat.com> - 2.3-5
- Added missing BR : maven-shared-reporting-impl

* Wed May 19 2010 Hui Wang <huwang@redhat.com> - 2.3-4
- Added missing obsoletes/provides

* Wed May 19 2010 Hui Wang <huwang@redhat.com> - 2.3-3
- Added missing BR : maven-archiver

* Mon May 17 2010 Hui Wang <huwang@redhat.com> - 2.3-2
- Fixed install -pm 644 pom.xml

* Fri May 14 2010 Hui Wang <huwang@redhat.com> - 2.3-1
- Initial version of the package
