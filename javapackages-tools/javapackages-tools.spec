Name:           javapackages-tools
Version:        0.10.0
Release:        1%{?dist}
Summary:        Macros and scripts for Java packaging support

License:        BSD
URL:            https://fedorahosted.org/javapackages/
Source0:        https://fedorahosted.org/released/javapackages/javapackages-%{version}.tar.xz
BuildArch:      noarch

BuildRequires:  jpackage-utils

Requires:       libxslt
Requires:       python

Requires:       jpackage-utils
Conflicts:      jpackage-utils < 1.7.5-17

%description
This package provides macros and scripts to support Java packaging.

%package -n maven-local
Summary:        Macros and scripts for Maven packaging support
Requires:       %{name} = %{version}-%{release}
Requires:       maven
# POM files needed by maven itself
Requires:       apache-commons-parent
Requires:       apache-parent
Requires:       maven-parent
Requires:       maven-plugins-pom
Requires:       mojo-parent
Requires:       plexus-components-pom
Requires:       plexus-pom
Requires:       plexus-tools-pom
Requires:       sonatype-oss-parent
# Don't pull in xmvn yet, add it later on
#Requires:       xmvn

%description -n maven-local
This package provides macros and scripts to support packaging Maven artifacts.


%prep
%setup -q -n javapackages-%{version}

%build

%install
install -d -m 755 $RPM_BUILD_ROOT%{_bindir}
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}-utils
install -d -m 755 $RPM_BUILD_ROOT%{_sysconfdir}/rpm
install -d -m 755 $RPM_BUILD_ROOT%{_rpmconfigdir}/fileattrs

install -p -m 755 depgenerators/maven.prov $RPM_BUILD_ROOT%{_rpmconfigdir}
install -p -m 755 depgenerators/maven.req $RPM_BUILD_ROOT%{_rpmconfigdir}
install -p -m 755 depgenerators/osgi.prov $RPM_BUILD_ROOT%{_rpmconfigdir}
install -p -m 755 depgenerators/osgi.req $RPM_BUILD_ROOT%{_rpmconfigdir}
install -p -m 755 depgenerators/javadoc.req $RPM_BUILD_ROOT%{_rpmconfigdir}
# Add the maven poms file attribute entry (rpm >= 4.9.0)
install -p -m 644 depgenerators/fileattrs/maven.attr $RPM_BUILD_ROOT%{_rpmconfigdir}/fileattrs
install -p -m 644 depgenerators/fileattrs/osgi.attr $RPM_BUILD_ROOT%{_rpmconfigdir}/fileattrs
install -p -m 644 depgenerators/fileattrs/javadoc.attr $RPM_BUILD_ROOT%{_rpmconfigdir}/fileattrs

install -p -m 644 macros.fjava $RPM_BUILD_ROOT%{_sysconfdir}/rpm
install -p -m 644 macros.xmvn $RPM_BUILD_ROOT%{_sysconfdir}/rpm
install -p -m 644 scripts/maven_depmap.py $RPM_BUILD_ROOT%{_javadir}-utils
install -p -m 644 scripts/pom_editor.sh $RPM_BUILD_ROOT%{_javadir}-utils
install -p -m 755 scripts/mvn-* $RPM_BUILD_ROOT%{_bindir}


