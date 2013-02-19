Name:           maven-plugin-tools
Version:        3.1
Release:        8%{?dist}
Epoch:          0
Summary:        Maven Plugin Tools

Group:          Development/Libraries
License:        ASL 2.0
URL:            http://maven.apache.org/plugin-tools/
Source0:        http://repo2.maven.org/maven2/org/apache/maven/plugin-tools/%{name}/%{version}/%{name}-%{version}-source-release.zip
BuildArch:      noarch

BuildRequires:  java-devel >= 1:1.6.0
BuildRequires:  jpackage-utils
BuildRequires:  maven-local
BuildRequires:  ant
BuildRequires:  bsh
BuildRequires:  jtidy
BuildRequires:  maven-artifact-manager
BuildRequires:  maven-doxia-sink-api
BuildRequires:  maven-doxia-sitetools
BuildRequires:  maven-enforcer-plugin
BuildRequires:  maven-plugin-annotations
BuildRequires:  maven-plugin-descriptor
BuildRequires:  maven-plugin-registry
BuildRequires:  maven-plugin-tools-annotations
BuildRequires:  maven-plugin-tools-api
BuildRequires:  maven-plugin-tools-generators
BuildRequires:  maven-plugin-tools-java
BuildRequires:  maven-plugin-tools-model
BuildRequires:  maven-project
BuildRequires:  maven-shared-reporting-api
BuildRequires:  maven-shared-reporting-impl
BuildRequires:  objectweb-asm
BuildRequires:  plexus-ant-factory
BuildRequires:  plexus-archiver
BuildRequires:  plexus-bsh-factory
BuildRequires:  plexus-containers-component-annotations
BuildRequires:  plexus-containers-container-default
BuildRequires:  plexus-utils
BuildRequires:  plexus-velocity
BuildRequires:  qdox
BuildRequires:  velocity
# This is parent POM of the plexus-ant-factory. It is not pulled in
# as a dependency of plexus-ant-factory, but we need it, because
# maven-script-ant subpackage fails to build without it.
BuildRequires:  plexus-component-factories-pom
# Test dependencies:
%if 0
BuildRequires:  easymock
BuildRequires:  fest-assert
BuildRequires:  junit
BuildRequires:  maven-plugin-testing-harness
BuildRequires:  plexus-compiler
BuildRequires:  xmlunit
%endif

Requires:       java
Requires:       jpackage-utils


%description
The Maven Plugin Tools contains the necessary tools to be able to produce Maven
Plugins in a variety of languages.

%package -n maven-plugin-annotations
Summary:        Maven Plugin Java 5 Annotations
Requires:       %{name} = %{epoch}:%{version}-%{release}
Requires:       java
Requires:       jpackage-utils
Requires:       maven
Obsoletes:      maven-plugin-annotations < 0:%{version}-%{release}

%description -n maven-plugin-annotations
This package contains Java 5 annotations to use in Mojos.

%package -n maven-plugin-plugin
Summary:        Maven Plugin Plugin
Requires:       %{name} = %{epoch}:%{version}-%{release}
Requires:       java
Requires:       jpackage-utils
Requires:       maven
Requires:       maven-artifact-manager
Requires:       maven-doxia-sink-api
Requires:       maven-doxia-sitetools
Requires:       maven-plugin-descriptor
Requires:       maven-plugin-registry
Requires:       maven-plugin-tools-annotations
Requires:       maven-plugin-tools-api
Requires:       maven-plugin-tools-beanshell
Requires:       maven-plugin-tools-generators
Requires:       maven-plugin-tools-java
Requires:       maven-plugin-tools-model
Requires:       maven-project
Requires:       maven-shared-reporting-api
Requires:       maven-shared-reporting-impl
Requires:       plexus-utils
Requires:       plexus-velocity
Requires:       velocity
Obsoletes:      maven2-plugin-plugin < 0:%{version}-%{release}
Provides:       maven2-plugin-plugin = 0:%{version}-%{release}

