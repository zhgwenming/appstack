# Copyright (c) 2011,  Percona Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; see the file COPYING. If not, write to the
# Free Software Foundation, Inc., 51 Franklin St, Fifth Floor, Boston
# MA  02110-1301  USA.

%define src_dir mysql-cluster-galera

%define rhelver %(rpm -qf --qf '%%{version}\\n' /etc/redhat-release | sed -e 's/^\\([0-9]*\\).*/\\1/g')
%if "%rhelver" == "5"
 %define boost_req boost141-devel
 %define gcc_req gcc44-c++
%else
 %define boost_req boost-devel
 %define gcc_req gcc-c++
%endif

%if %{undefined scons_args}
 %define scons_args %{nil}
%endif

%ifarch i686
 %define scons_arch arch=i686
%else
 %define scons_arch %{nil}
%endif

%define redhatversion %(lsb_release -rs | awk -F. '{ print $1}')
%define distribution  rhel%{redhatversion}

%define revision 113
Name:		mysql-cluster-galera
Version:	2.0
Release:	1.%{revision}%{?dist}
Summary:	Galera components of Percona XtraDB Cluster

Group:		Applications/Databases
License:	GPLv3
URL:		https://code.launchpad.net/percona-xtradb-cluster
Source0:        mysql-cluster-galera.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:	scons check-devel glibc-devel %{gcc_req} openssl-devel %{boost_req} check-devel

%description
This package contains the Galera components required by Percona XtraDB Cluster.

%prep
%setup -q -n %{src_dir}

%build
%if "%rhelver" == "5"
export CXX=g++44
%endif
export GALERA_REV=%{revision}
export GALERA_VER=2.0
scons %{?_smp_mflags} revno=%{revision} garb/garbd libgalera_smm.so %{scons_arch} %{scons_args}

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p "$RPM_BUILD_ROOT"

install -d "$RPM_BUILD_ROOT/%{_bindir}"
install -d "$RPM_BUILD_ROOT/%{_libdir}"
install -m 755 "$RPM_BUILD_DIR/%{src_dir}/garb/garbd" \
	"$RPM_BUILD_ROOT/%{_bindir}/"
install -m 755 "$RPM_BUILD_DIR/%{src_dir}/libgalera_smm.so" \
	"$RPM_BUILD_ROOT/%{_libdir}/"

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/garbd
%attr(0755,root,root) %{_libdir}/libgalera_smm.so

%changelog
