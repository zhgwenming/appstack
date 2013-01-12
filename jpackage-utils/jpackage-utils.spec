# Copyright (c) 2000-2008, JPackage Project
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
%global gcj_support 1

%global distver 1.7
%global section free

%global debug_package %{nil}

Name:           jpackage-utils
Version:        1.7.5
Release:        23%{?dist}
Epoch:          0
Summary:        JPackage utilities
License:        BSD
URL:            http://www.jpackage.org/
BuildArch:      noarch
Source0:        %{name}-%{version}.tar.bz2
Source1:        %{name}-README
Source2:        abs2rel.sh
Patch1:         %{name}-own-mavendirs.patch
Patch2:         %{name}-prefer-jre.patch
Patch3:         %{name}-set-classpath.patch
Patch5:         %{name}-build-classpath-symlink-fix.patch
Patch6:         %{name}-update-maven-depmap.patch
Group:          Utilities

Requires:       coreutils
Requires:       javapackages-tools
Requires:       perl
Requires:       perl(File::Spec)

# for noarch->arch change
Obsoletes:      %{name} < 0:1.7.5-9

%description
Utilities for the JPackage Project <http://www.jpackage.org/>.

It contains also the License, man pages, documentation, XSL files of general
use with maven2, a header file for spec files, etc. Please See
the %{_docdir}/%{name}-%{version}/%{name}-README file for more
information.

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch5 -p1
%patch6

cp -p %{SOURCE1} %{SOURCE2} .

%build
echo "JPackage release %{distver} (%{distribution}) for %{buildarch}" \
 > etc/jpackage-release


%install
# Pull macros out of macros.jpackage and emulate them during install for
# smooth bootstrapping experience.
for dir in \
    jvmdir jvmjardir jvmprivdir \
    jvmlibdir jvmdatadir jvmsysconfdir \
    jvmcommonlibdir jvmcommondatadir jvmcommonsysconfdir \
    javadir jnidir javadocdir mavenpomdir \
    mavendepmapdir mavendepmapfragdir; do
  export _${dir}=$(rpm --eval $(%{__grep} -E "^%_${dir}\b" \
    misc/macros.jpackage | %{__awk} '{ print $2 }'))
done

install -dm 755 ${RPM_BUILD_ROOT}%{_bindir}
install -dm 755 ${RPM_BUILD_ROOT}%{_sysconfdir}/{java,rpm}
%if %{gcj_support}
install -dm 755 ${RPM_BUILD_ROOT}%{_sysconfdir}/java/security
install -dm 755 ${RPM_BUILD_ROOT}%{_sysconfdir}/java/security/security.d
%endif
install -dm 755 ${RPM_BUILD_ROOT}${_jvmdir}
install -dm 755 ${RPM_BUILD_ROOT}${_jvmjardir}
install -dm 755 ${RPM_BUILD_ROOT}${_jvmprivdir}
install -dm 755 ${RPM_BUILD_ROOT}${_jvmlibdir}
install -dm 755 ${RPM_BUILD_ROOT}${_jvmdatadir}
install -dm 755 ${RPM_BUILD_ROOT}${_jvmsysconfdir}
install -dm 755 ${RPM_BUILD_ROOT}${_jvmcommonlibdir}
install -dm 755 ${RPM_BUILD_ROOT}${_jvmcommondatadir}
install -dm 755 ${RPM_BUILD_ROOT}${_jvmcommonsysconfdir}
install -dm 755 ${RPM_BUILD_ROOT}${_javadir}
install -dm 755 ${RPM_BUILD_ROOT}${_javadir}-utils
install -dm 755 ${RPM_BUILD_ROOT}${_javadir}-ext
install -dm 755 ${RPM_BUILD_ROOT}${_javadir}-{1.5.0,1.6.0,1.7.0}
install -dm 755 ${RPM_BUILD_ROOT}${_jnidir}
install -dm 755 ${RPM_BUILD_ROOT}${_jnidir}-ext
install -dm 755 ${RPM_BUILD_ROOT}${_jnidir}-{1.5.0,1.6.0,1.7.0}
install -dm 755 ${RPM_BUILD_ROOT}${_javadocdir}
install -dm 755 ${RPM_BUILD_ROOT}${_mavenpomdir}
install -dm 755 ${RPM_BUILD_ROOT}${_mavendepmapdir}
install -dm 755 ${RPM_BUILD_ROOT}${_mavendepmapfragdir}

