%define profile_d_dir %{_sysconfdir}/profile.d
%define maven_name maven2
%define prj_javadir %{_javadir}/%{name}
%define prj_datadir %{_datadir}/%{name}
Name:           apache-maven
Version:        3.0.4
Release:        2%{?dist}
Summary:        Java project management and project comprehension tool binary
Epoch:          0

Group:          Development/Tools
License:        ASL 2.0 and MIT and BSD
URL:            http://maven.apache.org/

Source0:        http://www.apache.org/dyn/closer.cgi/maven/binaries/%{name}-%{version}-bin.tar.gz
Source15:       %{name}-jpp-script
Source16:       mvn-rpmbuild

BuildArch: noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: java-devel >= 1:1.6.0
BuildRequires:  jpackage-utils
BuildRequires:  grep

# maven 3 seems require javac
Requires:  java-devel >= 1:1.6.0
Requires:  jpackage-utils
Provides:  maven

%description
Maven is a software project management and comprehension tool. Based on the
concept of a project object model (POM), Maven can manage a project's build,
reporting and documentation from a central piece of information.

Note that this package is binary version, thus cannot go in official
Fedora repo.

%prep
%setup -q
%{__sed} -i 's/\r//' LICENSE.txt
%{__sed} -i 's/\r//' NOTICE.txt
%{__sed} -i 's/\r//' README.txt

%build

%install
%__rm -rf $RPM_BUILD_ROOT

%__mkdir -p $RPM_BUILD_ROOT/%{prj_datadir}/bin
%__mkdir -p $RPM_BUILD_ROOT/%{_bindir}/bin
%__install -pm 644 bin/m2.conf $RPM_BUILD_ROOT/%{prj_datadir}/bin
%__install -pm 755 bin/mvn $RPM_BUILD_ROOT/%{prj_datadir}/bin
%__install -pm 755 bin/mvnDebug $RPM_BUILD_ROOT/%{prj_datadir}/bin
%__install -pm 755 %{SOURCE15} $RPM_BUILD_ROOT/%{prj_datadir}/bin/mvn-jpp
%__install -pm 755 bin/mvnyjp  $RPM_BUILD_ROOT/%{prj_datadir}/bin
%__install -pm 755 %{SOURCE16} $RPM_BUILD_ROOT%{_bindir}/mvn-rpmbuild

%__cp -R boot $RPM_BUILD_ROOT/%{prj_datadir}
%__mkdir -p $RPM_BUILD_ROOT/%{prj_datadir}/conf
%__install -pm 644 conf/settings.xml $RPM_BUILD_ROOT/%{prj_datadir}/conf
%__cp -R lib $RPM_BUILD_ROOT/%{prj_datadir}
%__mkdir -p $RPM_BUILD_ROOT/%{prj_javadir}
for jFile in %{prj_datadir}/lib/*.jar; do
# package name
    PNAME=`basename $jFile | sed -e 's/^\([A-Za-z-]*\)-\([0-9].*\)\.jar/\1/'`
    %__ln_s $jFile $RPM_BUILD_ROOT/%{prj_javadir}/$PNAME.jar
done

%__mkdir -p $RPM_BUILD_ROOT/%{profile_d_dir}
%__cat >>$RPM_BUILD_ROOT/%{profile_d_dir}/apache-maven.sh <<EOF
MAVEN_HOME=%{prj_datadir}
M2_HOME=\$MAVEN_HOME
PATH=\$MAVEN_HOME/bin:\$PATH
export MAVEN_HOME
export M2_HOME
export PATH
EOF

%__cat >>$RPM_BUILD_ROOT/%{profile_d_dir}/apache-maven.csh <<EOF
setenv MAVEN_HOME %{prj_datadir}
setenv M2_HOME \$MAVEN_HOME
if ( "\$path" !~ *\$MAVEN_HOME/bin* ) then
   set path = ( \$MAVEN_HOME/bin \$path  )
endif
EOF

%clean
%__rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/mvn-rpmbuild
%doc LICENSE.txt  NOTICE.txt  README.txt
%{prj_javadir}
%{prj_datadir}
%config(noreplace) %{profile_d_dir}/apache-maven.*sh


%changelog
* Fri Nov 26 2010 Ding-Yi Chen <dchen at redhat dot com> - 0:3.0-2
- Now requires java-devel instead of java, as mvn seems require javac
  to work properly.

* Tue Oct 12 2010 Ding-Yi Chen <dchen at redhat dot com> - 0:3.0-1
- Update to Maven3.

* Fri Jul 08 2010 Ding-Yi Chen <dchen at redhat dot com> - 0:2.2.1-7
- Don't tried to replace the whole Fedora's maven2, but cooperate with it.
  but still insert itself before Fedora's maven2.

* Thu Apr 01 2010 Ding-Yi Chen <dchen at redhat dot com> - 0:2.2.1-6
-Correct the apache-maven.csh

* Wed Mar 31 2010 Ding-Yi Chen <dchen at redhat dot com> - 0:2.2.1-5
-Correct the maven-plugins version.

* Mon Mar 29 2010 Ding-Yi Chen <dchen at redhat dot com> - 2.2.1-4
-Add Epoch
-Add plugins

* Wed Mar 09 2010 Ding-Yi Chen <dchen at redhat dot com> - 2.2.1-3
Fixed profile.d scripts

* Tue Mar 09 2010 Ding-Yi Chen <dchen at redhat dot com> - 2.2.1-2
Modify conflicts

* Tue Mar 09 2010 Ding-Yi Chen <dchen at redhat dot com> - 2.2.1-1
- Initial package.

