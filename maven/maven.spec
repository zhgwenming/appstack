%global bootstrap 1
%global debug_package %{nil}

Name:           maven
Version:        3.0.4
Release:        21.2%{?dist}
Summary:        Java project management and project comprehension tool

Group:          Development/Tools
License:        ASL 2.0
URL:            http://maven.apache.org/
# Source URL is for testing only, final version will be in different place:
# http://www.apache.org/dyn/closer.cgi/maven/source/apache-%{name}-%{version}-src.tar.gz
Source0:        http://www.apache.org/dist//maven/source/apache-%{name}-%{version}-src.tar.gz
Source1:        maven-bash-completion
Source2:        mvn.1

# custom resolver java files
# source: git clone git://fedorapeople.org/~sochotni/maven-javadir-resolver/
Source100:      JavadirWorkspaceReader.java
Source101:      MavenJPackageDepmap.java

# empty files for resolving to nothing
Source104:    %{name}-empty-dep.pom
Source105:    %{name}-empty-dep.jar

# 2xx for created non-buildable sources
Source200:    %{name}-script
Source201:    %{name}-script-local
Source202:    %{name}-script-rpmbuild

# Other included files
Source250:    repo-metadata.tar.xz

# Patch1XX could be upstreamed probably
Patch100:       0005-Use-generics-in-modello-generated-code.patch
Patch101:       0006-Make-compiler-plugin-default-to-source-1.5.patch

# Patch15X are already upstream
Patch150:         0001-Add-plugin-api-deps.patch
Patch151:         0003-Use-utf-8-source-encoding.patch
# Patch2XX for non-upstreamable patches
Patch200:       0002-Use-custom-resolver.patch
Patch201:       0004-Fix-text-scope-skipping-with-maven.test.skip.patch

Patch901:       1001-plexus-classworlds-loadpatch-fix.patch

BuildArch:      noarch

%if %{bootstrap}
BuildRequires: ant >= 1.8
%else
BuildRequires:  aether >= 1.13.1
BuildRequires:  aopalliance
BuildRequires:  apache-commons-parent
BuildRequires:  async-http-client
BuildRequires:  atinject
BuildRequires:  buildnumber-maven-plugin
BuildRequires:  cglib
BuildRequires:  google-guice >= 3.0
BuildRequires:  hamcrest
BuildRequires:  maven
BuildRequires:  maven2-common-poms
BuildRequires:  maven-assembly-plugin
BuildRequires:  maven-compiler-plugin
BuildRequires:  maven-install-plugin
BuildRequires:  maven-jar-plugin
BuildRequires:  maven-javadoc-plugin
BuildRequires:  maven-parent
BuildRequires:  maven-resources-plugin
BuildRequires:  maven-site-plugin
BuildRequires:  maven-surefire-plugin
BuildRequires:  maven-surefire-provider-junit4
BuildRequires:  mojo-parent
BuildRequires:  objectweb-asm
BuildRequires:  plexus-containers-component-metadata >= 1.5.5
BuildRequires:  plexus-containers-container-default
BuildRequires:  sisu >= 2.1.1-2
BuildRequires:  slf4j
BuildRequires:  sonatype-oss-parent
BuildRequires:  xmlunit
%endif

%if 0%{?fedora}
BuildRequires:  animal-sniffer >= 1.6-5
%endif

%if !%{bootstrap}
Requires:       aether >= 1.13.1
Requires:       apache-commons-cli
Requires:       apache-commons-parent
Requires:       async-http-client
Requires:       atinject
Requires:       google-guice >= 3.0
Requires:       guava
Requires:       hamcrest
Requires:       hamcrest
Requires:       java >= 1:1.6.0
Requires:       maven2-common-poms
Requires:       maven-parent
Requires:       maven-wagon
Requires:       mojo-parent
Requires:       nekohtml
Requires:       plexus-cipher
Requires:       plexus-classworlds >= 2.4
Requires:       plexus-containers-component-annotations
Requires:       plexus-containers-container-default
Requires:       plexus-interpolation
Requires:       plexus-sec-dispatcher
Requires:       plexus-utils
Requires:       sisu >= 2.1.1-2
Requires:       sonatype-oss-parent
Requires:       xbean
Requires:       xerces-j2
Requires:       yum-utils
%endif

