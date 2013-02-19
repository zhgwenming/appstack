%global bootstrap 0
%global __jar_repack 0

%global main_pkg maven

Name:	    maven2
Version:	2.2.1
Release:	42%{?dist}
Summary:	Java project management and project comprehension tool

Group:		Development/Build Tools
License:	ASL 2.0 and MIT and BSD
URL:		http://maven.apache.org

# export https://svn.apache.org/repos/asf/maven/maven-2/tags/maven-%{version}/ apache-maven-%{version}
# tar czvf %{name}-%{version}.tar.gz apache-maven-%{version}
Source0:	%{name}-%{version}.tar.gz


# 1xx for non-upstream/created sources
Source100:    %{name}-%{version}-settings.xml
Source103:    %{name}-%{version}-depmap.xml

Patch0:     %{name}-antbuild.patch
Patch2:     %{name}-%{version}-update-tests.patch
Patch3:     %{name}-%{version}-enable-bootstrap-repo.patch
Patch4:     %{name}-%{version}-unshade.patch
Patch5:     %{name}-%{version}-default-resolver-pool-size.patch
Patch6:     %{name}-%{version}-strip-jackrabbit-dep.patch
Patch7:     %{name}-%{version}-classworlds.patch

BuildRequires: java-devel >= 1.6.0

%if %{bootstrap}
BuildRequires: ant
%else
BuildRequires: apache-resource-bundles
BuildRequires: objectweb-asm
BuildRequires: buildnumber-maven-plugin
BuildRequires: bsh
BuildRequires: jsch
BuildRequires: apache-commons-codec
BuildRequires: jakarta-commons-httpclient
BuildRequires: apache-commons-io
BuildRequires: apache-commons-lang
BuildRequires: apache-commons-logging
BuildRequires: apache-commons-cli
BuildRequires: apache-commons-collections
BuildRequires: apache-commons-parent
BuildRequires: maven-local
BuildRequires: maven-enforcer-plugin
BuildRequires: maven-shade-plugin
%endif


BuildArch: noarch

%description
Apache Maven is a software project management and comprehension tool. Based on
the concept of a project object model (POM), Maven can manage a project's
build, reporting and documentation from a central piece of information.

%package -n maven-artifact
Group:          Development/Libraries
Summary:        Compatibility Maven artifact artifact
Requires:       jpackage-utils
Requires:       plexus-utils
Requires:       plexus-containers-container-default

%description -n maven-artifact
Maven artifact manager artifact

%package -n maven-artifact-manager
Group:          Development/Libraries
Summary:        Compatibility Maven artifact manager artifact
Requires:       jpackage-utils
Requires:       plexus-classworlds
Requires:       plexus-utils
Requires:       plexus-containers-container-default
Requires:       maven-artifact = %{version}-%{release}
Requires:       maven-wagon

%description -n maven-artifact-manager
Maven artifact manager artifact

%package -n maven-error-diagnostics
Group:          Development/Libraries
Summary:        Compatibility Maven error diagnostics artifact
Requires:       jpackage-utils
Requires:       plexus-containers-container-default

%description -n maven-error-diagnostics
Maven error diagnostics artifact

%package -n maven-model
Group:          Development/Libraries
Summary:        Compatibility Maven model artifact
Requires:       jpackage-utils
Requires:       plexus-utils

%description -n maven-model
Maven model artifact

%package -n maven-monitor
Group:          Development/Libraries
Summary:        Compatibility Maven monitor artifact
Requires:       jpackage-utils

%description -n maven-monitor
Maven monitor artifact

%package -n maven-plugin-registry
Group:          Development/Libraries
Summary:        Compatibility Maven plugin registry artifact
Requires:       jpackage-utils
Requires:       plexus-utils
Requires:       plexus-containers-container-default

%description -n maven-plugin-registry
Maven plugin registry artifact

%package -n maven-profile
Group:          Development/Libraries
Summary:        Compatibility Maven profile artifact
Requires:       jpackage-utils
Requires:       maven-model = %{version}-%{release}
Requires:       plexus-utils
Requires:       plexus-interpolation
Requires:       plexus-containers-container-default

%description -n maven-profile
Maven profile artifact

%package -n maven-project
Group:          Development/Libraries
Summary:        Compatibility Maven project artifact
Requires:       jpackage-utils
Requires:       maven-artifact-manager = %{version}-%{release}
Requires:       maven-profile = %{version}-%{release}
Requires:       maven-plugin-registry = %{version}-%{release}
Requires:       maven-model = %{version}-%{release}
Requires:       maven-settings = %{version}-%{release}
Requires:       plexus-interpolation
Requires:       plexus-utils
Requires:       plexus-containers-container-default

%description -n maven-project
Maven project artifact