install -pm 755 bin/* ${RPM_BUILD_ROOT}%{_bindir}
install -pm 644 etc/font.properties ${RPM_BUILD_ROOT}%{_sysconfdir}/java

# Install abs2rel scripts
install -pm 755 abs2rel.sh  ${RPM_BUILD_ROOT}%{_javadir}-utils

# Create an initial (empty) depmap
echo -e "<dependencies>\\n" \
  > ${RPM_BUILD_ROOT}${_mavendepmapdir}/maven2-depmap.xml
echo -e "</dependencies>\\n" \
  >> ${RPM_BUILD_ROOT}${_mavendepmapdir}/maven2-depmap.xml

cat > etc/java.conf << EOF
# System-wide Java configuration file                                -*- sh -*-
#
# JPackage Project <http://www.jpackage.org/>

# Location of jar files on the system
JAVA_LIBDIR=${_javadir}

# Location of arch-specific jar files on the system
JNI_LIBDIR=${_jnidir}

# Root of all JVM installations
JVM_ROOT=${_jvmdir}

# You can define a system-wide JVM root here if you're not using the
# default one.
#
# If you have the a base JRE package installed
# (e.g. java-1.6.0-openjdk):
#JAVA_HOME=\$JVM_ROOT/jre
#
# If you have the a devel JDK package installed
# (e.g. java-1.6.0-openjdk-devel):
#JAVA_HOME=\$JVM_ROOT/java

# Options to pass to the java interpreter
JAVACMD_OPTS=
EOF

install -pm 644 etc/java.conf ${RPM_BUILD_ROOT}%{_sysconfdir}/java
install -pm 644 etc/jpackage-release ${RPM_BUILD_ROOT}%{_sysconfdir}/java
install -pm 644 java-utils/* ${RPM_BUILD_ROOT}${_javadir}-utils
install -pm 644 misc/macros.jpackage ${RPM_BUILD_ROOT}%{_sysconfdir}/rpm
%{__mkdir_p} ${RPM_BUILD_ROOT}%{_mandir}/man1
install -pm 644 man/* ${RPM_BUILD_ROOT}%{_mandir}/man1
%{__mkdir_p} ${RPM_BUILD_ROOT}${_javadir}-utils/xml
install -pm 644 xml/* ${RPM_BUILD_ROOT}${_javadir}-utils/xml


cat <<EOF > %{name}-%{version}.files
%{_bindir}/*
%{_mandir}/man1/*
%dir %{_sysconfdir}/java
%if %{gcj_support}
%{_sysconfdir}/java/security
%endif
%dir ${_jvmdir}
%dir ${_jvmjardir}
%dir ${_jvmprivdir}
# %dir ${_jvmlibdir}
%dir ${_jvmdatadir}
%dir ${_jvmsysconfdir}
%dir ${_jvmcommonlibdir}
%dir ${_jvmcommondatadir}
%dir ${_jvmcommonsysconfdir}
%dir ${_javadir}
%dir ${_javadir}-*
%dir ${_jnidir}
%dir ${_jnidir}-*
%dir ${_javadocdir}
%dir ${_mavenpomdir}
%dir ${_mavendepmapdir}
%dir ${_mavendepmapfragdir}
${_javadir}-utils/*
%config %{_sysconfdir}/java/jpackage-release
%config(noreplace) %{_sysconfdir}/java/java.conf
%config(noreplace) %{_sysconfdir}/java/font.properties
%config(noreplace) %{_sysconfdir}/rpm/macros.jpackage
%config(noreplace) ${_mavendepmapdir}/maven2-depmap.xml
EOF

%files -f %{name}-%{version}.files
%doc %{name}-README LICENSE.txt HEADER.JPP doc/* etc/httpd-javadoc.conf


%changelog
* Thu Dec 20 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.7.5-23
- Set JAVA_HOME using java (not javac) location if _prefer_jre is true
- Resolves: rhbz#642035

* Thu Dec 13 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.7.5-22
- Make JNI directories arch independent and go back to noarch
- Reimplement abs2rel.sh using perl File::Spec module
- Reimplement %%update_maven_depmap as NOOP
- Resolves: rhbz#882537
- Resolves: rhbz#823669
- Resolves: rhbz#882578

* Tue Dec 11 2012 Deepak Bhole <dbhole@redhat.com> 1.7.5-21
- rhbz#862001: Updated patches to java-functions so that no .orig is produced

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.7.5-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 09 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.7.5-19
- Rebuilt to make sure upgrade path works

* Fri May 25 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.7.5-18
- Fix build-classpath ignoring symlinks in subdirs

* Wed Feb 15 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.7.5-17
- Remove bundled javapackages and Require separate package

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.7.5-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Sep 15 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.7.5-15
- Strip whitespace when generating fragments
- Fixes in OSGI provides/requires generator

* Fri Aug 26 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.7.5-14
- Check existence of jar file before creating depmap
- Add support for additional jar directories

* Tue Jul 19 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.7.5-13
- Fixed pom directory in javapackages

* Thu Jul  7 2011 Ville Skyttä <ville.skytta@iki.fi> - 0:1.7.5-12
- Own the /usr/lib/rpm/fileattrs dir.

* Tue Jul  5 2011 Ville Skyttä <ville.skytta@iki.fi> - 0:1.7.5-11
- Disable empty -debuginfo package.

* Mon Jul  4 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.7.5-10
- Add javajnidir resolving to build-classpath script family

* Mon Jul  4 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.7.5-9
- Change jnidir to libdir/java (see #665576)
- Add javajnidir macro definition
- Package is now architecture-specific because of _libdir use

* Wed Jun 29 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.7.5-8
- Change pom and fragment directories to /usr/share
- Improved error handing in add_maven_depmap
- Improved osgi bundle provides generation
- Addd osgi requires generator (disabled for now)
- Remove old source files

* Thu Jun 23 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.7.5-7
- Update javapackages to 0.2.2 - fix rpm macro expansion problems

* Wed Jun 22 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.7.5-6
- Update javapackages macros to 0.2.1 - fix add_maven_depmap macro problems

* Fri Jun  3 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.7.5-5
- Guidelines fixes (buildroot def, cleaning etc)
- Add fedora specific extension macros including depgenerators

* Tue May 31 2011 Alexander Kurtakov <akurtako@redhat.com> 0:1.7.5-4.14
- Proper osgi attr file.

* Tue May 31 2011 Alexander Kurtakov <akurtako@redhat.com> 0:1.7.5-4.13
- Add OSGi provides generator.

* Fri Apr 15 2011 Alexander Kurtakov <akurtako@redhat.com> 0:1.7.5-4.12
- Update to current guidelines.
- Drop patch enabling gcj_support macro by default.
- Don't install ${_javadir}-{1.3.1,1.4.0,1.4.1,1.4.2} and ${_jnidir}-{1.3.1,1.4.0,1.4.1,1.4.2}.
- Add mvn(groupId:artifactId) provides generator.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.7.5-4.11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jun 28 2010 Deepak Bhole <dbhole@redhat.com> - 0:1.7.5-3.11
- Fix rhbz# 472800, patch from  Adam Goode: Handle classpaths with spaces

* Tue May  4 2010 Michel Salim <salimma@fedoraproject.org> - 0:1.7.5-3.10
- Add Lua abs2rel script

* Fri Apr 30 2010 Deepak Bhole <dbhole@redhat.com> - 0:1.7.5-3.9
- Stopgap fix for rhbz#461683 from Ville Skyttä.

* Mon Sep 21 2009 Orion Poplawski <orion@cora.nwra.com> - 0:1.7.5-3.8
- Add Requires: coreutils because we provide scripts that are being executed
  in rpm %%post scriptlets that require it.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.7.5-3.7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Mar 31 2009 Deepak Bhole <dbhole@redhat.com> - 0:1.7.5-2.7
- rhbz# 225950. Shortened description, moved it to a README

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.7.5-2.6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Sep 24 2008 Deepak Bhole <dbhole@redhat.com> 1.7.5-1.6
- Update enable-gcj-support.patch to remove fuzz.

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.7.5-1.5
- drop repotag
- fix license tag

* Tue Jul 08 2008 Deepak Bhole <dbhole@redhat.com> 1.7.5-1jpp.4
- Update some macros to be based on other system macros.

* Mon Jul 07 2008 Deepak Bhole <dbhole@redhat.com> 1.7.5-1jpp.3
- Own mavendepmapfragdir as well.

* Mon Jul 07 2008 Deepak Bhole <dbhole@redhat.com> 1.7.5-1jpp.2
- Add ownership of maven directories

* Wed Apr  2 2008 Thomas Fitzsimmons <fitzsim@redhat.com> - 0:1.7.5-1jpp.1
- Import jpackage-utils 1.7.5-1jpp.
- Update IcedTea references to OpenJDK.
- Resolves: rhbz#440092

* Tue Apr  1 2008 Ville Skyttä <ville.skytta@iki.fi> - 0:1.7.5-1jpp
- Workaround a possible sed bug (or my misunderstanding of it?) in
  find_jvm unversioned fallback code.

* Tue Jan 22 2008 Thomas Fitzsimmons <fitzsim@redhat.com> - 0:1.7.4-2jpp.2
- Replace GCJ security directory.

* Tue Jan 22 2008 Thomas Fitzsimmons <fitzsim@redhat.com> - 0:1.7.4-2jpp.1
- Import jpackage-utils 1.7.4-2jpp.

* Mon Jan 21 2008 Thomas Fitzsimmons <fitzsim@redhat.com> - 0:1.7.3-1jpp.4
- Remove AutoReqProv.
- Remove Requires and BuildRequires.
- Wrap export, install and maven lines at 80 columns.
- Add jre option to java.conf comment.
- Related: rhbz#428520
- Remove commented jpackage.org sections.
- Remove duplicate files from files list.
- Remove trailing whitespace.
- Remove rebuild-security-providers.
- Resolves: rhbz#260161

* Fri Jan 04 2008 Ralph Apel <r.apel at r-apel.de> - 0:1.7.4-2jpp
- Fix Bug 293

* Wed Dec 19 2007 Ville Skyttä <ville.skytta@iki.fi> - 0:1.7.4-1jpp
- Terminate functions with %%{nil} in macros.jpackage.
- Make %%jpackage_script install the script with 0755 permissions.
- Use exec in java-functions' run().

* Wed Jun 20 2007 Thomas Fitzsimmons <fitzsim@redhat.com> - 0:1.7.3-1jpp.3
- Add 1.7.0 directories.

* Fri May 25 2007 Jason Corley <jason.corley@gmail.com> - 0:1.7.3-2jpp
- change distribution and vendor to macros
- rebuild in mock

* Thu Jan 11 2007 Thomas Fitzsimmons <fitzsim@redhat.com> - 0:1.7.3-1jpp.2
- Add 1.6.0 directories missed in merge.
- Resolves: rhbz#221262

* Mon Dec 11 2006 Thomas Fitzsimmons <fitzsim@redhat.com> - 0:1.7.3-1jpp.1
- Import version 0:1.7.3-1jpp from jpackage.org.
- Change release numbering format to Xjpp.Y.fc7.
- Resolves: rhbz#218936

* Sat Nov 11 2006 Ville Skyttä <ville.skytta@iki.fi> - 0:1.7.3-1jpp
- Add Java 1.6.0 dirs.

* Mon Oct 23 2006 Deepak Bhole <dbhole@redhat.com> 1.7.2-1jpp
- Added maven2 depmap related macros.

* Tue Sep 19 2006 Fernando Nasser <fnasser@jpackage.org> 0:1.7.1-1jpp
- Add new scripts from Deepak Bhole
- Add documentation from Jason Corley
- Add XLT file shared by maven2 packages

* Fri Nov 04 2005 Fernando Nasser <fnasser@jpackage.org> 0:1.7.0-1jpp
- Initial 1.7 release (eq. to 1.6.6)
- Add Copyright notice and license as header

* Sun Sep 18 2005 David Walluck <david@jpackage.org> 0:1.6.6-1jpp
- always define macros

* Sat Sep 17 2005 David Walluck <david@jpackage.org> 0:1.6.5-2jpp
- clean tarball

* Sat Sep 17 2005 David Walluck <david@jpackage.org> 0:1.6.5-1jpp
- fix conditional macros
- merge nim's and robert's changes

* Mon Aug 22 2005 David Walluck <david@jpackage.org> 0:1.6.4-1jpp
- long needed s/All/Some in error messages

* Fri Jan 28 2005 Nicolas Mailhot <nim at jpackage.org> - 0:1.6.3-1jpp
- prefer full JVM to JRE when not specified (my bad, sorry)
- remove LICENSE.txt as it does not seem to exist in the jpp16 branch anymore

* Sat Jan 15 2005 Nicolas Mailhot <nim at jpackage.org> - 0:1.6.2-1jpp
- Happy new year jpackagers!
- No longer define JAVA_HOME in default shipped java.conf (me)
- Search if $JVM_ROOT/jre or $JVM_ROOT/java exist in functions if JAVA_HOME is
  not defined in java.conf (me)
- Source ~/.java/java.conf in addition to /etc/java/java.conf in functions
  (me)
- Make find-jar use the same error code as build-classpath (Joe Wortmann)
  (note however find-jar was never intended to use directly in scripts, it's
   a low-level way to test the search engine)
- Change macros slightly so they no longer wreak havoc on x86_64 systems
  (Thomas Fitzsimmons for Red Hat)
  This is probably only a short-term fix since we've yet to decide how to
  handle real x86_64 JVMs cleanly.

* Thu Dec 16 2004 Robert Ottenhag <support@bea.com> -  0:1.6.3-1jpp
- Move the systemPrefs stuff into a separate new package java-systemprefs

* Wed Dec 15 2004 Robert Ottenhag <support@bea.com> -  0:1.6.2-1jpp
- Reapply all updates from 1.5.40-1jpp o 1.5.42-1jpp
  + Add support for splitting the installation of Java VMs/SDK/JREs
    according to FHS 2.3 in its architecture dependent, architecture
    independent, and configuration parts. Added new macros and dirs
    - %%{_jvmlibdir}, defined as %%{_libdir}/jvm, equal to %%{_jvmdir},
    - %%{_jvmdatadir}, defined as %%{_datadir}/jvm
    - %%{_jvmsysconfdir}, defined as %%{_sysconfdir}/jvm
  + Add support for splitting the installation of Java VMs/SDK/JREs
    in its common architecture dependent, architecture
    independent, and configuration parts. Added new macros and dirs
    - %%{_jvmcommonlibdir}, defined as %%{_libdir}/jvm-commmon
    - %%{_jvmcommondatadir}, defined as %%{_datadir}/jvm-commmon
    - %%{_jvmcommonsysconfdir}, defined as %%{_sysconfdir}/jvm-commmon
  + Ensure that a global systemPrefs database used by
    java.util.prefs.FileSystemPreferences exists at
    /etc/.java/.systemPrefs, or create an empty one if not, and
    symlink to it from %%{_jvmcommonsysconfdir}/java/jre/systemprefs.

* Sat Dec  4 2004 Ville Skyttä <ville.skytta@iki.fi> - 0:1.6.1-1jpp
- java-functions (set_jvm_dirs): try "java -fullversion" before
  "java -version" for performance, improve regexps, use sed from $PATH.
- Include correct specfile in tarball.

* Tue Nov 2 2004 Nicolas Mailhot <nim@jpackage.org> - 0:1.6.0-2jpp
- fix missing %%{_jnidir} in file list

* Tue Oct 12 2004 Ville Skyttä <ville.skytta@iki.fi> - 0:1.6.0-1jpp
- Start preparing for JPackage 1.6:
  - License change: jpackage-utils >= 1.6.0 is available under the (BSD-like)
    JPackage License.  See included LICENSE.txt.
  - Remove support for Java < 1.4 (dirs only for now).
  - Remove java_home.list and support for it.
- Add support for installing macros.jpackage into Asianux's rpm config,
  thanks to Robert Ottenhag for the info.

* Sun Aug 23 2004 Randy Watler <rwatler at finali.com> - 0:1.5.38-2jpp
- Rebuild with ant-1.6.2

* Mon Jun  7 2004 Ville Skyttä <ville.skytta@iki.fi> - 0:1.5.38-1jpp
- Update java_home.list with Sun's default 1.5.0beta2 location.
- Nuke extra copy of java.conf from tarball.

* Wed May 26 2004 Nicolas Mailhot <Nicolas.Mailhot at laPoste.net> - 0:1.5.37-1jpp
- add the --preserve-naming switch to build-jar-repository, and document it
  (following a discussion with Chip Turner)

* Thu May  6 2004 Ville Skyttä <ville.skytta@iki.fi> - 0:1.5.36-1jpp
- Fix bootstrap problem by ensuring that build time macro expansion for
  %%{_sysconfdir}/java.conf uses macros defined in this package and does not
  rely on the macros being already defined.
- Include correct spec file in tarball.

* Tue May 04 2004 David Walluck <david@jpackage.org> 0:1.5.35-1jpp
- expand macros in %%{_sysconfdir}/java.conf

* Fri Mar 26 2004 Ville Skyttä <ville.skytta@iki.fi> - 0:1.5.34-1jpp
- Update java_home.list with Sun's default 1.4.2_04, 1.4.1_07, 1.3.1_10
  and 1.3.1_11 locations.

* Tue Feb 09 2004 David Walluck <david@anti-microsoft.org> 0:1.5.33-1jpp
- update for J2SE 1.5.0 Beta 1

* Tue Jan 13 2004 Ville Skyttä <ville.skytta@iki.fi> - 0:1.5.32-1jpp
- Fix java-functions location in diff-jars.
- Add (X)Emacs mode cookies to java.conf and java-functions.
- Micro-performance improvement to set_javacmd.
- Insert macros.jpackage before anything starting with "~/" in rpmrc's.
- Include example httpd.conf snippet for javadocs.

* Mon Dec 29 2003 Ville Skyttä <ville.skytta@iki.fi> - 0:1.5.31-1jpp
- Update java_home.list with Sun's default 1.4.2_03, 1.4.1_06 and 1.4.0_04
  locations.

* Thu Nov 13 2003 Nicolas Mailhot <Nicolas.Mailhot at laPoste.net> - 0:1.5.30-1jpp
- Add a minimalist xfonset entry to the default font.properties

* Tue Oct 21 2003 Ville Skyttä <ville.skytta@iki.fi> - 0:1.5.29-1jpp
- Update java_home.list with Sun's default 1.4.2_02 and 1.4.1_05 locations.

* Fri Oct 17 2003 Ville Skyttä <ville.skytta@iki.fi> - 0:1.5.28-1jpp
- Make package bootstrappable, thanks to Markus Pilzecker for ideas.

* Sun Aug 31 2003 Ville Skyttä <ville.skytta@iki.fi> - 0:1.5.27-1jpp
- Update jpackage-1.5-policy wrt. jvm-private and speling fixxes.

* Sat Aug 30 2003 Ville Skyttä <ville.skytta@iki.fi> - 0:1.5.26-1jpp
- Add %%{_jvmprivdir} (== %%{_libdir}/jvm-private), a directory for
  JVM-private stuff (eg. JCE policy jars).
- Update java_home.list with Sun's default 1.4.2_01 location.

* Thu Aug 14 2003 Ville Skyttä <ville.skytta@iki.fi> - 0:1.5.25-1jpp
- Update java_home.list.
- Save .spec in UTF-8.

* Tue Jun 10 2003 Nicolas Mailhot <Nicolas.Mailhot at laPoste.net> 0:1.5.24-1jpp
- fix more symlinks/copy corner cases

* Tue Jun 10 2003 Nicolas Mailhot <Nicolas.Mailhot at laPoste.net> 0:1.5.23-1jpp
- debug 1.5.22

* Tue Jun 10 2003 Nicolas Mailhot <Nicolas.Mailhot at laPoste.net> 0:1.5.22-1jpp
- more correct java version detection regexp, courtesy of Scott Brickner
- allow creation of harlink/copy jar repositories since tomcat4 seems to need
  this (reported by Greg Barton)

* Sun May 18 2003 Nicolas Mailhot <Nicolas.Mailhot at laPoste.net> 0:1.5.21-1jpp
- fix a bug in jar repository handling
- remove unused APPDIR in jar resolution
- add doc for jpackage 1.5 policy

* Tue May 16 2003 Nicolas Mailhot <Nicolas.Mailhot at laPoste.net> 0:1.5.20-1jpp
- remove unneeded and brittle complexity

* Tue May 13 2003 Nicolas Mailhot <Nicolas.Mailhot at laPoste.net> 0:1.5.19-1jpp
- fix new jar repository scripts (more corner cases)
- create symlinks for not-found extensions to allow a later repository rebuild
- create symlinks as [extension].jar, for example [jsse][jcert].jar
- allow both extension split and collapsing
  (one jar -> one directory of jars or the other way round)

* Tue May 13 2003 Nicolas Mailhot <Nicolas.Mailhot at laPoste.net> 0:1.5.18-1jpp
- fix new scripts

* Tue May 13 2003 Nicolas Mailhot <Nicolas.Mailhot at laPoste.net> 0:1.5.17-1jpp
- add initial java repository support

* Sat May 10 2003 David Walluck <david@anti-microsoft.org> 0:1.5.16-1jpp
- %%jpackage_script macro fix
- add %%doc to file list
- add %%config(noreplace) to jpackage-release in file list to shut up rpmlint

* Wed May 7 2003 Nicolas Mailhot <Nicolas.Mailhot at laPoste.net> 0:1.5.15-1jpp
- fix error message in java dir computation

* Sun Apr 26 2003 Nicolas Mailhot <Nicolas.Mailhot at laPoste.net> 0:1.5.14-3jpp
- use java fonts if available first

* Sat Apr 26 2003 Nicolas Mailhot <Nicolas.Mailhot at laPoste.net> 0:1.5.14-1jpp
- add java font config

* Wed Apr 23 2003 David Walluck <david@anti-microsoft.org> 0:1.5.13-5jpp
- use quotes in 'test -f'

* Mon Apr 21 2003 David Walluck <david@anti-microsoft.org> 0:1.5.13-4jpp
- use hardcoded file list for %%postun and %%triggerin

* Thu Apr 17 2003 David Walluck <david@anti-microsoft.org> 0:1.5.13-3jpp
- don't use quotes around the 'find' command in %%postun and %%triggerin
- don't add a 'macrofiles:' line in %%triggerin to rpmrc if one isn't
  already there

* Tue Apr 15 2003 David Walluck <david@anti-microsoft.org> 0:1.5.13-2jpp
- try to support macros.jpackage on RedHat 9

* Mon Apr 14 2003 David Walluck <david@anti-microsoft.org> 0:1.5.13-1jpp
- change CLASSPATH to _CLASSPATH and JARS to _JARS
- clean up trailing ':' in _CLASSPATH

* Mon Apr 14 2003 Nicolas Mailhot <Nicolas.Mailhot at laPoste.net> 0:1.5.12-1jpp
- remove build-classpath dependency on David's stuff since it fails horribly
  when people actually use it
- try to actually fix triggers

* Sat Apr 12 2003 David Walluck <david@anti-microsoft.org> 0:1.5.11-3jpp
- don't remove macros.jpackage from rpmrc on jpackage-utils upgrade

* Sat Apr 12 2003 David Walluck <david@anti-microsoft.org> 0:1.5.11-2jpp
- remove argouml.log from tarball

* Fri Apr 11 2003 David Walluck <david@anti-microsoft.org> 0:1.5.11-1jpp
- add build-classpath-directory
- add epoch

* Thu Apr 10 2003 David Walluck <david@anti-microsoft.org> 1.5.10-1jpp
- back to using %%{_libdir}/rpm/rpmrc for macros.jpackage
- add %%{_javadir}--1.4.2 and %%{_jnidir}-1.4.2 directories
- update package description
- add JAVACMD_OPTS to java.conf
- use new external java.conf
- update build-classpath and java-functions to support directories in
  CLASSPATH

* Mon Mar 24 2003 Nicolas Mailhot <Nicolas.Mailhot@jpackage.org> 1.5.9-1jpp
- more symlinks handling

* Wed Mar 19 2003 Nicolas Mailhot <Nicolas.Mailhot@jpackage.org> 1.5.7-1jpp
- register new jvm alternatives
- allow use of build-classpath for incomplete paths

* Tue Mar 11 2003 Nicolas Mailhot <Nicolas.Mailhot@jpackage.org> 1.5.6-1jpp
- resurect borked icon/menu handling
- hopefuly support jni jars (arch-dependant jars)

* Thu Feb 13 2003 Nicolas Mailhot <Nicolas.Mailhot@jpackage.org> 1.5.4-3jpp
- extract jar resolving logic from classpath builder
- hopefully integrate classpath builder in set_classpath macro

* Wed Feb 12 2003 Nicolas Mailhot <Nicolas.Mailhot@jpackage.org> 1.5.3-1jpp
- add classpath builder

* Wed Feb 12 2003 Nicolas Mailhot <Nicolas.Mailhot@jpackage.org> 1.5.2-1jpp
- New reorg

* Tue Feb 11 2003 Nicolas Mailhot <Nicolas.Mailhot@jpackage.org> 1.5.1-1jpp
- add some extension handling
- fix some macros broken in 1.5.0

* Tue Feb 11 2003 Nicolas Mailhot <Nicolas.Mailhot@jpackage.org> 1.5.0-1jpp
- use a tar source file
- use lsb locations
- prepare for multi-jvm extensions support

* Mon Feb 10 2003 David Walluck <david@anti-microsoft.org> 1.4.8-1jpp
- better installation of macros
- update %%description to list all files currently included in this package
- jpackage-release in %%{_sysconfdir}, not /etc (I hope this is more
  correct)

* Sun Feb 09 2003 David Walluck <david@anti-microsoft.org> 1.4.7-1jpp
- fix sed in %%jpackage_script when paths to jars contain '/'
- fix typo in macros documentation
- add jpackage-policy
- add jpackage-release

* Wed Feb 05 2003 David Walluck <david@anti-microsoft.org> 1.4.6-1jpp
- macro bugfixes
- instead of tarball we now use %%{SOURCEn} format

* Fri Jan 31 2003 David Walluck <david@anti-microsoft.org> 1.4.5-1jpp
- add macros.jpackage (DO NOT attempt to use this until we figure something
  out, but I would still like to get some feedback about how it looks so far)

* Sun Jan 26 2003 David Walluck <david@anti-microsoft.org> 1.4.4-1jpp
- fix exiting on failed `which` (Ville Skyttä <ville.skytta@iki.fi>)

* Sun Jan 26 2003 David Walluck <david@anti-microsoft.org> 1.4.3-2jpp
- fix release tag in %%changelog

* Sun Jan 26 2003 David Walluck <david@anti-microsoft.org> 1.4.3-1jpp
- java-functions changes:
  + set_jvm: look for javac first to avoid erroneously setting
    JAVA_HOME to the location of the jre unless we have to
  + set_jvm: follow symlinks to avoid erroneously setting JAVA_HOME to
    /usr/bin
  + set_jvm: export JAVA_HOME
- changed to use install instead of mkdir and cp
- remove %%attr and rely on install to set the permissions instead

* Sat Jan 25 2003 Ville Skyttä <ville.skytta@iki.fi> - 1.4.2-1jpp
- java-functions changes:
  + Prevent non-success exit code from "which" in set_jvm, it can now
    be used when building RPMs.
  + Use set_jvm in set_javacmd.
  + Use set_javacmd and $JAVACMD in run.
- Fix Group tag.

* Sat Dec 28 2002 Ville Skyttä <ville.skytta@iki.fi> - 1.4.1-1jpp
- Add Sun's 1.4.0_03 and BEA JRockit 7.0SP1 default RPM locations.

* Thu Nov 21 2002 Ville Skyttä <ville.skytta@iki.fi> - 1.4-1jpp
- Fix diff-jars when diffing 2 jars with same basename (#635202).
- Add IBM's 1.4 default RPM location to jvm.list.

* Fri Nov  8 2002 Ville Skyttä <ville.skytta@iki.fi> - 1.3-6jpp
- Add Sun's 1.3.1_06 default RPM location.

* Sat Oct 19 2002 Ville Skyttä <ville.skytta@iki.fi> 1.3-5jpp
- Add Sun's 1.4.1_01 and 1.3.1_05 default RPM locations.

* Tue Sep 17 2002 Ville Skyttä <ville.skytta@iki.fi> 1.3-4jpp
- Add Sun's 1.4.1 default rpm location.

* Thu Sep 12 2002 Ville Skyttä <ville.skytta@iki.fi> 1.3-3jpp
- Add Sun's 1.4.0_02 and new BEA JRockit locations.

* Sat Jun 29 2002 Ville Skyttä <ville.skytta@iki.fi> 1.3-2jpp
- Add section macro.

* Sat Jun 29 2002 Ville Skyttä <ville.skytta@iki.fi> 1.3-1jpp
- Add some variants of Sun J2SE java homes as well as JRockit.
- Add Distribution tag.

* Fri May 3 2002 Nicolas Mailhot <nmailhot@users.sourceforge.net> 1.2-1jpp
Add some stuff to please jakarta ant developpers :
- OSX java home
- new function set_javacmd with AIX hack included

* Wed Dec 19 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.1-1jpp
- java-functions: centralized configuration
- java-functions: jvm list lookup
- diff-jars: fixed typo
- diff-jars: used /tmp for files
- corrected changelog

* Sat Dec 1 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.0-1jpp
- first JPackage release