%description -n maven-plugin-plugin
The Plugin Plugin is used to create a Maven plugin descriptor for any Mojo's
found in the source tree, to include in the JAR. It is also used to generate
Xdoc files for the Mojos as well as for updating the plugin registry, the
artifact metadata and a generic help goal.

%package annotations
Summary:        Maven Plugin Tool for Annotations
Requires:       %{name} = %{epoch}:%{version}-%{release}
Requires:       java
Requires:       jpackage-utils
Requires:       maven
Requires:       maven-plugin-annotations
Requires:       maven-plugin-descriptor
Requires:       maven-plugin-tools-api
Requires:       maven-project
Requires:       objectweb-asm
Requires:       plexus-archiver
Requires:       plexus-containers-component-annotations
Requires:       plexus-containers-container-default
Requires:       plexus-utils
Requires:       qdox

%description annotations
This package provides Java 5 annotation tools for use with Apache Maven.

%package ant
Summary:        Maven Plugin Tool for Ant
Requires:       %{name} = %{epoch}:%{version}-%{release}
Requires:       java
Requires:       jpackage-utils
Requires:       maven-plugin-descriptor
Requires:       maven-plugin-tools-api
Requires:       maven-plugin-tools-model
Requires:       maven-project
Requires:       plexus-containers-component-annotations
Requires:       plexus-containers-container-default
Requires:       plexus-utils
Obsoletes:      maven-shared-plugin-tools-ant < 0:%{version}-%{release}
Provides:       maven-shared-plugin-tools-ant = 0:%{version}-%{release}

%description ant
Descriptor extractor for plugins written in Ant.

%package api
Summary:        Maven Plugin Tools APIs
Requires:       %{name} = %{epoch}:%{version}-%{release}
Requires:       java
Requires:       jpackage-utils
Requires:       maven
Requires:       maven-plugin-descriptor
Requires:       maven-project
Requires:       plexus-containers-container-default
Requires:       plexus-utils
Obsoletes:      maven-shared-plugin-tools-api < 0:%{version}-%{release}
Provides:       maven-shared-plugin-tools-api = 0:%{version}-%{release}

%description api
The Maven Plugin Tools API provides an API to extract information from
and generate documentation for Maven Plugins.

%package beanshell
Summary:        Maven Plugin Tool for Beanshell
Requires:       %{name} = %{epoch}:%{version}-%{release}
Requires:       java
Requires:       jpackage-utils
Requires:       bsh
Requires:       maven-plugin-descriptor
Requires:       maven-plugin-tools-api
Requires:       plexus-containers-component-annotations
Obsoletes:      maven-shared-plugin-tools-beanshell < 0:%{version}-%{release}
Provides:       maven-shared-plugin-tools-beanshell = 0:%{version}-%{release}

%description beanshell
Descriptor extractor for plugins written in Beanshell.

%package generators
Summary:        Maven Plugin Tools Generators
Requires:       %{name} = %{epoch}:%{version}-%{release}
Requires:       java
Requires:       jpackage-utils
Requires:       jtidy
Requires:       maven
Requires:       maven-plugin-descriptor
Requires:       maven-plugin-tools-api
Requires:       maven-project
Requires:       maven-shared-reporting-api
Requires:       objectweb-asm
Requires:       plexus-containers-container-default
Requires:       plexus-utils
Requires:       plexus-velocity
Requires:       velocity

%description generators
The Maven Plugin Tools Generators provides content generation
(documentation, help) from plugin descriptor.

%package java
Summary:        Maven Plugin Tool for Java
Requires:       %{name} = %{epoch}:%{version}-%{release}
Requires:       java
Requires:       jpackage-utils
Requires:       maven
Requires:       maven-plugin-descriptor
Requires:       maven-plugin-tools-api
Requires:       maven-project
Requires:       plexus-containers-component-annotations
Requires:       plexus-containers-container-default
Requires:       plexus-utils
Requires:       qdox
Obsoletes:      maven-shared-plugin-tools-java < 0:%{version}-%{release}
Provides:       maven-shared-plugin-tools-java = 0:%{version}-%{release}