%package -n maven-settings
Group:          Development/Libraries
Summary:        Compatibility Maven settings artifact
Requires:       jpackage-utils
Requires:       maven-model = %{version}-%{release}
Requires:       plexus-interpolation
Requires:       plexus-utils
Requires:       plexus-containers-container-default

%description -n maven-settings
Maven settings artifact

%package -n maven-toolchain
Group:          Development/Libraries
Summary:        Compatibility Maven toolchain artifact
Requires:       jpackage-utils

%description -n maven-toolchain
Maven toolchain artifact

%package -n maven-plugin-descriptor
Group:          Development/Libraries
Summary:        Maven Plugin Description Model
Requires:       jpackage-utils
Requires:       maven
Requires:       plexus-classworlds
Requires:       plexus-container-default

%description -n maven-plugin-descriptor
Maven toolchain artifact

%package javadoc
Summary:        Javadoc for %{name}
Group:          Documentation
Requires:       jpackage-utils

%description javadoc
Javadoc for %{name}.


%prep
%setup -q -n apache-maven-2.2.1

%patch0 -b .antbuild
%patch2 -b .update-tests

%if ! %{bootstrap}
%patch4 -b .unshade
%endif

%if %{bootstrap}
%patch3 -b .enable-bootstrap-repo
%endif

# set cache location
export M2_REPO=`pwd`/.m2
mkdir $M2_REPO

# if bootstrapping, extract the dependencies
%if %{bootstrap}
(cd $M2_REPO

  tar xzf %{SOURCE1}

  # maven-remote-resources-plugin (m-r-r-p) is used side-by-side with
  # plexus-velocity (p-v) 1.1.3 upstream.. we collapse to a single p-v version
  # of 1.1.7. 1.1.7 however has a component descriptor that conflicts
  # with the one in m-r-r-p. We therefore need to remove the descriptor
  # from m-r-r-p first
  zip -d repository/org/apache/maven/plugins/maven-remote-resources-plugin/1.0-beta-2/maven-remote-resources-plugin-1.0-beta-2.jar \
         META-INF/plexus/components.xml

  # resource bundle 1.3 is needed during build, but not when done via
  # upstream, for some reason
  mkdir -p repository/org/apache/apache-jar-resource-bundle/1.3
  ln -s ../1.4/apache-jar-resource-bundle-1.4.jar \
        repository/org/apache/apache-jar-resource-bundle/1.3/apache-jar-resource-bundle-1.3.jar
  ln -s ../1.4/apache-jar-resource-bundle-1.4.jar.sha1 \
        repository/org/apache/apache-jar-resource-bundle/1.3/apache-jar-resource-bundle-1.3.jar.sha1
)
%endif

# disable parallel artifact resolution
%patch5 -p1 -b .parallel-artifacts-resolution

# remove unneeded jackrabbit dependency
%patch6 -p1 -b .strip-jackrabbit-dep

#%patch7 -p1 -b .classworlds

for nobuild in apache-maven maven-artifact-test \
               maven-compat maven-core maven-plugin-api \
               maven-plugin-parameter-documenter maven-reporting \
               maven-script;do
    %pom_disable_module $nobuild
done

# Don't depend on backport-util-concurrent
%pom_remove_dep :backport-util-concurrent
%pom_remove_dep :backport-util-concurrent maven-artifact-manager
sed -i s/edu.emory.mathcs.backport.// `find -name DefaultArtifactResolver.java`

%build
export M2_REPO=`pwd`/.m2
export M2_HOME=`pwd`/installation/apache-maven-%{version}

# copy settings to where ant reads from
mkdir -p $M2_HOME/conf
cp %{SOURCE100} $M2_HOME/conf/settings.xml

# replace locations in the copied settings file
sed -i -e s:__M2_LOCALREPO_PLACEHOLDER__:"file\://$M2_REPO/cache":g $M2_HOME/conf/settings.xml
sed -i -e s:__M2_REMOTEREPO_PLACEHOLDER__:"file\://$M2_REPO/repository":g $M2_HOME/conf/settings.xml

# replace settings file location before patching
sed -i -s s:__M2_SETTINGS_FILE__:$M2_HOME/conf/settings.xml:g build.xml

%if %{bootstrap}
ant -Dmaven.repo.local=$M2_REPO/cache
%else
mvn-rpmbuild -Dmaven.test.skip=true -P all-models \
             -Dmaven.local.depmap.file=%{SOURCE103} \
             install javadoc:aggregate
%endif

%install

# maven2 directory in /usr/share/java
install -dm 755 $RPM_BUILD_ROOT%{_javadir}/%{main_pkg}
install -dm 755 $RPM_BUILD_ROOT%{_mavenpomdir}


