Name:           plexus-io
Version:        2.0.4
Release:        2%{?dist}
Summary:        Plexus IO Components

Group:          Development/Libraries
License:        ASL 2.0
URL:            http://plexus.codehaus.org/plexus-components/plexus-io
# fetched from https://github.com/sonatype/plexus-io/tarball/plexus-io-2.0.4
Source0:        sonatype-plexus-io-plexus-io-2.0.4-0-g2767dfe.tar.gz
BuildArch: noarch

BuildRequires: java-devel >= 1:1.6.0
BuildRequires:  jpackage-utils

BuildRequires: plexus-utils
BuildRequires: plexus-container-default
BuildRequires: maven
BuildRequires: maven-resources-plugin
BuildRequires: maven-compiler-plugin
BuildRequires: maven-jar-plugin
BuildRequires: maven-install-plugin
BuildRequires: maven-javadoc-plugin
BuildRequires: maven-surefire-plugin
BuildRequires: maven-surefire-provider-junit
BuildRequires: maven-doxia-sitetools
Requires:  jpackage-utils
Requires: plexus-utils
Requires: plexus-container-default

%description
Plexus IO is a set of plexus components, which are designed for use
in I/O operations.

%package javadoc
Group:          Documentation
Summary:        Javadoc for %{name}
Requires:       jpackage-utils

%description javadoc
API documentation for %{name}.


%prep
%setup -q -n sonatype-plexus-io-fd7f1a8

%build
mvn-rpmbuild install javadoc:aggregate

%install
# jars
install -d -m 0755 %{buildroot}%{_javadir}/plexus
install -m 644 target/%{name}-%{version}.jar   %{buildroot}%{_javadir}/plexus/io.jar


# poms
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -pm 644 pom.xml \
    %{buildroot}%{_mavenpomdir}/JPP.%{name}.pom

%add_maven_depmap JPP.%{name}.pom plexus/io.jar

# javadoc
install -d -m 0755 %{buildroot}%{_javadocdir}/%{name}
cp -pr target/site/api*/* %{buildroot}%{_javadocdir}/%{name}/


%files
%doc NOTICE.txt
%{_javadir}/plexus/io.jar
%{_mavenpomdir}/JPP.%{name}.pom
%{_mavendepmapfragdir}/%{name}

%files javadoc
%{_javadocdir}/%{name}

%changelog
* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Apr 18 2012 Alexander Kurtakov <akurtako@redhat.com> 2.0.4-1
- Update to latest upstream.

* Thu Feb 02 2012 Tomas Radej <tradej@redhat.com> - 2.0.2-1
- Updated to upstream version

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Sep 8 2011 Alexander Kurtakov <akurtako@redhat.com> 2.0.1-1
- Update to 2.0.1 upstream release.

* Wed Jul 27 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.0.1-2
- Use add_maven_depmap macro

* Wed Jul 27 2011 Jaromir Capik <jcapik@redhat.com> - 1.0.1-2
- Removal of plexus-maven-plugin dependency (not needed)
- Minor spec file changes according to the latest guidelines

* Tue May 17 2011 Alexander Kurtakov <akurtako@redhat.com> 1.0.1-1
- Update to upstream 1.0.1.
- Adapt to current guidelines.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.3.a5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 23 2009 Alexander Kurtakov <akurtako@redhat.com> 1.0-0.2.a5
- Fix review comments.

* Wed Dec 23 2009 Alexander Kurtakov <akurtako@redhat.com> 1.0-0.1.a5.1
- Initial package
