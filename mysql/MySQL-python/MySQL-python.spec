Summary: An interface to MySQL
Name: MySQL-python
Version: 1.2.3
Release: 7%{?dist}
License: GPLv2+
Group: Development/Libraries
URL: http://sourceforge.net/projects/mysql-python/

Source0: http://prdownloads.sourceforge.net/mysql-python/MySQL-python-%{version}.tar.gz

Patch1: MySQL-python-no-openssl.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: python-devel python-setuptools
BuildRequires: mysql-devel zlib-devel
# is this still needed?
# Requires: mx

%description
Python interface to MySQL

MySQLdb is an interface to the popular MySQL database server for Python.
The design goals are:

-     Compliance with Python database API version 2.0 
-     Thread-safety 
-     Thread-friendliness (threads will not block each other) 
-     Compatibility with MySQL 3.23 and up

This module should be mostly compatible with an older interface
written by Joe Skinner and others. However, the older version is
a) not thread-friendly, b) written for MySQL 3.21, c) apparently
not actively maintained. No code from that version is used in MySQLdb.

%prep
%setup -q -n %{name}-%{version}

%patch1 -p1

%build
rm -f doc/*~
export libdirname=%{_lib}
CFLAGS="$RPM_OPT_FLAGS" python setup.py build

%install
rm -rf $RPM_BUILD_ROOT

export libdirname=%{_lib}
python setup.py install --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)
%doc README doc/*
%dir %{_libdir}/python?.?/site-packages/MySQLdb
%{_libdir}/python?.?/site-packages/MySQLdb/*.pyo
%{_libdir}/python?.?/site-packages/MySQLdb/constants/*.pyo
%{_libdir}/python?.?/site-packages/*.pyo
%dir /usr/%{_lib}/python?.?/site-packages/MySQLdb/constants

%changelog
* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jul 14 2012 Tom Lane <tgl@redhat.com> 1.2.3-5
- Fix failure to enable SSL support with mysql 5.5, per Matthias Runge

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Mar 22 2011 Tom Lane <tgl@redhat.com> 1.2.3-3
- Rebuild for libmysqlclient 5.5.10 soname version bump

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 24 2010 Tom Lane <tgl@redhat.com> 1.2.3-1
- Update to final release of 1.2.3
Resolves: #660484
- Rebuild was needed anyway for mysql ABI break (no more libmysqlclient_r)

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 1.2.3-0.5.c1
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Mon Nov 23 2009 Tom Lane <tgl@redhat.com> 1.2.3-0.4.c1
- Fix format mismatch in _mysql_ConnectionObject_kill
Resolves: #538234

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 1.2.3-0.3.c1
- rebuilt with new openssl

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-0.2.c1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jun 28 2009 Tom Lane <tgl@redhat.com> 1.2.3-0.1.c1
- Update to release candidate 1.2.3c1 for better mysql 5.1 and python 2.6
  compatibility
Resolves: #505611
- Use python-setuptools instead of distutils, stop using old setup.py
Resolves: #467510
- Remove unnecessary manual Requires: specifications
Resolves: #507750

* Wed Apr 15 2009 Karsten Hopp <karsten@redhat.com> 1.2.2-11
- bump release and rebuild for s390x

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 22 2009 Tom Lane <tgl@redhat.com> 1.2.2-9
- Rebuild for mysql 5.1

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.2.2-8
- Rebuild for Python 2.6

* Thu Jun 19 2008 Tom Lane <tgl@redhat.com> 1.2.2-7
- Fix broken escape() method
Resolves: #331021

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.2.2-6
- Autorebuild for GCC 4.3

* Wed Dec  5 2007 Tom Lane <tgl@redhat.com> 1.2.2-5
- Rebuild for new openssl

* Thu Aug  2 2007 Tom Lane <tgl@redhat.com> 1.2.2-4
- Update License tag to match code.

* Tue Jul  3 2007 Tom Lane <tgl@redhat.com> 1.2.2-3
- Ooops, previous fix for quoting bug was wrong, because it converted the
  version_info tuple to a string in Python's eyes
Resolves: #246366

* Tue Jun 12 2007 Tom Lane <tgl@redhat.com> 1.2.2-2
- Fix quoting bug in use of older setup.py: need to quote version_info now
Resolves: #243877

* Fri Apr 20 2007 Tom Lane <tgl@redhat.com> 1.2.2-1
- Update to 1.2.2, but not 1.2.2 setup.py (since we don't ship setuptools yet)

* Thu Dec  7 2006 Jeremy Katz <katzj@redhat.com> - 1.2.1_p2-2
- rebuild for python 2.5

* Wed Dec  6 2006 Tom Lane <tgl@redhat.com> 1.2.1_p2-1
- Update to 1.2.1_p2

* Fri Jul 21 2006 Tom Lane <tgl@redhat.com> 1.2.1-1
- Update to 1.2.1
- Remove hardwired python version number in favor of asking Python

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.2.0-3.2.2.1
- rebuild

* Mon Feb 13 2006 Jesse Keating <jkeating@redhat.com> - 1.2.0-3.2.2
- rebump for build order issues during double-long bump

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.2.0-3.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.2.0-3.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Nov  9 2005 Tom Lane <tgl@redhat.com> 1.2.0-3
- Rebuild due to mysql 5.0 update and openssl library update.

* Wed Aug 03 2005 Karsten Hopp <karsten@redhat.de> 1.2.0-2
- package all python files. INSTALLED_FILES doesn't contain files created
  by the brp-python-bytecompile script

* Thu Apr 21 2005 Tom Lane <tgl@redhat.com> 1.2.0-1
- Update to 1.2.0, per bug #155341
- Link against mysql 4.x not 3.x, per bug #150828

* Sun Mar  6 2005 Tom Lane <tgl@redhat.com> 1.0.0-3
- Rebuild with gcc4.

* Thu Nov 11 2004 Tom Lane <tgl@redhat.com> 1.0.0-2
- bring us to python 2.4

* Thu Nov 11 2004 Tom Lane <tgl@redhat.com> 1.0.0-1
- update to 1.0.0; rebuild against mysqlclient10

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 20 2004 Tom Lane <tgl@redhat.com>
- reinstate (and update) patch for /usr/lib64 compatibility
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Nov 25 2003 Patrick Macdonald <patrickm@redhat.com> 0.9.2-1
- update to 0.9.2
- remove patches (no longer applicable)

* Sat Nov 15 2003 Tom "spot" Callaway <tcallawa@redhat.com> 0.9.1-10
- bring us to python 2.3

* Thu Jul 03 2003 Patrick Macdonald <patrickm@redhat.com> 0.9.1-9
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com> 0.9.1-8
- rebuilt

* Tue Mar 04 2003 Patrick Macdonald <patrickm@redhat.com> 0.9.1-7
- explicitly define the constants directory in case a more
  restrictive umask is encountered (#74019)

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Dec 11 2002 Tim Powers <timp@redhat.com> 0.9.1-5
- lib64'ize

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon May 13 2002 Trond Eivind Glomsrd <teg@redhat.com> 0.9.1-2
- Build for newer python

* Wed Mar 13 2002 Trond Eivind Glomsrd <teg@redhat.com> 0.9.1-1
- 0.9.1

* Tue Feb 26 2002 Trond Eivind Glomsrd <teg@redhat.com> 0.9.0-6
- Rebuild

* Thu Jan 31 2002 Elliot Lee <sopwith@redhat.com> 0.9.0-5
- Change python conflicts to requires
- Use pybasever/pynextver macros.

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Sep 14 2001 Trond Eivind Glomsrd <teg@redhat.com> 0.9.0-3
- Build for Python 2.2

* Mon Jul 23 2001 Trond Eivind Glomsrd <teg@redhat.com>
- Add zlib-devel to buildrequires (#49788)

* Tue Jun 19 2001 Trond Eivind Glomsrd <teg@redhat.com>
- Initial build