# parts of maven2 now go into separate subpackages
for subdir in maven-artifact-manager maven-error-diagnostics \
              maven-monitor maven-plugin-registry \
              maven-profile maven-project maven-toolchain maven-plugin-descriptor ;do
     pushd $subdir
     install -m 644 target/$subdir-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{main_pkg}/$subdir.jar
     install -m 644 pom.xml $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{main_pkg}-$subdir.pom
     %add_maven_depmap JPP.%{main_pkg}-$subdir.pom %{main_pkg}/$subdir.jar -f $subdir
     popd
done

# these parts are compatibility versions which are available in
# maven-3.x as well. We default to maven-3, but if someone asks for
# 2.x we provide few compat versions
for subdir in \
  maven-artifact \
  maven-model \
  maven-settings;
do
     pushd $subdir
     install -m 644 target/$subdir-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{main_pkg}/$subdir.jar
     install -m 644 pom.xml $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{main_pkg}-$subdir.pom
     %add_maven_depmap JPP.%{main_pkg}-$subdir.pom %{main_pkg}/$subdir.jar -f $subdir -v "2.0.2,2.0.6,2.0.7,2.0.8"
     popd
done

# javadoc
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}
cp -pr target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}



%files -n maven-artifact
%{_mavendepmapfragdir}/%{name}-maven-artifact
%{_javadir}/%{main_pkg}/maven-artifact-2.*.jar
%{_mavenpomdir}/JPP.%{main_pkg}-maven-artifact-2.*.pom

%files -n maven-artifact-manager
%doc LICENSE.txt NOTICE.txt
%{_mavendepmapfragdir}/%{name}-maven-artifact-manager
%{_javadir}/%{main_pkg}/maven-artifact-manager.jar
%{_mavenpomdir}/JPP.%{main_pkg}-maven-artifact-manager.pom

%files -n maven-error-diagnostics
%doc LICENSE.txt NOTICE.txt
%{_mavendepmapfragdir}/%{name}-maven-error-diagnostics
%{_javadir}/%{main_pkg}/maven-error-diagnostics.jar
%{_mavenpomdir}/JPP.%{main_pkg}-maven-error-diagnostics.pom

%files -n maven-model
%doc LICENSE.txt NOTICE.txt
%{_mavendepmapfragdir}/%{name}-maven-model
%{_javadir}/%{main_pkg}/maven-model-*.jar
%{_mavenpomdir}/JPP.%{main_pkg}-maven-model-*.pom

%files -n maven-monitor
%doc LICENSE.txt NOTICE.txt
%{_mavendepmapfragdir}/%{name}-maven-monitor
%{_javadir}/%{main_pkg}/maven-monitor.jar
%{_mavenpomdir}/JPP.%{main_pkg}-maven-monitor.pom

%files -n maven-plugin-registry
%doc LICENSE.txt NOTICE.txt
%{_mavendepmapfragdir}/%{name}-maven-plugin-registry
%{_javadir}/%{main_pkg}/maven-plugin-registry.jar
%{_mavenpomdir}/JPP.%{main_pkg}-maven-plugin-registry.pom

%files -n maven-profile
%doc LICENSE.txt NOTICE.txt
%{_mavendepmapfragdir}/%{name}-maven-profile
%{_javadir}/%{main_pkg}/maven-profile.jar
%{_mavenpomdir}/JPP.%{main_pkg}-maven-profile.pom

%files -n maven-project
%doc LICENSE.txt NOTICE.txt
%{_mavendepmapfragdir}/%{name}-maven-project
%{_javadir}/%{main_pkg}/maven-project.jar
%{_mavenpomdir}/JPP.%{main_pkg}-maven-project.pom

%files -n maven-settings
%doc LICENSE.txt NOTICE.txt
%{_mavendepmapfragdir}/%{name}-maven-settings
%{_javadir}/%{main_pkg}/maven-settings-*.jar
%{_mavenpomdir}/JPP.%{main_pkg}-maven-settings-*.pom

%files -n maven-toolchain
%doc LICENSE.txt NOTICE.txt
%{_mavendepmapfragdir}/%{name}-maven-toolchain
%{_javadir}/%{main_pkg}/maven-toolchain.jar
%{_mavenpomdir}/JPP.%{main_pkg}-maven-toolchain.pom

%files -n maven-plugin-descriptor
%doc LICENSE.txt NOTICE.txt
%{_mavendepmapfragdir}/%{name}-maven-plugin-descriptor
%{_javadir}/%{main_pkg}/maven-plugin-descriptor.jar
%{_mavenpomdir}/JPP.%{main_pkg}-maven-plugin-descriptor.pom

