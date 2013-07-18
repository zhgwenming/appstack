%global realname mochiweb
%global debug_package %{nil}
%global git_tag 80571b9


Name:		erlang-%{realname}
Version:	1.4.1
Release:	5%{?dist}
Summary:	An Erlang library for building lightweight HTTP servers
Group:		Development/Libraries
License:	MIT
URL:		http://github.com/mochi/mochiweb
# wget --no-check-certificate https://github.com/mochi/mochiweb/tarball/1.4.1
Source0:	mochi-%{realname}-%{version}-0-g%{git_tag}.tar.gz
Patch1:		erlang-mochiweb-0001-The-term-boolean-isn-t-availabie-in-R12B5.patch
Patch2:		erlang-mochiweb-0002-No-erlang-min-A-B-in-R12B-5-and-below.patch
Patch3:		erlang-mochiweb-0003-No-such-function-erl_scan-string-3-in-R12B5.patch
Patch4:		erlang-mochiweb-0004-No-such-function-lists-keyfind-3-in-R12B5-use-lists-.patch
Patch5:		erlang-mochiweb-0005-Fixed-ssl-related-tests-on-R12B-requires-ssl-example.patch
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires:	erlang-erts
BuildRequires:	erlang-eunit
BuildRequires:	erlang-tools
BuildRequires:	erlang-xmerl
Requires:	erlang-compiler
Requires:	erlang-crypto
Requires:	erlang-erts
Requires:	erlang-eunit
Requires:	erlang-inets
Requires:	erlang-kernel
Requires:	erlang-ssl
Requires:	erlang-stdlib
Requires:	erlang-syntax_tools
Requires:	erlang-xmerl
Provides:	%{realname} = %{version}-%{release}


%description
An Erlang library for building lightweight HTTP servers.


%prep
%setup -q -n mochi-%{realname}-%{git_tag}
%if 0%{?el5}
# Erlang/OTP R12B5
%patch1 -p1 -b .no-boolean
%patch2 -p1 -b .no-erlang-min-2
%patch3 -p1 -b .no-erl_scan-string-3
%patch4 -p1 -b .no-lists-keyfind-3
%patch5 -p1 -b .fix_for_ssl_cacert
%endif
chmod 755 scripts/new_mochiweb.erl


%build
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT

# base binary modules
install -D -m 644 ebin/%{realname}.app $RPM_BUILD_ROOT%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
install -m 644 ebin/*.beam $RPM_BUILD_ROOT%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/

# Remove test file
#rm -f $RPM_BUILD_ROOT%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/mochiweb_request_tests.beam

# skeleton files
cp -arv priv $RPM_BUILD_ROOT%{_libdir}/erlang/lib/%{realname}-%{version}
cp -arv scripts $RPM_BUILD_ROOT%{_libdir}/erlang/lib/%{realname}-%{version}
cp -arv support $RPM_BUILD_ROOT%{_libdir}/erlang/lib/%{realname}-%{version}

%check
make test


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc LICENSE README examples
%dir %{_libdir}/erlang/lib/%{realname}-%{version}
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/ebin
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/mochifmt.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/mochifmt_records.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/mochifmt_std.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/mochiglobal.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/mochihex.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/mochijson.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/mochijson2.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/mochilists.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/mochilogfile2.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/mochinum.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/mochitemp.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/mochiutf8.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/mochiweb.app
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/mochiweb.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/mochiweb_acceptor.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/mochiweb_app.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/mochiweb_charref.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/mochiweb_cookies.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/mochiweb_cover.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/mochiweb_echo.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/mochiweb_headers.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/mochiweb_html.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/mochiweb_http.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/mochiweb_io.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/mochiweb_mime.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/mochiweb_multipart.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/mochiweb_request.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/mochiweb_request_tests.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/mochiweb_response.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/mochiweb_skel.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/mochiweb_socket.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/mochiweb_socket_server.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/mochiweb_sup.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/mochiweb_util.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/reloader.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/priv
%{_libdir}/erlang/lib/%{realname}-%{version}/scripts
%{_libdir}/erlang/lib/%{realname}-%{version}/support


%changelog
* Wed Apr 06 2011 Peter Lemenkov <lemenkov@gmail.com> - 1.4.1-5
- Don't remove test-file (rhbz #675699)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov 22 2010 Peter Lemenkov <lemenkov@gmail.com> - 1.4.1-3
- Added erlang-xmerl as BuildRequires

* Mon Nov 22 2010 Peter Lemenkov <lemenkov@gmail.com> - 1.4.1-2
- Added accidentally removed dependency required for %%check

* Sat Nov 13 2010 Peter Lemenkov <lemenkov@gmail.com> - 1.4.1-1
- Ver. 1.4.1

* Wed Oct 13 2010 Peter Lemenkov <lemenkov@gmail.com> - 1.4.0-1
- Ver. 1.4.0

* Wed Sep 29 2010 Peter Lemenkov <lemenkov@gmail.com> - 1.3-0.8.20100929git9687b40
- Narrowed BuildRequires
- Restricted explicit requirement for obsoleted fd_server module (rhbz #601152)
- Dropped upstreamed patch6

* Tue Aug 17 2010 Peter Lemenkov <lemenkov@gmail.com> - 1.3-0.7.20100724git9a53dbd7
- Fix improper int to string conversion

* Wed Aug 11 2010 Peter Lemenkov <lemenkov@gmail.com> - 1.3-0.6.20100724git9a53dbd7
- Fixed all tests on EL-5
- New git snapshot

* Tue Jul 13 2010 Peter Lemenkov <lemenkov@gmail.com> - 1.3-0.5.20100507svn159
- Fixed several tests on EL-5 (enough to allow CouchDB to pass its own self-tests)

* Mon Jul 12 2010 Peter Lemenkov <lemenkov@gmail.com> - 1.3-0.4.20100507svn159
- Rebuild with new Erlang
- Simplified spec-file

* Mon Jun  7 2010 Peter Lemenkov <lemenkov@gmail.com> - 1.3-0.3.20100507svn159
- Added %%check target and fixed mochiweb:test()
- Fix EL-5 build

* Mon Jun  7 2010 Peter Lemenkov <lemenkov@gmail.com> - 1.3-0.2.20100507svn159
- Removed accidentally added macro

* Mon May 31 2010 Peter Lemenkov <lemenkov@gmail.com> - 1.3-0.1.20100507svn159
- New pre-release version (from VCS).

* Thu May 13 2010 Peter Lemenkov <lemenkov@gmail.com> - 0-0.1.svn154
- Initial package
