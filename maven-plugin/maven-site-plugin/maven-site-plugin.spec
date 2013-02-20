Name:           maven-site-plugin
Version:        3.1
Release:        3%{?dist}
Summary:        Maven Site Plugin

Group:          Development/Libraries
License:        ASL 2.0
URL:            http://maven.apache.org/plugins/maven-site-plugin/
Source0:        http://repo2.maven.org/maven2/org/apache/maven/plugins/%{name}/%{version}/%{name}-%{version}-source-release.zip

Patch0:         0001-Set-source-encoding-property-to-UTF8.patch
Patch1:         0002-Port-to-jetty-8.x.patch

BuildArch: noarch

BuildRequires: java-devel >= 1:1.6.0
BuildRequires: maven
BuildRequires: maven-artifact-manager
BuildRequires: maven-plugin-plugin
BuildRequires: maven-assembly-plugin
BuildRequires: maven-compiler-plugin
BuildRequires: maven-install-plugin
BuildRequires: maven-javadoc-plugin
BuildRequires: maven-jar-plugin
BuildRequires: maven-resources-plugin
BuildRequires: maven-doxia
BuildRequires: maven-doxia-sitetools
BuildRequires: maven-doxia-tools
BuildRequires: maven-project
BuildRequires: maven-surefire-plugin
BuildRequires: maven-surefire-provider-junit
BuildRequires: maven-shade-plugin
BuildRequires: maven-plugin-testing-harness
BuildRequires: maven-wagon
BuildRequires: maven-reporting-exec
BuildRequires: plexus-containers-component-metadata
BuildRequires: jetty-client >= 8.1.0-0.1.rc5
BuildRequires: jetty-server >= 8.1.0-0.1.rc5
BuildRequires: jetty-servlet >= 8.1.0-0.1.rc5
BuildRequires: jetty-util >= 8.1.0-0.1.rc5
BuildRequires: jetty-webapp >= 8.1.0-0.1.rc5
BuildRequires: servlet3
BuildRequires: plexus-archiver
BuildRequires: plexus-containers-container-default
BuildRequires: plexus-i18n
BuildRequires: plexus-velocity
BuildRequires: plexus-utils
BuildRequires: jetty-parent

Requires: maven
Requires: jetty-server >= 8.1.0-0.1.rc5
Requires: jetty-util >= 8.1.0-0.1.rc5
Requires: jetty-webapp >= 8.1.0-0.1.rc5
Requires: java
Requires: jpackage-utils
Requires: maven-artifact-manager
Requires: maven-doxia-tools
Requires: maven-project
Requires: maven-shared-reporting-api
Requires: maven-wagon
Requires: maven-reporting-exec
Requires: servlet3
Requires: plexus-archiver
Requires: plexus-containers-container-default
Requires: plexus-i18n
Requires: plexus-velocity
Requires: plexus-utils
Requires: jetty-parent

Provides:       maven2-plugin-site = %{version}-%{release}
Obsoletes:      maven2-plugin-site <= 0:2.0.8

%description
The Maven Site Plugin is a plugin that generates a site for the current project.

%package javadoc
Group:          Documentation
Summary:        Javadoc for %{name}
Requires:       jpackage-utils

%description javadoc
API documentation for %{name}.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
# skipping tests because we need to fix them first for jetty update
mvn-rpmbuild \
        -Dmaven.test.skip=true \
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

%files javadoc
%doc LICENSE NOTICE
%{_javadocdir}/%{name}

%changelog
* Tue Oct 30 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1-3
- Don't require full jetty, only minimal set of subpackages

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 20 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1-1
- Updatw to upstream 3.1

* Wed Apr 18 2012 Alexander Kurtakov <akurtako@redhat.com> 3.0-5
- BR/R servlet 3.

* Thu Jan 26 2012 Alexander Kurtakov <akurtako@redhat.com> 3.0-4
- Add BR/R on jetty-parent.

* Thu Jan 26 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0-3
- Port for jetty 8.1.0
- Small spec cleanups

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Aug 12 2011 Alexander Kurtakov <akurtako@redhat.com> 3.0-1
- Update to upstream 3.0 release.

* Thu Jul 21 2011 Jaromir Capik <jcapik@redhat.com> - 2.3-3
- Removal of plexus-maven-plugin dependency (not needed)

* Thu Jun 23 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.3-2
- Add several missing things to (Build)Requires
- Fix build for maven3-only buildroot

* Wed May 25 2011 Alexander Kurtakov <akurtako@redhat.com> 2.3-1
- Update to new upstream version.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 26 2011 Alexander Kurtakov <akurtako@redhat.com> 2.2-1
- Update to new upstream version.

* Tue Jun 15 2010 Alexander Kurtakov <akurtako@redhat.com> 2.1-3
- Requires maven-doxia-tools.

* Tue May 18 2010 Alexander Kurtakov <akurtako@redhat.com> 2.1-2
- Fix requires.

* Tue May 18 2010 Alexander Kurtakov <akurtako@redhat.com> 2.1-1
- Initial package.