%files javadoc
%doc LICENSE.txt NOTICE.txt
%{_javadocdir}/*


%changelog
* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-42
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 2.2.1-41
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Fri Nov 23 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2.1-40
- Add license to javadoc subpackage

* Thu Nov 22 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2.1-39
- Add license and notice files to packages
- Add javadoc subpackage

* Fri Nov  9 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2.1-38
- Don't depend on backport-util-concurrent

* Mon Aug 20 2012 Michel Salim <salimma@fedoraproject.org> - 2.2.1-37
- Provide compatibility versions for maven-artifact and -settings

* Thu Jul 26 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2.1-36
- Remove mistaken epoch use in requires

* Wed Jul 25 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2.1-35
- Move artifacts together with maven-3 files
- Provide compatibility versions for maven-model

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed May  9 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2.1-33
- Completely remove main package since it was just confusing

* Wed Jan 25 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2.1-32
- Stip down maven 2 to bare minimum
- Remove scripts and most of home

* Mon Jan 23 2012 Tomas Radej <tradej@redhat.com> - 2.2.1-31
- Fixed Requires for plugin-descriptor

* Mon Jan 23 2012 Tomas Radej <tradej@redhat.com> - 2.2.1-30
- Moved plugin-descriptor into subpackage

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Oct 11 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2.1-28
- Provide mvn2 script instead of mvn (maven provides that now)

* Tue Jul 19 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2.1-27
- Add maven-error-diagnostics subpackage
- Order subpackages according to alphabet

* Tue Jul 19 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2.1-26
- Unown jars contained in subpackages (#723124)

* Mon Jun 27 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2.1-25
- Add maven-toolchain subpackage

* Fri Jun 24 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2.1-24
- Add few new subpackages
- Add several missing requires to new subpackages

* Fri Jun 24 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2.1-23
- Split artifact-manager and project into subpackages
- Fix resolver to process poms and fragments from datadir
- No more need to update_maven_depmap after this update

* Mon Apr 18 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2.1-22
- Fix jpp script to limit maven2.jpp.mode scope

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 19 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2.1-20
- Add maven-artifact-test to installation

* Tue Jan 18 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2.1-19
- Print plugin collector debug output only when maven2.jpp.debug mode is on

* Wed Dec 22 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2.1-18
- Add xml-commons-apis to lib directory
- fixes NoClassDefFoundError org/w3c/dom/ElementTraversal

* Fri Dec 10 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2.1-17
- Add conditional BRs to enable ff merge between f14 and f15
- Remove jackrabbit dependency from pom files

* Fri Dec 10 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2.1-16
- Fix installation of pom files for artifact jars

* Mon Nov 22 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2.1-15
- Add apache-commons-parent to BR/R
- Rename BRs from jakarta-commons to apache-commons

* Thu Nov 11 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2.1-14
- Remove old depmaps from -depmap.xml file
- Fix argument quoting for mvn scripts (Resolves rhbz#647945)

* Mon Sep 20 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2.1-13
- Create dangling symlinks during install (Resolves rhbz#613866)

* Fri Sep 17 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2.1-12
- Update JPackageRepositoryLayout to handle "signature" packaging

* Mon Sep 13 2010 Yong Yang <yyang@redhat.com> 2.2.1-11
- Add -P all-models to generate maven model v3

* Wed Sep 1 2010 Alexander Kurtakov <akurtako@redhat.com> 2.2.1-10
- Remove buildnumber-maven-plugins deps now that is fixed.
- Use new package names in BR/R.
- Use global instead of define.

* Fri Aug 27 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2.1-9
- Remove failing tests after maven-surefire 2.6 update

* Thu Aug 26 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2.1-8
- Remove incorrect testcase failing with ant 1.8
- Cleanup whitespace

* Tue Jun 29 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2.1-7
- Updated previous patch to only modify behaviour in JPP mode

* Mon Jun 28 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2.1-6
- Disable parallel artifact resolution

* Wed Jun 23 2010 Yong Yang <yyang@redhat.com> 2.2.1-5
- Add Requires: maven-enforcer-plugin

* Fri Jun 18 2010 Deepak Bhole <dbhole@redhat.com> 2.2.1-4
- Final non-bootstrap build against non-bootstrap maven

* Fri Jun 18 2010 Deepak Bhole <dbhole@redhat.com> 2.2.1-3
- Added buildnumber plugin requirements
- Rebuild in non-bootstrap

* Thu Jun 17 2010 Deepak Bhole <dbhole@redhat.com> - 0:2.2.1-2
- Added support for dumping mapping info (in debug mode)
- Add a custom depmap
- Added empty-dep
- Added proper requirements
- Fixed classworlds jar name used at runtime
- Install individual components
- Install poms and mappings
- Remove non maven items from shaded uber jar
- Create dependency links in $M2_HOME/lib at install time

* Thu Nov 26 2009 Deepak Bhole <dbhole@redhat.com> - 0:2.2.1-1
- Initial bootstrap build