Requires:	xml-commons-apis

%if 0%{?fedora}
Requires:       animal-sniffer >= 1.6-5
%endif


# for noarch->arch change
Obsoletes:      %{name} < 0:%{version}-%{release}

# maven2 bin package no longer exists. Replace it
# these should be around until F20
Obsoletes:      maven2 < 2.2.1-99
Provides:       maven2 = %{version}-%{release}

%description
Maven is a software project management and comprehension tool. Based on the
concept of a project object model (POM), Maven can manage a project's build,
reporting and documentation from a central piece of information.

%package        javadoc
Summary:        API documentation for %{name}
Group:          Documentation
Requires:       jpackage-utils
BuildArch:      noarch

%description    javadoc
%{summary}.

%prep
%setup -q -n apache-%{name}-%{version}%{?ver_add}
#%patch150 -p1
#%patch151 -p1
%patch200 -p1
#%patch201 -p1
#%patch100 -p1
#%patch101 -p1
%patch901 -p1

# get custom resolver in place
mkdir -p maven-aether-provider/src/main/java/org/apache/maven/artifact/resolver \
         maven-aether-provider/src/main/java/org/apache/maven/artifact/repository

cp %{SOURCE100} maven-aether-provider/src/main/java/org/apache/maven/artifact/resolver
cp %{SOURCE101} maven-aether-provider/src/main/java/org/apache/maven/artifact/repository