# Ugly as hell, but Eclipse relocated various artifacts under
# their own groupId. We need to fix this globally.
# FIXME: this should be moved to respective packages
%add_to_maven_depmap org.eclipse.jetty.orbit javax.servlet any JPP tomcat-servlet-3.0-api
%add_to_maven_depmap org.eclipse.jetty.orbit javax.security.auth.message any JPP geronimo-jaspic-spec
%add_to_maven_depmap org.eclipse.jetty.orbit javax.mail.glassfish any JPP/javamail mail
%add_to_maven_depmap org.eclipse.jetty.orbit javax.transaction any JPP geronimo-jta
%add_to_maven_depmap org.eclipse.jetty.orbit javax.annotation any JPP geronimo-annotation
%add_to_maven_depmap org.eclipse.jetty.orbit org.objectweb.asm any JPP/objectweb-asm asm-all
%add_to_maven_depmap org.eclipse.jetty.orbit javax.servlet.jsp any JPP tomcat-jsp-api
%add_to_maven_depmap org.eclipse.jetty.orbit org.apache.jasper.glassfish any JPP glassfish-jsp
%add_to_maven_depmap org.eclipse.jetty.orbit javax.servlet.jsp.jstl any JPP taglibs-core
%add_to_maven_depmap org.eclipse.jetty.orbit org.apache.taglibs.standard.glassfish any JPP taglibs-standard
%add_to_maven_depmap org.eclipse.jetty.orbit javax.el any JPP tomcat-el-2.2-api
%add_to_maven_depmap org.eclipse.jetty.orbit com.sun.el any JPP tomcat-el-2.2-api
%add_to_maven_depmap org.eclipse.jetty.orbit org.eclipse.jdt.core any JPP/eclipse jdt.core


%files
%doc LICENSE
%dir %{_rpmconfigdir}/fileattrs
%{_rpmconfigdir}/fileattrs/*.attr
%{_rpmconfigdir}/*.prov
%{_rpmconfigdir}/*.req
# The python file is compiled producing .pyc and .pyo, which we need to include
%{_javadir}-utils/maven_depmap.py*
%{_javadir}-utils/pom_editor.sh
%config(noreplace) %{_sysconfdir}/rpm/macros.fjava

%files -n maven-local
%{_mavendepmapfragdir}/%{name}
%config(noreplace) %{_sysconfdir}/rpm/macros.xmvn
%{_bindir}/mvn-*


%changelog
* Mon Jan  7 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.10.0-1
- Update to upstream version 0.10.0
- Implement %%xmvn_alias, %%xmvn_file and %%xmvn_package macros
- Fix regex in osgi.attr
- Add support for pre- and post-goals in mvn-build script

* Mon Dec 10 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.9.1-1
- Update to upstream version 0.9.1
- Resolves: rhbz#885636

* Thu Dec  6 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.9.0-1
- Update to latest upstream version
- Enable maven requires generator for xmvn packages
- Enable requires generator for javadoc packages

* Wed Dec  5 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.8.3-1
- Update to upstream version 0.8.3
- Fix maven provides generator for new XML valid fragments

* Fri Nov 30 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.8.2-1
- Update to upstream version 0.8.2

* Fri Nov 30 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.8.1-1
- Update to upstream version 0.8.1

* Wed Nov 28 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.8.0-1
- Update to upstream version 0.8.0
- Add xmvn macros

* Tue Nov 27 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.7.5-3
- Add BR: jpackage-utils

* Tue Nov 27 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.7.5-2
- Add maven-local subpackage

* Thu Nov 08 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.7.5-1
- Fix versioned pom installation by quoting _jpath

* Wed Oct 31 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.7.4-1
- Shorten maven filelist filenames

* Wed Oct 31 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.7.3-1
- Update to upstream version 0.7.3

* Wed Oct 31 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.7.2-1
- Make sure add_maven_depmap fails when python tracebacks

* Wed Oct 31 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.7.1-1
- Fix problem with exception in default add_maven_depmap invocation

* Tue Oct 30 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.7.0-1
- Update to latest upstream
- Full support for compat depmap generation
- Generate maven-files-%%{name} with a list of files to package
- Add support for maven repo generation (alpha version)

* Mon Jul 30 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.6.0-1
- Update to upstream version 0.6.0
- Make maven provides versioned
- Add additional pom_ macros to simplify additional pom editing

* Wed Jul 25 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.5.0-1
- Update to upstream version 0.5.0 - add support for add_maven_depmap -v

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul  9 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.4.1-1
- Update to upstream version 0.4.1
- Fixes #837203

* Wed Jun 27 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.4.0-1
- Update to upstream version 0.4.0

* Tue Mar  6 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.3.1-1
- Create maven provides from fragments instead of poms

* Thu Feb 16 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.3.0-3
- Fix maven_depmap installation

* Wed Feb 15 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.3.0-2
- Add conflicts with older jpackage-utils

* Wed Feb 15 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.3.0-1
- Initial version split from jpackage-utils