%description java
Descriptor extractor for plugins written in Java.

# Note that this package contains code, not documentation.
# See comments about "javadocs" subpackage below.
%package javadoc
Summary:        Maven Plugin Tools Javadoc
Requires:       %{name} = %{epoch}:%{version}-%{release}
Requires:       java
Requires:       jpackage-utils
Requires:       maven-plugin-tools-java

%description javadoc
The Maven Plugin Tools Javadoc provides several Javadoc taglets to be used when
generating Javadoc.

Java API documentation for %{name} is contained in
%{name}-javadocs package. This package does not contain it.

%package model
Summary:        Maven Plugin Metadata Model
Requires:       %{name} = %{epoch}:%{version}-%{release}
Requires:       java
Requires:       jpackage-utils
Requires:       maven-plugin-descriptor
Requires:       plexus-containers-container-default
Requires:       plexus-utils
Obsoletes:      maven-shared-plugin-tools-model < 0:%{version}-%{release}
Provides:       maven-shared-plugin-tools-model = 0:%{version}-%{release}

%description model
The Maven Plugin Metadata Model provides an API to play with the Metadata
model.

%package -n maven-script
Summary:        Maven Script Mojo Support
Requires:       %{name} = %{epoch}:%{version}-%{release}
Requires:       jpackage-utils

%description -n maven-script
Maven Script Mojo Support lets developer write Maven plugins/goals
with scripting languages instead of compiled Java.

%package -n maven-script-ant
Summary:        Maven Ant Mojo Support
Requires:       maven-script = %{epoch}:%{version}-%{release}
Requires:       java
Requires:       jpackage-utils
Requires:       ant
Requires:       maven
Requires:       maven-plugin-descriptor
Requires:       maven-project
Requires:       plexus-ant-factory
Requires:       plexus-archiver
Requires:       plexus-containers-container-default
Requires:       plexus-component-factories-pom

%description -n maven-script-ant
This package provides %{summary}, which write Maven plugins with
Ant scripts.

%package -n maven-script-beanshell
Summary:        Maven Beanshell Mojo Support
Requires:       maven-script = %{epoch}:%{version}-%{release}
Requires:       java
Requires:       jpackage-utils
Requires:       maven
Requires:       plexus-bsh-factory

%description -n maven-script-beanshell
This package provides %{summary}, which write Maven plugins with
Beanshell scripts.

# This "javadocs" package violates packaging guidelines as of Sep 6 2012. The
# subpackage name "javadocs" instead of "javadoc" is intentional. There was a
# consensus that current naming scheme should be kept, even if it doesn't
# conform to the guidelines.  mizdebsk, September 2012
%package javadocs
Group:          Documentation
Summary:        Javadoc for %{name}
Requires:       jpackage-utils

%description javadocs
API documentation for %{name}.


%prep
%setup -q
# For easier installation
ln -s maven-script/maven-script-{ant,beanshell} .

%pom_xpath_inject "pom:project/pom:properties" "
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    <project.reporting.outputEncoding>UTF-8</project.reporting.outputEncoding>"

%build
mvn-rpmbuild package javadoc:aggregate -Dmaven.test.skip=true

%install
install -d -m 755 %{buildroot}%{_javadir}/%{name}
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}

# pom artifacts
install -pm 644 pom.xml %{buildroot}%{_mavenpomdir}/JPP.%{name}-%{name}.pom
%add_maven_depmap JPP.%{name}-%{name}.pom
install -pm 644 maven-script/pom.xml %{buildroot}%{_mavenpomdir}/JPP.%{name}-maven-script.pom
%add_maven_depmap -f maven-script JPP.%{name}-maven-script.pom
mv %{buildroot}%{_mavendepmapfragdir}/%{name}-maven-script %{buildroot}%{_mavendepmapfragdir}/maven-script