pushd apache-maven
rm src/bin/*bat
popd

%if ! %{bootstrap}
# by adding our things this has become compile dep
sed -i 's:<scope>runtime</scope>::' maven-core/pom.xml

# not really used during build, but a precaution
rm maven-ant-tasks-*.jar

# fix line endings
sed -i 's:\r::' *.txt

# fix for animal-sniffer (we don't generate 1.5 signatures)
sed -i 's:check-java-1.5-compat:check-java-1.6-compat:' pom.xml

pushd apache-maven
rm src/bin/*bat

sed -i 's:\r::' src/conf/settings.xml

# Update shell scripts to use unversioned classworlds
sed -i -e s:'-classpath "${M2_HOME}"/boot/plexus-classworlds-\*.jar':'-classpath "${M2_HOME}"/boot/plexus-classworlds.jar':g \
        src/bin/mvn*
popd

# Disable animal-sniffer on RHEL
# Temporarily disabled for fedora to solve asm & asm4 clashing on classpath
#if [ %{?rhel} ]; then
%pom_remove_plugin :animal-sniffer-maven-plugin
#fi

%pom_add_dep aopalliance:aopalliance:any:test maven-model-builder
%pom_add_dep cglib:cglib:any:test maven-model-builder

%endif

%build

export M2_REPO=$HOME/m2
export M2_HOME=$(pwd)/m2home/apache-maven-%{version}%{?ver_add}

%if %{bootstrap}
ant -Dmaven.repo.local=$M2_REPO
%else
mvn-rpmbuild -e install javadoc:aggregate
%endif

#mkdir m2home
(cd m2home
#tar --delay-directory-restore -xvf ../apache-maven/target/*tar.gz
#chmod -R +rwX apache-%{name}-%{version}%{?ver_add}
chmod -x apache-%{name}-%{version}%{?ver_add}/conf/settings.xml
)


%install
export M2_HOME=$(pwd)/m2home/apache-maven-%{version}%{?ver_add}

# maven2 directory in /usr/share/java
install -dm 755 $RPM_BUILD_ROOT%{_javadir}/%{name}

# put global m2 config into /etc and symlink it later
install -dm 755 $RPM_BUILD_ROOT%{_sysconfdir}
mv $M2_HOME/bin/m2.conf $RPM_BUILD_ROOT%{_sysconfdir}/

###########
# M2_HOME #
###########
install -dm 755 $RPM_BUILD_ROOT%{_datadir}/%{name}

#################
# Repo metadata #
#################
install -m 755 %{SOURCE250} $RPM_BUILD_ROOT%{_datadir}/%{name}/


###############
# M2_HOME/bin #
###############
install -dm 755 $RPM_BUILD_ROOT%{_datadir}/%{name}/bin
cp -a $M2_HOME/bin/* $RPM_BUILD_ROOT%{_datadir}/%{name}/bin

ln -sf %{_sysconfdir}/m2.conf $RPM_BUILD_ROOT%{_datadir}/%{name}/bin/m2.conf


################
# M2_HOME/boot #
################
install -dm 755 $RPM_BUILD_ROOT%{_datadir}/%{name}/boot

# this dangling symlink will be filled in by Requires
(cd $RPM_BUILD_ROOT%{_datadir}/%{name}/boot
  ln -sf `build-classpath plexus/classworlds` plexus-classworlds.jar
)


################
# M2_HOME/conf #
################
install -dm 755 $RPM_BUILD_ROOT%{_datadir}/%{name}/conf
cp -a $M2_HOME/conf/* $RPM_BUILD_ROOT%{_datadir}/%{name}/conf/

###############
# M2_HOME/lib #
###############
install -dm 755 $RPM_BUILD_ROOT%{_datadir}/%{name}/lib

cp -a $M2_HOME/lib/* $RPM_BUILD_ROOT%{_datadir}/%{name}/lib/

# jdom is needed for our custom resolving code only
(cd $RPM_BUILD_ROOT%{_datadir}/%{name}/lib

#  build-jar-repository -s -p . aether/api aether/connector-wagon aether/impl aether/spi aether/util \
#                               commons-cli guava google-guice nekohtml plexus/plexus-cipher \
#                               plexus/containers-component-annotations  \
#                               plexus/interpolation plexus/plexus-sec-dispatcher plexus/utils \
#                               sisu/sisu-inject-bean sisu/sisu-inject-plexus maven-wagon/file \
#                               maven-wagon/http-lightweight maven-wagon/http-shared maven-wagon/provider-api \
#                               xbean/xbean-reflect xerces-j2 atinject aopalliance cglib \
#                               slf4j/api slf4j/nop objectweb-asm
  # dependency of our resolver
  #mkdir ext/
  #build-jar-repository -s -p ext/ xml-commons-apis
)

################
# M2_HOME/poms #
#*##############
install -dm 755 $RPM_BUILD_ROOT%{_datadir}/%{name}/poms

########################
# /etc/maven/fragments #
########################
install -dm 755 $RPM_BUILD_ROOT/%{_sysconfdir}/maven/fragments

##############################
# /usr/share/java repository #
##############################
install -dm 755 $RPM_BUILD_ROOT%{_datadir}/%{name}/repository
ln -s %{_javadir} $RPM_BUILD_ROOT%{_datadir}/%{name}/repository/JPP

##############################
# /usr/share/java-jni repository #
##############################
install -dm 755 $RPM_BUILD_ROOT%{_datadir}/%{name}/repository-java-jni
ln -s %{_javajnidir} $RPM_BUILD_ROOT%{_datadir}/%{name}/repository-java-jni/JPP

##############################
# _libdir/java repository #
##############################
install -dm 755 $RPM_BUILD_ROOT%{_datadir}/%{name}/repository-jni
# create symlink in post, remove in preun so we can stay noarch

##################
# javadir/maven #
#*################
install -dm 755 $RPM_BUILD_ROOT%{_javadir}/%{name}

#######################
# javadir/maven/poms #
#*#####################
ln -s %{_datadir}/%{name}/poms $RPM_BUILD_ROOT%{_javadir}/%{name}/poms

# for our custom resolver to remove dependencies we need empty jar and
# pom file
install -m 644 %{SOURCE104} $RPM_BUILD_ROOT%{_datadir}/%{name}/poms/JPP.maven-empty-dep.pom
install -m 644 %{SOURCE105} $RPM_BUILD_ROOT%{_javadir}/%{name}/empty-dep.jar

############
# /usr/bin #
############
install -dm 755 $RPM_BUILD_ROOT%{_bindir}

# Wrappers
cp -af %{SOURCE200} $RPM_BUILD_ROOT%{_bindir}/mvn
cp -af %{SOURCE201} $RPM_BUILD_ROOT%{_bindir}/mvn-local
cp -af %{SOURCE202} $RPM_BUILD_ROOT%{_bindir}/mvn-rpmbuild

###################
# Individual jars #
###################

for module in maven-aether-provider maven-artifact maven-compat \
              maven-core maven-embedder maven-model \
              maven-model-builder maven-plugin-api \
              maven-repository-metadata  maven-settings \
              maven-settings-builder;do

    pushd $module
    install -m 644 target/$module-%{version}%{?ver_add}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/$module.jar
    ln -s %{_javadir}/%{name}/$module.jar $RPM_BUILD_ROOT%{_datadir}/%{name}/lib/$module.jar
    install -m 644 pom.xml $RPM_BUILD_ROOT%{_datadir}/%{name}/poms/JPP.%{name}-$module.pom
    %add_to_maven_depmap org.apache.maven $module %{version} JPP/%{name} $module
    popd
done

# maven pom
install -m 644 pom.xml $RPM_BUILD_ROOT%{_datadir}/%{name}/poms/JPP.%{name}-maven.pom
%add_to_maven_depmap org.apache.maven maven %{version} JPP/%{name} maven

# javadocs
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}
#cp -pr target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

# Install bash-completion
install -Dm 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/bash_completion.d/%{name}

# Manual page
install -dm 755 $RPM_BUILD_ROOT%{_mandir}/man1
install -pm 644 %{SOURCE2} $RPM_BUILD_ROOT%{_mandir}/man1
gzip -9 $RPM_BUILD_ROOT%{_mandir}/man1/*

%preun
if [ $1 -eq 0 ] ; then
   if [ -h %{_datadir}/%{name}/repository-jni/JPP ];then
      rm %{_datadir}/%{name}/repository-jni/JPP
   fi
fi

%posttrans
# ugly as hell
ln -sf `rpm --eval '%%{_jnidir}'` %{_datadir}/%{name}/repository-jni/JPP

%files
%doc LICENSE.txt NOTICE.txt README.txt
%attr(0755,root,root) %{_bindir}/mvn
%attr(0755,root,root) %{_bindir}/mvn-local
%attr(0755,root,root) %{_bindir}/mvn-rpmbuild
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/bin
%attr(0755,root,root) %{_datadir}/%{name}/bin/mvn
%attr(0755,root,root) %{_datadir}/%{name}/bin/mvnyjp
%attr(0755,root,root) %{_datadir}/%{name}/bin/mvnDebug
%{_datadir}/%{name}/bin/*.conf
%config(noreplace) %{_sysconfdir}/m2.conf
%{_datadir}/%{name}/boot
%{_datadir}/%{name}/conf
%{_datadir}/%{name}/lib
%{_datadir}/%{name}/poms
%{_datadir}/%{name}/repository
%{_datadir}/%{name}/repository-jni
%{_datadir}/%{name}/repository-java-jni
%config %{_mavendepmapfragdir}/%{name}
%{_javadir}/%{name}
%{_datadir}/%{name}/repo-metadata.tar.xz
%config(noreplace) %{_sysconfdir}/bash_completion.d/%{name}
%{_mandir}/man1/mvn.1.gz

%files javadoc
%doc LICENSE.txt NOTICE.txt
%{_javadocdir}/%{name}


%changelog
* Mon Nov 19 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.4-21.2
- Fix license tag

* Thu Nov 15 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.4-21.1
- Install NOTICE file with javadoc package

* Thu Nov 08 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.4-21
- Add support for custom jar/pom/fragment directories

* Thu Nov  8 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.4-20
- Remove all slf4j providers except nop from maven realm

* Thu Nov  1 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.4-19
- Add aopalliance and cglib to maven-model-builder test dependencies

* Thu Nov  1 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.4-18
- Add objectweb-asm to classpath

* Thu Nov  1 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.4-17
- Add aopalliance, cglib, slf4j to classpath

* Wed Oct 31 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.4-16
- Don't echo JAVA_HOME in maven-script
- Add bash completion for -Dproject.build.sourceEncoding

* Mon Oct 29 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.4-15
- Add a few bash completion goals

* Wed Oct 24 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.4-14
- Enable test skipping patch only for local mode (#869399)

* Fri Oct 19 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.4-13
- Make sure we look for requested pom file and not resolved

* Thu Oct 18 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.4-12
- Look into maven.repo.local first to handle corner-case packages (#865599)
- Finish handling of compatibility packages
- Disable animal-sniffer temporarily in Fedora as well

* Mon Aug 27 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.4-11
- Disable animal-sniffer on RHEL

* Wed Jul 25 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.4-10
- Fix exit code of mvn-rpmbuild outside of mock
- Fix bug in compatibility jar handling

* Mon Jul 23 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.4-9
- Run redundant dependency checks only in mock

* Tue Jul 17 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.4-8
- Add manual page

* Mon Jun 11 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.4-7
- Implement redundant dependency checks

* Thu May 24 2012 Krzysztof Daniel <kdaniel@redhat.com> 3.0.4-6
- Bug 824789 -Use the version if it is possible.

* Mon May 14 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.4-5
- Use Obsoletes instead of Conflicts

* Mon May 14 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.4-4
- Obsolete and provide maven2

* Thu Mar 29 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.4-3
- Make package noarch again to simplify bootstrapping

* Thu Feb  9 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.4-2
- Make javadoc noarch
- Make compilation source level 1.5
- Fix borked tarball unpacking (reason unknown)

* Tue Jan 31 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.4-1
- Update to latest upstream version

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.3-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 13 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.3-16
- Add maven2-common-poms to Requires

* Tue Oct 11 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.3-15
- Provide mvn script now instead of maven2
- Conflict with older versions of maven2

* Tue Aug 30 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.3-14
- Fix test scope skipping

* Mon Aug 22 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.3-13
- Remove unnecessary deps causing problems from lib/
- Add utf-8 source encoding patch

* Thu Jul 28 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.3-12
- Disable debug package creation

* Thu Jul 28 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.3-11
- Change to arch specific since we are using _libdir for _jnidir

* Tue Jul 26 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.3-10
- Add bash completion (#706856)

* Mon Jul  4 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.3-9
- Add resolving from jnidir and java-jni

* Thu Jun 23 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.3-8
- Add maven-parent to BR/R

* Wed Jun 22 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.3-7
- Process fragments in alphabetical order

* Tue Jun 21 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.3-6
- Fix handling of fallback default_poms
- Add empty-dep into maven package to not require maven2 version

* Fri Jun 10 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.3-5
- Process fragments directly instead of maven2-depmap.xml
- Expect fragments in /usr/share/maven-fragments
- Resolve poms also from /usr/share/maven-poms

* Mon Jun  6 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.3-4
- Add help to mvn-rpmbuild and mvn-local (rhbz#710448)

* Tue May 10 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.3-3
- Improve and clean up depmap handling for m2/m3 repos

* Mon Apr 18 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.3-2
- Enable MAVEN_OPTS override in scripts

* Fri Mar  4 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.3-1
- Update to 3.0.3
- Add ext subdirectory to lib

* Tue Mar  1 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.3-0.1.rc1
- Update to 3.0.3rc1
- Enable tests again

* Thu Feb 10 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.2-2
- Added mvn-rpmbuild script to be used in spec files
- mvn-local is now mixed mode (online with javadir priority)
- Changed mvn.jpp to mvn.local

* Fri Jan 28 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0.2-1
- Update to latest version (3.0.2)
- Ignore test failures temporarily

* Wed Jan 12 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0-6
- Fix bug #669034

* Tue Jan 11 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0-5
- Fix bugs #667625 #667614 and #667636
- Install maven metadata so they are not downloaded when mvn is run
- Rename mvn3-local to mvn-local
- Add more comments to resolver patch

* Tue Dec 21 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0-4
- Add fedora local resolver
- Fix quoting of arguments to mvn scripts
- Add javadoc subpackage
- Make jars versionless and remove unneeded clean section

* Wed Dec  1 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0-3
- Remove maven-ant-tasks jar in prep
- Make fragment file as %%config

* Tue Nov 16 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0-2
- Added apache-commons-parent to BR after commons changes

* Tue Oct 12 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0-1
- Initial package with vanilla maven (no jpp mode yet)