# jar or plugin artifacts
for module in                      \
    maven-plugin-annotations       \
    maven-plugin-plugin            \
    maven-plugin-tools-annotations \
    maven-plugin-tools-ant         \
    maven-plugin-tools-api         \
    maven-plugin-tools-beanshell   \
    maven-plugin-tools-generators  \
    maven-plugin-tools-java        \
    maven-plugin-tools-javadoc     \
    maven-plugin-tools-model       \
    maven-script-ant               \
    maven-script-beanshell
do
    install -p -m 644 ${module}/target/${module}-%{version}.jar %{buildroot}%{_javadir}/%{name}/${module}.jar
    install -p -m 644 ${module}/pom.xml %{buildroot}%{_mavenpomdir}/JPP.%{name}-${module}.pom
    %add_maven_depmap -f ${module} JPP.%{name}-${module}.pom %{name}/${module}.jar
    mv %{buildroot}%{_mavendepmapfragdir}/%{name}-${module} %{buildroot}%{_mavendepmapfragdir}/${module}
done

# javadoc
cp -pr target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}


%files
%doc LICENSE NOTICE
%{_mavenpomdir}/JPP.%{name}-%{name}.pom
%{_mavendepmapfragdir}/%{name}

%files -n maven-plugin-annotations
%{_javadir}/%{name}/maven-plugin-annotations.jar
%{_mavenpomdir}/JPP.%{name}-maven-plugin-annotations.pom
%{_mavendepmapfragdir}/maven-plugin-annotations

%files -n maven-plugin-plugin
%{_javadir}/%{name}/maven-plugin-plugin.jar
%{_mavenpomdir}/JPP.%{name}-maven-plugin-plugin.pom
%{_mavendepmapfragdir}/maven-plugin-plugin

%files annotations
%{_javadir}/%{name}/%{name}-annotations.jar
%{_mavenpomdir}/JPP.%{name}-%{name}-annotations.pom
%{_mavendepmapfragdir}/%{name}-annotations

%files ant
%{_javadir}/%{name}/%{name}-ant.jar
%{_mavenpomdir}/JPP.%{name}-%{name}-ant.pom
%{_mavendepmapfragdir}/%{name}-ant

%files api
%{_javadir}/%{name}/%{name}-api.jar
%{_mavenpomdir}/JPP.%{name}-%{name}-api.pom
%{_mavendepmapfragdir}/%{name}-api

%files beanshell
%{_javadir}/%{name}/%{name}-beanshell.jar
%{_mavenpomdir}/JPP.%{name}-%{name}-beanshell.pom
%{_mavendepmapfragdir}/%{name}-beanshell

%files generators
%{_javadir}/%{name}/%{name}-generators.jar
%{_mavenpomdir}/JPP.%{name}-%{name}-generators.pom
%{_mavendepmapfragdir}/%{name}-generators

%files java
%{_javadir}/%{name}/%{name}-java.jar
%{_mavenpomdir}/JPP.%{name}-%{name}-java.pom
%{_mavendepmapfragdir}/%{name}-java

%files javadoc
%{_javadir}/%{name}/%{name}-javadoc.jar
%{_mavenpomdir}/JPP.%{name}-%{name}-javadoc.pom
%{_mavendepmapfragdir}/%{name}-javadoc

%files model
%{_javadir}/%{name}/%{name}-model.jar
%{_mavenpomdir}/JPP.%{name}-%{name}-model.pom
%{_mavendepmapfragdir}/%{name}-model

%files -n maven-script
%{_mavenpomdir}/JPP.%{name}-maven-script.pom
%{_mavendepmapfragdir}/maven-script

%files -n maven-script-ant
%{_javadir}/%{name}/maven-script-ant.jar
%{_mavenpomdir}/JPP.%{name}-maven-script-ant.pom
%{_mavendepmapfragdir}/maven-script-ant

%files -n maven-script-beanshell
%{_javadir}/%{name}/maven-script-beanshell.jar
%{_mavenpomdir}/JPP.%{name}-maven-script-beanshell.pom
%{_mavendepmapfragdir}/maven-script-beanshell

%files javadocs
%doc LICENSE NOTICE
%{_javadocdir}/%{name}


%changelog
* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 0:3.1-8
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Fri Dec 21 2012 Michal Srb <msrb@redhat.com> - 0:3.1-7
- Migrated from maven-doxia to doxia subpackage (Resolves: #889147)

* Wed Nov 14 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:3.1-6
- Skip running tests because they are failing

* Tue Sep 11 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:3.1-5
- Add missing requires

* Tue Sep 11 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:3.1-4
- Rebuild without bootstrap

* Tue Sep 11 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:3.1-3
- Add obsoletes for maven-plugin-annotations

* Mon Sep 10 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:3.1-2
- Bump release

* Fri Sep  7 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:3.1-1
- Update to upstream version 3.1
- Bootstrap using prebuilt upstream binaries

* Thu Sep  6 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.7-7
- Remove rpm bug workaround

* Tue Aug 28 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.7-6
- Wrap descriptions at column 80
- Install LICENSE and NOTICE files

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 16 2011 Jaromir Capik <jcapik@redhat.com> -  0:2.7-3
- Missing com.sun.javadoc / com.sun.tools.doclet forced in the POM

* Tue Aug 16 2011 Jaromir Capik <jcapik@redhat.com> -  0:2.7-2
- Removal of plexus-maven-plugin (not needed)
- Migration to maven3
- Removal of unwanted file duplicates
- Minor spec file changes according to the latest guidelines

* Sat Feb 12 2011 Alexander Kurtakov <akurtako@redhat.com> 0:2.7-1
- Update to new upstream release.
- Adapt to current guidelines.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Sep 30 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:2.6-8
- Remove jtidy depmap (not needed anymore)

* Wed Sep 29 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:2.6-7
- Add patch for new jtidy
- Add jtidy depmap

* Wed Sep 8 2010 Alexander Kurtakov <akurtako@redhat.com> 0:2.6-6
- BR maven-site-plugin.
- Use javadoc:aggregate for multimodule projects.

* Thu May 27 2010 Alexander Kurtakov <akurtako@redhat.com> 0:2.6-5
- Add missing requires.
- Drop modello patches not needed anymore.

* Wed May 19 2010 Alexander Kurtakov <akurtako@redhat.com> 0:2.6-4
- Fix plugin-tools-java obsoletes.

* Tue May 18 2010 Alexander Kurtakov <akurtako@redhat.com> 0:2.6-3
- More BRs.

* Tue May 18 2010 Alexander Kurtakov <akurtako@redhat.com> 0:2.6-2
- Fix BRs.

* Tue May 18 2010 Alexander Kurtakov <akurtako@redhat.com> 2.6-0
- Update to 2.6.
- Separate modules as subpackages.

* Mon Nov 23 2009 Alexander Kurtakov <akurtako@redhat.com> 0:2.1-6
- BR maven-plugin-tools.

* Mon Aug 31 2009 Alexander Kurtakov <akurtako@redhat.com> 0:2.1-5
- Set minimum version for plexus-utils BR.
- BR java-devel.
- Fix javadoc subpackage description.

* Mon Aug 31 2009 Alexander Kurtakov <akurtako@redhat.com> 0:2.1-4
- Adapt for Fedora.

* Wed May 20 2009 Fernando Nasser <fnasser@redhat.com> - 0:2.1-3
- Fix license
- Fix URL

* Mon Apr 27 2009 Yong Yang <yyang@redhat.com> - 0:2.1-2
- Add BRs for maven-doxia*
- Rebuild with maven2-2.0.8 built in non-bootstrap mode

* Mon Mar 09 2009 Yong Yang <yyang@redhat.com> - 0:2.1-1
- Import from dbhole's maven2 2.0.8 packages

* Mon Apr 07 2008 Deepak Bhole <dbhole@redhat.com> - 0:2.1-0jpp.1
- Initial build
