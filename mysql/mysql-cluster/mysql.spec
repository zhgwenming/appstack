# Copyright (c) 2000, 2010, Oracle and/or its affiliates. All rights reserved.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
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

##############################################################################
# Some common macro definitions
##############################################################################

# NOTE: "vendor" is used in upgrade/downgrade check, so you can't
# change these, has to be exactly as is.
%{?scl:%scl_package mysql}

%define mysql_old_vendor        MySQL AB
%define mysql_vendor_2          Sun Microsystems, Inc.
%define mysql_vendor            Oracle and/or its affiliates
%define mysql_server_vendor	%{pkgvendor}

# based on 5.5.29-23.7.2.389.rhel6
%define wsrep_version 908.23.7.2
%define revision 389

%define mysql_version   5.5.29
%define redhatversion %(lsb_release -rs | awk -F. '{ print $1}')
%define majorversion 29
%define minorversion 4
%define distribution  rhel%{redhatversion}
%define percona_server_version	%{wsrep_version}

%define mysqld_user     mysql
%define mysqld_group    mysql
%define mysqldatadir    %{?scl:/srv/%{scl}/mysql}%{!?scl:%{_localstatedir}/lib/mysql}

%if %{undefined revision}
%define revision	1
%endif

%define release_tag	%{nil}
%define release         %{release_tag}%{wsrep_version}.%{revision}

#
# Macros we use which are not available in all supported versions of RPM
#
# - defined/undefined are missing on RHEL4
#
%if %{expand:%{?defined:0}%{!?defined:1}}
%define defined()       %{expand:%%{?%{1}:1}%%{!?%{1}:0}}
%endif
%if %{expand:%{?undefined:0}%{!?undefined:1}}
%define undefined()     %{expand:%%{?%{1}:0}%%{!?%{1}:1}}
%endif

# ----------------------------------------------------------------------------
# RPM build tools now automatically detect Perl module dependencies.  This
# detection causes problems as it is broken in some versions, and it also
# provides unwanted dependencies from mandatory scripts in our package.
# It might not be possible to disable this in all versions of RPM, but here we
# try anyway.  We keep the "AutoReqProv: no" for the "test" sub package, as
# disabling here might fail, and that package has the most problems.
# See:
#  http://fedoraproject.org/wiki/Packaging/Perl#Filtering_Requires:_and_Provides
#  http://www.wideopen.com/archives/rpm-list/2002-October/msg00343.html
# ----------------------------------------------------------------------------
%undefine __perl_provides
%undefine __perl_requires

##############################################################################
# Command line handling
##############################################################################
#
# To set options:
#
#   $ rpmbuild --define="option <x>" ...
#

# ----------------------------------------------------------------------------
# Commercial builds
# ----------------------------------------------------------------------------
%if %{undefined commercial}
%define commercial 0
%endif

# ----------------------------------------------------------------------------
# Source name
# ----------------------------------------------------------------------------
%if %{undefined src_base}
%define src_base mysql
%endif
%define src_dir %{src_base}-%{mysql_version}

# ----------------------------------------------------------------------------
# Feature set (storage engines, options).  Default to community (everything)
# ----------------------------------------------------------------------------
%if %{undefined feature_set}
%define feature_set community
%endif

# ----------------------------------------------------------------------------
# Server comment strings
# ----------------------------------------------------------------------------
%if %{undefined compilation_comment_debug}
%define compilation_comment_debug       MySQL Galera Cluster - Debug (GPL)
%endif
%if %{undefined compilation_comment_release}
%define compilation_comment_release     MySQL Galera Cluster (GPL)
%endif

# ----------------------------------------------------------------------------
# Product and server suffixes
# ----------------------------------------------------------------------------
%define product_suffix %{nil}
%if %{undefined product_suffix}
  %if %{defined short_product_tag}
    %define product_suffix      -%{short_product_tag}
  %else
    %define product_suffix      %{nil}
  %endif
%endif

%define server_suffix %{product_suffix}
%if %{undefined server_suffix}
%define server_suffix   %{nil}
%endif

# ----------------------------------------------------------------------------
# Distribution support
# ----------------------------------------------------------------------------
%if %{undefined distro_specific}
%define distro_specific 0
%endif
%if %{distro_specific}
  %if %(test -f /etc/enterprise-release && echo 1 || echo 0)
    %define oelver %(rpm -qf --qf '%%{version}\\n' /etc/enterprise-release | sed -e 's/^\\([0-9]*\\).*/\\1/g')
    %if "%oelver" == "4"
      %define distro_description        Oracle Enterprise Linux 4
      %define distro_releasetag         oel4
      %define distro_buildreq           gcc-c++ gperf ncurses-devel perl readline-devel time zlib-devel libaio-devel bison cmake redhat-lsb
      %define distro_requires           chkconfig coreutils grep procps shadow-utils
    %else
      %if "%oelver" == "5"
        %define distro_description      Oracle Enterprise Linux 5
        %define distro_releasetag       oel5
        %define distro_buildreq         gcc-c++ gperf ncurses-devel perl readline-devel time zlib-devel libaio-devel bison cmake redhat-lsb
        %define distro_requires         chkconfig coreutils grep procps shadow-utils
      %else
        %{error:Oracle Enterprise Linux %{oelver} is unsupported}
      %endif
    %endif
  %else
    %if %(test -f /etc/redhat-release && echo 1 || echo 0)
      %define rhelver %(rpm -qf --qf '%%{version}\\n' /etc/redhat-release | sed -e 's/^\\([0-9]*\\).*/\\1/g')
      %if "%rhelver" == "4"
        %define distro_description      Red Hat Enterprise Linux 4
        %define distro_releasetag       rhel4
        %define distro_buildreq         gcc-c++ gperf ncurses-devel perl readline-devel time zlib-devel libaio-devel bison cmake redhat-lsb
        %define distro_requires         chkconfig coreutils grep procps shadow-utils
      %else
        %if "%rhelver" == "5"
          %define distro_description    Red Hat Enterprise Linux 5
          %define distro_releasetag     rhel5
          %define distro_buildreq       gcc-c++ gperf ncurses-devel perl readline-devel time zlib-devel libaio-devel bison cmake redhat-lsb
          %define distro_requires       chkconfig coreutils grep procps shadow-utils
        %else
          %{error:Red Hat Enterprise Linux %{rhelver} is unsupported}
        %endif
      %endif
    %else
      %if %(test -f /etc/SuSE-release && echo 1 || echo 0)
        %define susever %(rpm -qf --qf '%%{version}\\n' /etc/SuSE-release)
        %if "%susever" == "10"
          %define distro_description    SUSE Linux Enterprise Server 10
          %define distro_releasetag     sles10
          %define distro_buildreq       gcc-c++ gdbm-devel gperf ncurses-devel openldap2-client readline-devel zlib-devel libaio-devel bison cmake redhat-lsb
          %define distro_requires       aaa_base coreutils grep procps pwdutils
        %else
          %if "%susever" == "11"
            %define distro_description  SUSE Linux Enterprise Server 11
            %define distro_releasetag   sles11
            %define distro_buildreq     gcc-c++ gdbm-devel gperf ncurses-devel openldap2-client procps pwdutils readline-devel zlib-devel libaio-devel bison cmake redhat-lsb
            %define distro_requires     aaa_base coreutils grep procps pwdutils
          %else
            %{error:SuSE %{susever} is unsupported}
          %endif
        %endif
      %else
        %{error:Unsupported distribution}
      %endif
    %endif
  %endif
%else
  %define generic_kernel %(uname -r | cut -d. -f1-2)
  %define distro_description            Generic Linux (kernel %{generic_kernel})
  %define distro_releasetag             linux%{generic_kernel}
  %define distro_buildreq               gcc-c++ gperf ncurses-devel perl readline-devel time zlib-devel libaio-devel bison cmake redhat-lsb
  %define distro_requires               coreutils grep procps /sbin/chkconfig /usr/sbin/useradd /usr/sbin/groupadd
%endif

# ----------------------------------------------------------------------------
# Support optional "tcmalloc" library (experimental)
# ----------------------------------------------------------------------------
%if %{defined malloc_lib_target}
%define WITH_TCMALLOC 1
%else
%define WITH_TCMALLOC 0
%endif

##############################################################################
# Configuration based upon above user input, not to be set directly
##############################################################################

%if %{commercial}
%define license_files_server    %{src_dir}/LICENSE.mysql
%define license_type            Commercial
%else
%define license_files_server    %{src_dir}/COPYING %{src_dir}/README
%define license_type            GPL
%endif

##############################################################################
# Main spec file section
##############################################################################

Name:           %{?scl: %{scl_prefix}}mysql
Summary:        A High Availability solution based on galera
Group:          Applications/Databases
Version:        %{mysql_version}
Release:        %{release}%{?dist}
Epoch:		1
Distribution:   %{distro_description}
License:        Copyright (c) 2000, 2010, %{mysql_vendor}.  All rights reserved.  Use is subject to license terms.  Under %{license_type} license as shown in the Description field.
Source:         mysql-%{mysql_version}.tar.gz
URL:            http://www.percona.com/
Packager:       MySQL Development Team
Vendor:         %{mysql_server_vendor}
Provides:       %{?scl_prefix}mysql
Requires:	%{name}-libs = %{version}-%{release}
BuildRequires:  %{distro_buildreq}
BuildRequires:  pam-devel

Source3: my.cnf
Source4: mcluster-bootstrap
Source5: mcheck
Source101: mysql.init

Patch101: mysql-scl-env-check.patch
Patch102: mysql-daemonstatus.patch

# Think about what you use here since the first step is to
# run a rm -rf
BuildRoot:    %{_tmppath}/%{name}-%{version}-build

# From the manual
%description
MySQL Galera Cluster is based on the Percona/galera Server database server and
provides a High Availability solution.
MySQL Galera Cluster provides synchronous replication, supports
multi-master replication, parallel applying on slaves, automatic node
provisioning with primary focus on data consistency.


##############################################################################
# Sub package definition
##############################################################################

%package server
Summary:        MySQL Galera Cluster - server package
Group:          Applications/Databases
Requires:       %{distro_requires} %{?scl_prefix}mysql-libs mysql-cluster-galera xtrabackup >= 1.9.0 tar nc rsync
Requires:	%{name} = %{version}-%{release}
Requires:	ruby-mysql
%{?scl:Requires:%scl_runtime}
Provides:       %{?scl_prefix}mysql-server MySQL-server 
Conflicts:	Percona-Server-server-55 Percona-Server-server-51

%description server
MySQL Galera Cluster is based on the Percona Server database server and
provides a High Availability solution.
MySQL Galera Cluster provides synchronous replication, supports
multi-master replication, parallel applying on slaves, automatic node
provisioning with primary focus on data consistency.

This package includes the MySQL Galera Cluster binary 
as well as related utilities to run and administer MySQL Galera Cluster.

If you want to access and work with the database, you have to install
package "mysql" as well!

# ----------------------------------------------------------------------------
%package bench

Summary: MySQL benchmark scripts and data
Group: Applications/Databases
Requires: %{name}% = %{version}-%{release}
Conflicts: MySQL-bench

%description bench
MySQL is a multi-user, multi-threaded SQL database server. This
package contains benchmark scripts and data for use when benchmarking
MySQL.

%package test
Requires:       mysql perl
Summary:        MySQL Galera Cluster - Test suite
Group:          Applications/Databases
Provides:       %{?scl_prefix}mysql-test
Conflicts:	Percona-Server-test-55 Percona-Server-test-51
AutoReqProv:    no

%description test
MySQL Galera Cluster provides synchronous replication, supports
multi-master replication, parallel applying on slaves, automatic node
provisioning with primary focus on data consistency.

This package contains the MySQL Galera Cluster regression test suite.

For a description of MySQL Galera Cluster see

# ----------------------------------------------------------------------------
%package devel
Summary:        MySQL Galera Cluster - Development header files and libraries
Group:          Applications/Databases
Provides:       %{?scl_prefix}mysql-devel
Conflicts:	Percona-Server-devel-55 Percona-Server-devel-51

%description devel
MySQL Galera Cluster is based on the Percona Server database server and
provides a High Availability solution.
MySQL Galera Cluster provides synchronous replication, supports
multi-master replication, parallel applying on slaves, automatic node
provisioning with primary focus on data consistency.

This package contains the development header files and libraries necessary
to develop MySQL Galera Cluster client applications.

# ----------------------------------------------------------------------------
%package libs
Summary:        MySQL Galera Cluster - Shared libraries
Group:          Applications/Databases
Provides:       %{?scl_prefix}mysql-libs
Conflicts:	Percona-Server-shared-55 Percona-Server-shared-51

%description libs
MySQL Galera Cluster is based on the Percona Server database server and
provides a High Availability solution.
MySQL Galera Cluster provides synchronous replication, supports
multi-master replication, parallel applying on slaves, automatic node
provisioning with primary focus on data consistency.

This package contains the shared libraries (*.so*) which certain languages
and applications need to dynamically load and use MySQL Galera Cluster.

##############################################################################
%prep
%setup -T -a 0 -c %{?scl:-n %{pkg_name}-%{version}}

# path adding collection name into some scripts
# patch is applied only if building into SCL
# some values in patch are replaced by real value depending on collection name
cp -p %{SOURCE101} %{src_dir}/mysql.init
(cd %{src_dir};
%if 0%{?scl:1}
%global scl_sed_patches 1
%if %scl_sed_patches
cat %{PATCH101} | sed -e "s/__SCL_NAME__/%{?scl}/g" \
                      -e "s|__SCL_SCRIPTS__|%{?_scl_scripts}|g" \
                | patch -p1 -b --suffix .scl-env-check
cat %{PATCH102} | sed -e "s/__SCL_NAME__/%{?scl}/" \
                | patch -p1 -b --suffix .daemonstatus
%else
patch -p1 -b --suffix .scl-env-check<%{PATCH101}
patch -p1 -b --suffix .daemonstatus<%{PATCH102}
%endif
%endif
)


##############################################################################
%build

# Be strict about variables, bail at earliest opportunity, etc.
set -uex

BuildHandlerSocket() {
    cd storage/HandlerSocket-Plugin-for-MySQL
    bash -x ./autogen.sh
    echo "Configuring HandlerSocket"
    CXX="${HS_CXX:-g++}" \
        MYSQL_CFLAGS="-I %{_builddir}/%{src_dir}/release/include" \
        ./configure --with-mysql-source=%{_builddir}/%{src_dir}/%{src_dir} \
        --with-mysql-bindir=%{_builddir}/%{src_dir}/release/scripts \
        --with-mysql-plugindir=%{_libdir}/mysql/plugin \
        --libdir=%{_libdir} \
        --prefix=%{_prefix}
    make %{?_smp_mflags}
    cd -
}

BuildUDF() {
    cd UDF
    CXX="${UDF_CXX:-g++}"\
        CXXFLAGS="$CXXFLAGS -I%{_builddir}/%{src_dir}/release/include" \
        ./configure --includedir=%{_builddir}/%{src_dir}/%{src_dir}/include \
        --libdir=%{_libdir}/mysql/plugin
    make %{?_smp_mflags} all
    cd -
}

build_pam() {
    cd plugin/percona-pam-for-mysql
    bash -x ./autogen.sh
    CXX="${UDF_CXX:-g++}"\
        CXXFLAGS="$CXXFLAGS -I%{_builddir}/%{src_dir}/release/include" \
        ./configure --includedir=%{_builddir}/%{src_dir}/%{src_dir}/include \
        --libdir=%{_libdir}/mysql/plugin
    make %{?_smp_mflags} all
    cd -
}

# Optional package files
touch optional-files-devel

#
# Set environment in order of preference, MYSQL_BUILD_* first, then variable
# name, finally a default.  RPM_OPT_FLAGS is assumed to be a part of the
# default RPM build environment.
#
# We set CXX=gcc by default to support so-called 'generic' binaries, where we
# do not have a dependancy on libgcc/libstdc++.  This only works while we do
# not require C++ features such as exceptions, and may need to be removed at
# a later date.
#

# This is a hack, $RPM_OPT_FLAGS on ia64 hosts contains flags which break
# the compile in cmd-line-utils/readline - needs investigation, but for now
# we simply unset it and use those specified directly in cmake.
%if "%{_arch}" == "ia64"
RPM_OPT_FLAGS=
%endif

export PATH=${MYSQL_BUILD_PATH:-$PATH}
export CC=${MYSQL_BUILD_CC:-${CC:-gcc}}
export CXX=${MYSQL_BUILD_CXX:-${CXX:-gcc}}
export CFLAGS=${MYSQL_BUILD_CFLAGS:-${CFLAGS:-$RPM_OPT_FLAGS}}
export CXXFLAGS=${MYSQL_BUILD_CXXFLAGS:-${CXXFLAGS:-$RPM_OPT_FLAGS -felide-constructors -fno-exceptions -fno-rtti}}
export LDFLAGS=${MYSQL_BUILD_LDFLAGS:-${LDFLAGS:-}}
export CMAKE=${MYSQL_BUILD_CMAKE:-${CMAKE:-cmake}}
export MAKE_JFLAG=${MYSQL_BUILD_MAKE_JFLAG:-${MAKE_JFLAG:-}}

# Build debug mysqld and libmysqld.a
mkdir debug
(
  cd debug
  # Attempt to remove any optimisation flags from the debug build
  CFLAGS=`echo " ${CFLAGS} " | \
            sed -e 's/ -O[0-9]* / /' \
                -e 's/ -unroll2 / /' \
                -e 's/ -ip / /' \
                -e 's/^ //' \
                -e 's/ $//'`
  CXXFLAGS=`echo " ${CXXFLAGS} " | \
              sed -e 's/ -O[0-9]* / /' \
                  -e 's/ -unroll2 / /' \
                  -e 's/ -ip / /' \
                  -e 's/^ //' \
                  -e 's/ $//'`
  # XXX: MYSQL_UNIX_ADDR should be in cmake/* but mysql_version is included before
  # XXX: install_layout so we can't just set it based on INSTALL_LAYOUT=RPM
           #-DFEATURE_SET="%{feature_set}" \
  ${CMAKE} ../%{src_dir} -DBUILD_CONFIG=mysql_release -DINSTALL_LAYOUT=RPM \
           -DCMAKE_BUILD_TYPE=Debug \
        -DCMAKE_INSTALL_PREFIX="%{_prefix}" \
        -DINSTALL_INCLUDEDIR=include/mysql \
        -DINSTALL_INFODIR=share/info \
        -DINSTALL_LIBDIR="%{_lib}/mysql" \
        -DINSTALL_MANDIR=share/man \
        -DINSTALL_MYSQLSHAREDIR=share/mysql \
        -DINSTALL_MYSQLTESTDIR=share/mysql-test \
        -DINSTALL_PLUGINDIR="%{_lib}/mysql/plugin" \
        -DINSTALL_SBINDIR=libexec \
        -DINSTALL_SCRIPTDIR=bin \
        -DINSTALL_SQLBENCHDIR=share \
        -DINSTALL_SUPPORTFILESDIR=share/mysql \
        -DMYSQL_DATADIR="%{?_scl_root}/var/lib/mysql" \
        -DMYSQL_UNIX_ADDR="/var/lib/mysql/mysql.sock" \
        -DENABLED_LOCAL_INFILE=ON \
           -DENABLE_DTRACE=OFF \
           -DWITH_EMBEDDED_SERVER=OFF \
           -DFEATURE_SET="%{feature_set}" \
           -DCOMPILATION_COMMENT="%{compilation_comment_debug}" \
           -DWITH_WSREP=1 \
           -DWITH_INNODB_DISALLOW_WRITES=ON \
        -DWITH_READLINE=ON \
        -DWITH_SSL=system \
        -DWITH_ZLIB=system \
           -DMYSQL_SERVER_SUFFIX="%{server_suffix}" \
        -DSYSCONFDIR="%{?_scl_root}/etc" \
        -DWITH_MYSQLD_LDFLAGS="-Wl,-z,relro,-z,now"

  echo BEGIN_DEBUG_CONFIG ; egrep '^#define' include/config.h ; echo END_DEBUG_CONFIG
  make %{?_smp_mflags} ${MAKE_JFLAG}
)

# Build full release
mkdir release
(
  cd release
  #build_pam
  # XXX: MYSQL_UNIX_ADDR should be in cmake/* but mysql_version is included before
  # XXX: install_layout so we can't just set it based on INSTALL_LAYOUT=RPM
  ${CMAKE} ../%{src_dir} -DBUILD_CONFIG=mysql_release -DINSTALL_LAYOUT=RPM \
           -DCMAKE_BUILD_TYPE=RelWithDebInfo \
        -DCMAKE_INSTALL_PREFIX="%{_prefix}" \
        -DINSTALL_INCLUDEDIR=include/mysql \
        -DINSTALL_INFODIR=share/info \
        -DINSTALL_LIBDIR="%{_lib}/mysql" \
        -DINSTALL_MANDIR=share/man \
        -DINSTALL_MYSQLSHAREDIR=share/mysql \
        -DINSTALL_MYSQLTESTDIR=share/mysql-test \
        -DINSTALL_PLUGINDIR="%{_lib}/mysql/plugin" \
        -DINSTALL_SBINDIR=libexec \
        -DINSTALL_SCRIPTDIR=bin \
        -DINSTALL_SQLBENCHDIR=share \
        -DINSTALL_SUPPORTFILESDIR=share/mysql \
        -DMYSQL_DATADIR="%{?_scl_root}/var/lib/mysql" \
        -DMYSQL_UNIX_ADDR="/var/lib/mysql/mysql.sock" \
        -DENABLED_LOCAL_INFILE=ON \
           -DENABLE_DTRACE=OFF \
           -DWITH_EMBEDDED_SERVER=OFF \
           -DFEATURE_SET="%{feature_set}" \
           -DCOMPILATION_COMMENT="%{compilation_comment_release}" \
           -DWITH_WSREP=1 \
           -DWITH_INNODB_DISALLOW_WRITES=ON \
        -DWITH_READLINE=ON \
        -DWITH_SSL=system \
        -DWITH_ZLIB=system \
           -DMYSQL_SERVER_SUFFIX="%{server_suffix}" \
        -DSYSCONFDIR="%{?_scl_root}/etc" \
        -DWITH_MYSQLD_LDFLAGS="-Wl,-z,relro,-z,now"

  echo BEGIN_NORMAL_CONFIG ; egrep '^#define' include/config.h ; echo END_NORMAL_CONFIG
  make %{?_smp_mflags} ${MAKE_JFLAG}
  cd ../%{src_dir}
  d="`pwd`"
  BuildHandlerSocket
  BuildUDF
  cd "$d"
)

# For the debuginfo extraction stage, some source files are not located in the release
# and debug dirs, but in the source dir. Make a link there to avoid errors in the
# strip phase.
for f in lexyy.c pars0grm.c pars0grm.y pars0lex.l
do
    for d in debug release
    do
        ln -s "../../../%{src_dir}/storage/innobase/pars/$f" "$d/storage/innobase/"
    done
done

# Use the build root for temporary storage of the shared libraries.
RBR=%{buildroot}

# Clean up the BuildRoot first
[ "%{buildroot}" != "/" ] && [ -d "%{buildroot}" ] && rm -rf "%{buildroot}";

# For gcc builds, include libgcc.a in the devel subpackage (BUG 4921).  This
# needs to be during build phase as $CC is not set during install.
if "$CC" -v 2>&1 | grep '^gcc.version' >/dev/null 2>&1
then
  libgcc=`$CC $CFLAGS --print-libgcc-file`
  if [ -f $libgcc ]
  then
    mkdir -p %{buildroot}%{_libdir}/mysql
    install -m 644 $libgcc %{buildroot}%{_libdir}/mysql/libmygcc.a
    echo "%{_libdir}/mysql/libmygcc.a" >>optional-files-devel
  fi
fi

# Move temporarily the saved files to the BUILD directory since the BUILDROOT
# dir will be cleaned at the start of the install phase
mkdir -p "$(dirname %{_builddir}/%{_libdir})"
mv %{buildroot}%{_libdir} %{_builddir}/%{_libdir}

##############################################################################
%install

RBR=%{buildroot}
MBD=%{_builddir}/%{src_dir}

# Move back the libdir from BUILD dir to BUILDROOT
mkdir -p "$(dirname %{buildroot}%{_libdir})"
mv %{_builddir}/%{_libdir} %{buildroot}%{_libdir}

# Ensure that needed directories exists
install -d %{buildroot}%{?scl:%_root_sysconfdir}%{!?scl:%_sysconfdir}/{logrotate.d,xinetd.d,rc.d/init.d}
install -d %{buildroot}%{_localstatedir}/run/mysqld

install -d %{buildroot}%{mysqldatadir}
install -d %{buildroot}%{_datadir}/mysql-test
install -d %{buildroot}%{_datadir}/mysql/SELinux/RHEL4
install -d %{buildroot}%{_includedir}
install -d %{buildroot}%{_libdir}
install -d %{buildroot}%{_mandir}
install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_libdir}/mysql/plugin

(
  cd $MBD/release
  make %{?_smp_mflags} DESTDIR=%{buildroot} benchdir_root=%{_datadir} install
  d="`pwd`"
  cd $MBD/%{src_dir}/storage/HandlerSocket-Plugin-for-MySQL
  make %{?_smp_mflags} DESTDIR=%{buildroot} benchdir_root=%{_datadir} install
  cd "$d"
  cd $MBD/%{src_dir}/UDF
  make %{?_smp_mflags} DESTDIR=%{buildroot} benchdir_root=%{_datadir} install
  cd "$d"
)

# Install all binaries
(
  cd $MBD/release
  make %{?_smp_mflags} DESTDIR=%{buildroot} install
)

# FIXME: at some point we should stop doing this and just install everything
# FIXME: directly into %{_libdir}/mysql - perhaps at the same time as renaming
# FIXME: the shared libraries to use libmysql*-$major.$minor.so syntax
mv -v %{buildroot}/%{_libdir}/*.a %{buildroot}/%{_libdir}/mysql/

# Install logrotate and autostart
install -m 644 $MBD/release/support-files/mysql-log-rotate %{buildroot}%{?scl:%_root_sysconfdir}%{!?scl:%_sysconfdir}/logrotate.d/%{?scl_prefix}mysqld
sed -i -e 's|/var/log/mysql|/var/log/%{?scl_prefix}mysql|g' %{buildroot}%{?scl:%_root_sysconfdir}%{!?scl:%_sysconfdir}/logrotate.d/%{?scl_prefix}mysqld

install -m 644 $MBD/release/support-files/mysqlchk %{buildroot}%{?scl:%_root_sysconfdir}%{!?scl:%_sysconfdir}/xinetd.d/%{?scl_prefix}mysqlchk
#install -m 755 $MBD/release/support-files/mysql.server %{buildroot}%{?scl:%_root_sysconfdir}%{!?scl:%_sysconfdir}/rc.d/init.d/%{?scl_prefix}mysqld
sed -i  -e 's|/etc/my.cnf|%{_sysconfdir}/my.cnf|g' \
        -e 's|/etc/sysconfig/mysqld|%{_sysconfdir}/sysconfig/mysqld|g' \
        -e 's|/etc/sysconfig/\$prog|%{_sysconfdir}/sysconfig/\$prog|g' \
        -e 's|/var/run/mysqld/|%{?_scl_root}/var/run/mysqld/|g' \
        -e 's|/usr|%{_prefix}|g' \
        -e 's|/var/lib/|%{?_scl_root}/var/lib/|g' \
        -e 's|/var/log/mysql|/var/log/%{?scl_prefix}mysql|g' \
        -e 's|get_mysql_option mysqld socket "$datadir/mysql.sock"|get_mysql_option mysqld socket "/var/lib/mysql/mysql.sock"|' %{src_dir}/mysql.init
install -m 0755 %{src_dir}/mysql.init %{buildroot}%{?scl:%_root_sysconfdir}%{!?scl:%_sysconfdir}/rc.d/init.d/%{?scl_prefix}mysqld

install -d %{buildroot}/%{_sysconfdir}
install -m 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/my.cnf
sed -i	-e 's|__SCL_ROOT__|%{_scl_root}|' \
	-e 's|__SCL__|%{scl}|' %{buildroot}%{_sysconfdir}/my.cnf

mkdir -p %{buildroot}/var/log
touch %{buildroot}/var/log/%{?scl_prefix}mysqld.log

# always install it to the base system, like other scripts
install -d  %{buildroot}/usr/share/mysql
install -m 0755 %{SOURCE4} %{buildroot}/usr/share/mysql/mcluster-bootstrap
install -m 0755 %{SOURCE5} %{buildroot}{_bindir}/mcheck
sed -i	-e 's|__SCL_ROOT__|%{_scl_root}|' %{buildroot}/usr/share/mysql/mcluster-bootstrap

# Create a symlink "rcmysql", pointing to the init.script. SuSE users
# will appreciate that, as all services usually offer this.
ln -s %{?scl:_root_sysconfdir}{!?scl:_sysconfdir}/init.d/mysql %{buildroot}%{_sbindir}/rcmysql

# Create a wsrep_sst_rsync_wan symlink.
install -d %{buildroot}%{_bindir}
ln -s wsrep_sst_rsync %{buildroot}%{_bindir}/wsrep_sst_rsync_wan

# Install SELinux files in datadir
install -m 600 $MBD/%{src_dir}/support-files/RHEL4-SElinux/mysql.{fc,te} \
  %{buildroot}%{_datadir}/mysql/SELinux/RHEL4

%if %{WITH_TCMALLOC}
# Even though this is a shared library, put it under /usr/lib*/mysql, so it
# doesn't conflict with possible shared lib by the same name in /usr/lib*.  See
# `mysql_config --variable=pkglibdir` and mysqld_safe for how this is used.
install -m 644 "%{malloc_lib_source}" \
  "%{buildroot}%{_libdir}/mysql/%{malloc_lib_target}"
%endif

# Remove man pages we explicitly do not want to package, avoids 'unpackaged
# files' warning.
rm -f %{buildroot}%{_mandir}/man1/make_win_bin_dist.1*

# ldconfig for mysql libs
mkdir -p %{buildroot}/etc/ld.so.conf.d
echo "%{_libdir}/mysql" > %{buildroot}/etc/ld.so.conf.d/%{name}-%{_arch}.conf


# ----------------------------------------------------------------------
# Clean up the BuildRoot after build is done
# ----------------------------------------------------------------------
%clean
[ "%{buildroot}" != "/" ] && [ -d %{buildroot} ] \
  && rm -rf %{buildroot};

##############################################################################
#  Post processing actions, i.e. when installed
##############################################################################

%pre server

/usr/sbin/groupadd -g 27 -o -r mysql >/dev/null 2>&1 || :
/usr/sbin/useradd -M -N -g mysql -o -r -d %{mysqldatadir} -s /bin/bash \
	-c "MySQL Server" -u 27 mysql >/dev/null 2>&1 || :


# Shut down a previously installed server first
if [ -x %{?scl:_root_sysconfdir}%{!?scl:%_sysconfdir}/init.d/%{?scl_prefix}mysqld ] ; then
        service %{?scl_prefix}mysqld stop
fi

%post server

if [ -x /sbin/chkconfig ] ; then
        /sbin/chkconfig --add %{?scl_prefix}mysqld
fi

echo "MySQL Galera Cluster is distributed with several useful UDFs"
echo "Run the following commands to create these functions:"
echo "mysql -e \"CREATE FUNCTION fnv1a_64 RETURNS INTEGER SONAME 'libfnv1a_udf.so'\""
echo "mysql -e \"CREATE FUNCTION fnv_64 RETURNS INTEGER SONAME 'libfnv_udf.so'\""
echo "mysql -e \"CREATE FUNCTION murmur_hash RETURNS INTEGER SONAME 'libmurmur_udf.so'\""
echo "See http://code.google.com/p/maatkit/source/browse/trunk/udf for more details"

%preun server

# Which '$1' does this refer to?  Fedora docs have info:
# " ... a count of the number of versions of the package that are installed.
#   Action                           Count
#   Install the first time           1
#   Upgrade                          2 or higher (depending on the number of versions installed)
#   Remove last version of package   0 "
#
#  http://docs.fedoraproject.org/en-US/Fedora_Draft_Documentation/0.1/html/RPM_Guide/ch09s04s05.html
 
if [ $1 = 0 ] ; then
        # Stop MySQL before uninstalling it
	service %{scl_prefix}mysqld stop
fi

# We do not remove the mysql user since it may still own a lot of
# database files.

%post libs
/sbin/ldconfig

%postun libs
/sbin/ldconfig


##############################################################################
#  Files section
##############################################################################

%files server
%defattr(-,root,root,0755)

%if %{defined license_files_server}
%doc %{license_files_server}
%endif
#%doc %{src_dir}/Docs/INFO_SRC
%doc release/Docs/INFO_BIN
%doc release/support-files/my-*.cnf
%doc %{src_dir}/Docs/README-wsrep
%doc release/support-files/wsrep.cnf

%doc %attr(644, root, root) %{_infodir}/mysql.info*

%doc %attr(644, root, man) %{_mandir}/man1/innochecksum.1*
%doc %attr(644, root, man) %{_mandir}/man1/myisam_ftdump.1*
%doc %attr(644, root, man) %{_mandir}/man1/myisamchk.1*
%doc %attr(644, root, man) %{_mandir}/man1/myisamlog.1*
%doc %attr(644, root, man) %{_mandir}/man1/myisampack.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysql_convert_table_format.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysql_fix_extensions.1*
%doc %attr(644, root, man) %{_mandir}/man8/mysqld.8*
%doc %attr(644, root, man) %{_mandir}/man1/mysqld_multi.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysqld_safe.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysqldumpslow.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysql_install_db.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysql_secure_installation.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysql_setpermission.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysql_upgrade.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysqlhotcopy.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysqlman.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysql.server.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysqltest.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysql_tzinfo_to_sql.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysql_zap.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysqlbug.1*
%doc %attr(644, root, man) %{_mandir}/man1/perror.1*
%doc %attr(644, root, man) %{_mandir}/man1/replace.1*
%doc %attr(644, root, man) %{_mandir}/man1/resolve_stack_dump.1*
%doc %attr(644, root, man) %{_mandir}/man1/resolveip.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysql_plugin.1*

%attr(755, root, root) %{_bindir}/clustercheck
%attr(755, root, root) %{_bindir}/innochecksum
%attr(755, root, root) %{_bindir}/myisam_ftdump
%attr(755, root, root) %{_bindir}/myisamchk
%attr(755, root, root) %{_bindir}/myisamlog
%attr(755, root, root) %{_bindir}/myisampack
%attr(755, root, root) %{_bindir}/mysql_convert_table_format
%attr(755, root, root) %{_bindir}/mysql_fix_extensions
%attr(755, root, root) %{_bindir}/mysql_install_db
%attr(755, root, root) %{_bindir}/mysql_secure_installation
%attr(755, root, root) %{_bindir}/mysql_setpermission
%attr(755, root, root) %{_bindir}/mysql_tzinfo_to_sql
%attr(755, root, root) %{_bindir}/mysql_upgrade
%attr(755, root, root) %{_bindir}/mysql_plugin
%attr(755, root, root) %{_bindir}/mysql_zap
%attr(755, root, root) %{_bindir}/mysqlbug
%attr(755, root, root) %{_bindir}/mysqld_multi
%attr(755, root, root) %{_bindir}/mysqld_safe
%attr(755, root, root) %{_bindir}/mysqldumpslow
%attr(755, root, root) %{_bindir}/mysqlhotcopy
%attr(755, root, root) %{_bindir}/mysqltest
%attr(755, root, root) %{_bindir}/perror
%attr(755, root, root) %{_bindir}/replace
%attr(755, root, root) %{_bindir}/resolve_stack_dump
%attr(755, root, root) %{_bindir}/resolveip
%attr(755, root, root) %{_bindir}/wsrep_sst_common
%attr(755, root, root) %{_bindir}/wsrep_sst_mysqldump
%attr(755, root, root) %{_bindir}/wsrep_sst_xtrabackup
%attr(755, root, root) %{_bindir}/wsrep_sst_rsync
%attr(755, root, root) %{_bindir}/wsrep_sst_rsync_wan

%attr(755, root, root) %{_libexecdir}/mysqld
%attr(755, root, root) %{_libexecdir}/mysqld-debug
%attr(755, root, root) %{_sbindir}/rcmysql
%attr(755, root, root) %{_libdir}/mysql/plugin/daemon_example.ini
%attr(755, root, root) %{_libdir}/mysql/plugin/adt_null.so
%attr(755, root, root) %{_libdir}/mysql/plugin/libdaemon_example.so
%attr(755, root, root) %{_libdir}/mysql/plugin/mypluglib.so
%attr(755, root, root) %{_libdir}/mysql/plugin/semisync_master.so
%attr(755, root, root) %{_libdir}/mysql/plugin/semisync_slave.so
%attr(755, root, root) %{_libdir}/mysql/plugin/auth.so
%attr(755, root, root) %{_libdir}/mysql/plugin/auth_socket.so
%attr(755, root, root) %{_libdir}/mysql/plugin/auth_test_plugin.so
%attr(755, root, root) %{_libdir}/mysql/plugin/qa_auth_client.so
%attr(755, root, root) %{_libdir}/mysql/plugin/qa_auth_interface.so
%attr(755, root, root) %{_libdir}/mysql/plugin/qa_auth_server.so
%attr(755, root, root) %{_libdir}/mysql/plugin/auth_pam.so
%attr(755, root, root) %{_libdir}/mysql/plugin/auth_pam_compat.so
%attr(755, root, root) %{_libdir}/mysql/plugin/dialog.so
%attr(755, root, root) %{_libdir}/mysql/plugin/debug/adt_null.so
%attr(755, root, root) %{_libdir}/mysql/plugin/debug/libdaemon_example.so
%attr(755, root, root) %{_libdir}/mysql/plugin/debug/mypluglib.so
%attr(755, root, root) %{_libdir}/mysql/plugin/debug/semisync_master.so
%attr(755, root, root) %{_libdir}/mysql/plugin/debug/semisync_slave.so
%attr(755, root, root) %{_libdir}/mysql/plugin/debug/auth.so
%attr(755, root, root) %{_libdir}/mysql/plugin/debug/auth_socket.so
%attr(755, root, root) %{_libdir}/mysql/plugin/debug/auth_test_plugin.so
%attr(755, root, root) %{_libdir}/mysql/plugin/debug/qa_auth_client.so
%attr(755, root, root) %{_libdir}/mysql/plugin/debug/qa_auth_interface.so
%attr(755, root, root) %{_libdir}/mysql/plugin/debug/qa_auth_server.so
%attr(755, root, root) %{_libdir}/mysql/plugin/debug/auth_pam.so
%attr(755, root, root) %{_libdir}/mysql/plugin/debug/auth_pam_compat.so
%attr(755, root, root) %{_libdir}/mysql/plugin/debug/dialog.so
# HandlerSocket files
%attr(755, root, root) %{_libdir}/mysql/plugin/handlersocket.a
%attr(755, root, root) %{_libdir}/mysql/plugin/handlersocket.la
%attr(755, root, root) %{_libdir}/mysql/plugin/handlersocket.so
%attr(755, root, root) %{_libdir}/mysql/plugin/handlersocket.so.0
%attr(755, root, root) %{_libdir}/mysql/plugin/handlersocket.so.0.0.0
# UDF files
%attr(755, root, root) %{_libdir}/mysql/plugin/libfnv1a_udf.so
%attr(755, root, root) %{_libdir}/mysql/plugin/libfnv1a_udf.so.0
%attr(755, root, root) %{_libdir}/mysql/plugin/libfnv1a_udf.so.0.0.0
%attr(755, root, root) %{_libdir}/mysql/plugin/libfnv_udf.so
%attr(755, root, root) %{_libdir}/mysql/plugin/libfnv_udf.so.0
%attr(755, root, root) %{_libdir}/mysql/plugin/libfnv_udf.so.0.0.0
%attr(755, root, root) %{_libdir}/mysql/plugin/libmurmur_udf.so
%attr(755, root, root) %{_libdir}/mysql/plugin/libmurmur_udf.so.0
%attr(755, root, root) %{_libdir}/mysql/plugin/libmurmur_udf.so.0.0.0




%if %{WITH_TCMALLOC}
%attr(755, root, root) %{_libdir}/mysql/%{malloc_lib_target}
%endif

#%attr(644, root, root) %config(noreplace,missingok) %{_sysconfdir}/logrotate.d/mysqld
%{?scl:%_root_sysconfdir}%{!?scl:%_sysconfdir}/rc.d/init.d/%{?scl_prefix}mysqld
%config(noreplace) %{?scl:%_root_sysconfdir}%{!?scl:%_sysconfdir}/logrotate.d/%{?scl_prefix}mysqld
%config(noreplace) %{?scl:%_root_sysconfdir}%{!?scl:%_sysconfdir}/xinetd.d/%{?scl_prefix}mysqlchk

%attr(0755,mysql,mysql) %dir %{_localstatedir}/run/mysqld
%attr(0640,mysql,mysql) %config(noreplace) %verify(not md5 size mtime) /var/log/%{?scl_prefix}mysqld.log

#%{_datadir}/mysql/
#%attr(755, root, root) %{_datadir}/mysql/
%attr(755, root, root) %{_datadir}/mysql/SELinux/RHEL4/mysql.fc
%attr(755, root, root) %{_datadir}/mysql/SELinux/RHEL4/mysql.te
%attr(755, root, root) %{_datadir}/mysql/binary-configure
%attr(755, root, root) %{_datadir}/mysql/config.huge.ini
%attr(755, root, root) %{_datadir}/mysql/config.medium.ini
%attr(755, root, root) %{_datadir}/mysql/config.small.ini
%attr(755, root, root) %{_datadir}/mysql/errmsg-utf8.txt
%attr(755, root, root) %{_datadir}/mysql/fill_help_tables.sql
%attr(755, root, root) %{_datadir}/mysql/magic
%attr(755, root, root) %{_datadir}/mysql/my-huge.cnf
%attr(755, root, root) %{_datadir}/mysql/my-innodb-heavy-4G.cnf
%attr(755, root, root) %{_datadir}/mysql/my-large.cnf
%attr(755, root, root) %{_datadir}/mysql/my-medium.cnf
%attr(755, root, root) %{_datadir}/mysql/my-small.cnf
%attr(755, root, root) %{_datadir}/mysql/mysql-log-rotate
%attr(755, root, root) %{_datadir}/mysql/mysql.server
%attr(755, root, root) %{_datadir}/mysql/mysqlchk
%attr(755, root, root) %{_datadir}/mysql/mysql_system_tables.sql
%attr(755, root, root) %{_datadir}/mysql/mysql_system_tables_data.sql
%attr(755, root, root) %{_datadir}/mysql/mysql_test_data_timezone.sql
%attr(755, root, root) %{_datadir}/mysql/mysqld_multi.server
%attr(755, root, root) %{_datadir}/mysql/ndb-config-2-node.ini
%attr(755, root, root) %{_datadir}/mysql/wsrep.cnf
%attr(755, root, root) %{_datadir}/mysql/wsrep_notify

%attr(755, root, root) /usr/share/mysql/mcluster-bootstrap
%attr(755, root, root) {_bindir}/mcheck
%attr(0755,mysql,mysql) %dir %{mysqldatadir}


# ----------------------------------------------------------------------------
%files

%defattr(-, root, root, 0755)
%attr(755, root, root) %{_bindir}/msql2mysql
%attr(755, root, root) %{_bindir}/mysql
%attr(755, root, root) %{_bindir}/my_print_defaults
%attr(755, root, root) %{_bindir}/mysql_find_rows
%attr(755, root, root) %{_bindir}/mysql_waitpid
%attr(755, root, root) %{_bindir}/mysqlaccess
# XXX: This should be moved to %{_sysconfdir}
%attr(644, root, root) %{_bindir}/mysqlaccess.conf
%attr(755, root, root) %{_bindir}/mysqladmin
%attr(755, root, root) %{_bindir}/mysqlbinlog
%attr(755, root, root) %{_bindir}/mysqlcheck
%attr(755, root, root) %{_bindir}/mysqldump
%attr(755, root, root) %{_bindir}/mysqlimport
%attr(755, root, root) %{_bindir}/mysqlshow
%attr(755, root, root) %{_bindir}/mysqlslap
%attr(755, root, root) %{_bindir}/hsclient

%doc %attr(644, root, man) %{_mandir}/man1/msql2mysql.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysql.1*
%doc %attr(644, root, man) %{_mandir}/man1/my_print_defaults.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysql_find_rows.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysql_waitpid.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysqlaccess.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysqladmin.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysqlbinlog.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysqlcheck.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysqldump.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysqlimport.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysqlshow.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysqlslap.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysql_config.1*
%attr(755, root, root) %{_bindir}/mysql_config

# ----------------------------------------------------------------------------
%files devel -f optional-files-devel
%defattr(-, root, root, 0755)
%doc %attr(644, root, man) %{_mandir}/man1/comp_err.1*
%dir %attr(755, root, root) %{_includedir}/mysql
%dir %attr(755, root, root) %{_libdir}/mysql
%{_includedir}/mysql/*
%{_includedir}/handlersocket
%{_datadir}/aclocal/mysql.m4
%{_libdir}/mysql/libmysqlclient.a
%{_libdir}/mysql/libmysqlclient_r.a
%{_libdir}/mysql/libmysqlservices.a
%{_libdir}/mysql/libhsclient.a
%{_libdir}/libhsclient.la

# ----------------------------------------------------------------------------
%files libs
%defattr(-, root, root, 0755)
# Shared libraries (omit for architectures that don't support them)
#%{_libdir}/libmysql*.so*
%{_libdir}/mysql/libmysql*.so*
# Maatkit UDF libs
%{_libdir}/mysql/plugin/libfnv1a_udf.a
%{_libdir}/mysql/plugin/libfnv1a_udf.la
%{_libdir}/mysql/plugin/libfnv_udf.a
%{_libdir}/mysql/plugin/libfnv_udf.la
%{_libdir}/mysql/plugin/libmurmur_udf.a
%{_libdir}/mysql/plugin/libmurmur_udf.la

/etc/ld.so.conf.d/*

%config(noreplace) %{_sysconfdir}/my.cnf

%dir %{_datadir}/mysql
%{_datadir}/mysql/english
%lang(cs) %{_datadir}/mysql/czech
%lang(da) %{_datadir}/mysql/danish
%lang(nl) %{_datadir}/mysql/dutch
%lang(et) %{_datadir}/mysql/estonian
%lang(fr) %{_datadir}/mysql/french
%lang(de) %{_datadir}/mysql/german
%lang(el) %{_datadir}/mysql/greek
%lang(hu) %{_datadir}/mysql/hungarian
%lang(it) %{_datadir}/mysql/italian
%lang(ja) %{_datadir}/mysql/japanese
%lang(ko) %{_datadir}/mysql/korean
%lang(no) %{_datadir}/mysql/norwegian
%lang(no) %{_datadir}/mysql/norwegian-ny
%lang(pl) %{_datadir}/mysql/polish
%lang(pt) %{_datadir}/mysql/portuguese
%lang(ro) %{_datadir}/mysql/romanian
%lang(ru) %{_datadir}/mysql/russian
%lang(sr) %{_datadir}/mysql/serbian
%lang(sk) %{_datadir}/mysql/slovak
%lang(es) %{_datadir}/mysql/spanish
%lang(sv) %{_datadir}/mysql/swedish
%lang(uk) %{_datadir}/mysql/ukrainian
%{_datadir}/mysql/charsets

%files bench
%defattr(-,root,root)
%{_datadir}/sql-bench

# ----------------------------------------------------------------------------
%files test
%defattr(-, root, root, 0755)
%attr(-, root, root) %{_datadir}/mysql-test
%attr(755, root, root) %{_bindir}/mysql_client_test
#%attr(755, root, root) %{_bindir}/mysql_client_test_embedded
#%attr(755, root, root) %{_bindir}/mysqltest_embedded
%doc %attr(644, root, man) %{_mandir}/man1/mysql_client_test.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysql-stress-test.pl.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysql-test-run.pl.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysql_client_test_embedded.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysqltest_embedded.1*

##############################################################################
# The spec file changelog only includes changes made to the spec file
# itself - note that they must be ordered by date (important when
# merging BK trees)
##############################################################################
%changelog
* Tue Aug 27 2013 Albert Zhang <zhgwenming@gmail.com>
- SCL support

* Tue Aug 6 2013 Albert Zhang <zhgwenming@gamil.com>
- Change the default SST port to 4569
- ldconfig config file for mysql

* Thu Feb 10 2011 Ignacio Nin <ignacio.nin@percona.com>

- Removed lines which prevented -debuginfo packages from being built.

* Tue Nov 23 2010 Jonathan Perkin <jonathan.perkin@oracle.com>

- EXCEPTIONS-CLIENT has been deleted, remove it from here too
- Support MYSQL_BUILD_MAKE_JFLAG environment variable for passing
  a '-j' argument to make.

* Mon Nov 1 2010 Georgi Kodinov <georgi.godinov@oracle.com>

- Added test authentication (WL#1054) plugin binaries

* Wed Oct 6 2010 Georgi Kodinov <georgi.godinov@oracle.com>

- Added example external authentication (WL#1054) plugin binaries

* Wed Aug 11 2010 Joerg Bruehe <joerg.bruehe@oracle.com>

- With a recent spec file cleanup, names have changed: A "-community" part was dropped.
  Reflect that in the "Obsoletes" specifications.
- Add a "triggerpostun" to handle the uninstall of the "-community" server RPM.
- This fixes bug#55015 "MySQL server is not restarted properly after RPM upgrade".

* Tue Jun 15 2010 Joerg Bruehe <joerg.bruehe@sun.com>

- Change the behaviour on installation and upgrade:
  On installation, do not autostart the server.
  *Iff* the server was stopped before the upgrade is started, this is taken as a
  sign the administrator is handling that manually, and so the new server will
  not be started automatically at the end of the upgrade.
  The start/stop scripts will still be installed, so the server will be started
  on the next machine boot.
  This is the 5.5 version of fixing bug#27072 (RPM autostarting the server).

* Tue Jun 1 2010 Jonathan Perkin <jonathan.perkin@oracle.com>

- Implement SELinux checks from distribution-specific spec file.

* Wed May 12 2010 Jonathan Perkin <jonathan.perkin@oracle.com>

- Large number of changes to build using CMake
- Introduce distribution-specific RPMs
- Drop debuginfo, build all binaries with debug/symbols
- Remove __os_install_post, use native macro
- Remove _unpackaged_files_terminate_build, make it an error to have
  unpackaged files
- Remove cluster RPMs

* Wed Mar 24 2010 Joerg Bruehe <joerg.bruehe@sun.com>

- Add "--with-perfschema" to the configure options.

* Mon Mar 22 2010 Joerg Bruehe <joerg.bruehe@sun.com>

- User "usr/lib*" to allow for both "usr/lib" and "usr/lib64",
  mask "rmdir" return code 1.
- Remove "ha_example.*" files from the list, they aren't built.

* Wed Mar 17 2010 Joerg Bruehe <joerg.bruehe@sun.com>

- Fix a wrong path name in handling the debug plugins.

* Wed Mar 10 2010 Joerg Bruehe <joerg.bruehe@sun.com>

- Take the result of the debug plugin build and put it into the optimized tree,
  so that it becomes part of the final installation;
  include the files in the packlist. Part of the fixes for bug#49022.

* Mon Mar 01 2010 Joerg Bruehe <joerg.bruehe@sun.com>

- Set "Oracle and/or its affiliates" as the vendor and copyright owner,
  accept upgrading from packages showing MySQL or Sun as vendor.

* Fri Feb 12 2010 Joerg Bruehe <joerg.bruehe@sun.com>

- Formatting changes:
  Have a consistent structure of separator lines and of indentation
  (8 leading blanks => tab).
- Introduce the variable "src_dir".
- Give the environment variables "MYSQL_BUILD_CC(CXX)" precedence
  over "CC" ("CXX").
- Drop the old "with_static" argument analysis, this is not supported
  in 5.1 since ages.
- Introduce variables to control the handlers individually, as well
  as other options.
- Use the new "--with-plugin" notation for the table handlers.
- Drop handling "/etc/rc.d/init.d/mysql", the switch to "/etc/init.d/mysql"
  was done back in 2002 already.
- Make "--with-zlib-dir=bundled" the default, add an option to disable it.
- Add missing manual pages to the file list.
- Improve the runtime check for "libgcc.a", protect it against being tried
  with the Intel compiler "icc".

* Mon Jan 11 2010 Joerg Bruehe <joerg.bruehe@sun.com>

- Change RPM file naming:
  - Suffix like "-m2", "-rc" becomes part of version as "_m2", "_rc".
  - Release counts from 1, not 0.

* Wed Dec 23 2009 Joerg Bruehe <joerg.bruehe@sun.com>

- The "semisync" plugin file name has lost its introductory "lib",
  adapt the file lists for the subpackages.
  This is a part missing from the fix for bug#48351.
- Remove the "fix_privilege_tables" manual, it does not exist in 5.5
  (and likely, the whole script will go, too).

* Mon Nov 16 2009 Joerg Bruehe <joerg.bruehe@sun.com>

- Fix some problems with the directives around "tcmalloc" (experimental),
  remove erroneous traces of the InnoDB plugin (that is 5.1 only).

* Fri Oct 06 2009 Magnus Blaudd <mvensson@mysql.com>

- Removed mysql_fix_privilege_tables

* Fri Oct 02 2009 Alexander Nozdrin <alexander.nozdrin@sun.com>

- "mysqlmanager" got removed from version 5.4, all references deleted.

* Fri Aug 28 2009 Joerg Bruehe <joerg.bruehe@sun.com>

- Merge up from 5.1 to 5.4: Remove handling for the InnoDB plugin.

* Thu Aug 27 2009 Joerg Bruehe <joerg.bruehe@sun.com>

- This version does not contain the "Instance manager", "mysqlmanager":
  Remove it from the spec file so that packaging succeeds.

* Mon Aug 24 2009 Jonathan Perkin <jperkin@sun.com>

- Add conditionals for bundled zlib and innodb plugin

* Fri Aug 21 2009 Jonathan Perkin <jperkin@sun.com>

- Install plugin libraries in appropriate packages.
- Disable libdaemon_example and ftexample plugins.

* Thu Aug 20 2009 Jonathan Perkin <jperkin@sun.com>

- Update variable used for mysql-test suite location to match source.

* Fri Nov 07 2008 Joerg Bruehe <joerg@mysql.com>

- Correct yesterday's fix, so that it also works for the last flag,
  and fix a wrong quoting: un-quoted quote marks must not be escaped.

* Thu Nov 06 2008 Kent Boortz <kent.boortz@sun.com>

- Removed "mysql_upgrade_shell"
- Removed some copy/paste between debug and normal build

* Thu Nov 06 2008 Joerg Bruehe <joerg@mysql.com>

- Modify CFLAGS and CXXFLAGS such that a debug build is not optimized.
  This should cover both gcc and icc flags.  Fixes bug#40546.

* Fri Aug 29 2008 Kent Boortz <kent@mysql.com>

- Removed the "Federated" storage engine option, and enabled in all

* Tue Aug 26 2008 Joerg Bruehe <joerg@mysql.com>

- Get rid of the "warning: Installed (but unpackaged) file(s) found:"
  Some generated files aren't needed in RPMs:
  - the "sql-bench/" subdirectory
  Some files were missing:
  - /usr/share/aclocal/mysql.m4  ("devel" subpackage)
  - Manual "mysqlbug" ("server" subpackage)
  - Program "innochecksum" and its manual ("server" subpackage)
  - Manual "mysql_find_rows" ("client" subpackage)
  - Script "mysql_upgrade_shell" ("client" subpackage)
  - Program "ndb_cpcd" and its manual ("ndb-extra" subpackage)
  - Manuals "ndb_mgm" + "ndb_restore" ("ndb-tools" subpackage)

* Mon Mar 31 2008 Kent Boortz <kent@mysql.com>

- Made the "Federated" storage engine an option
- Made the "Cluster" storage engine and sub packages an option

* Wed Mar 19 2008 Joerg Bruehe <joerg@mysql.com>

- Add the man pages for "ndbd" and "ndb_mgmd".

* Mon Feb 18 2008 Timothy Smith <tim@mysql.com>

- Require a manual upgrade if the alread-installed mysql-server is
  from another vendor, or is of a different major version.

* Wed May 02 2007 Joerg Bruehe <joerg@mysql.com>

- "ndb_size.tmpl" is not needed any more,
  "man1/mysql_install_db.1" lacked the trailing '*'.

* Sat Apr 07 2007 Kent Boortz <kent@mysql.com>

- Removed man page for "mysql_create_system_tables"

* Wed Mar 21 2007 Daniel Fischer <df@mysql.com>

- Add debug server.

* Mon Mar 19 2007 Daniel Fischer <df@mysql.com>

- Remove Max RPMs; the server RPMs contain a mysqld compiled with all
  features that previously only were built into Max.

* Fri Mar 02 2007 Joerg Bruehe <joerg@mysql.com>

- Add several man pages for NDB which are now created.

* Fri Jan 05 2007 Kent Boortz <kent@mysql.com>

- Put back "libmygcc.a", found no real reason it was removed.

- Add CFLAGS to gcc call with --print-libgcc-file, to make sure the
  correct "libgcc.a" path is returned for the 32/64 bit architecture.

* Mon Dec 18 2006 Joerg Bruehe <joerg@mysql.com>

- Fix the move of "mysqlmanager" to section 8: Directory name was wrong.

* Thu Dec 14 2006 Joerg Bruehe <joerg@mysql.com>

- Include the new man pages for "my_print_defaults" and "mysql_tzinfo_to_sql"
  in the server RPM.
- The "mysqlmanager" man page got moved from section 1 to 8.

* Thu Nov 30 2006 Joerg Bruehe <joerg@mysql.com>

- Call "make install" using "benchdir_root=%{_datadir}",
  because that is affecting the regression test suite as well.

* Thu Nov 16 2006 Joerg Bruehe <joerg@mysql.com>

- Explicitly note that the "MySQL-shared" RPMs (as built by MySQL AB)
  replace "mysql-shared" (as distributed by SuSE) to allow easy upgrading
  (bug#22081).

* Mon Nov 13 2006 Joerg Bruehe <joerg@mysql.com>

- Add "--with-partition" to all server builds.

- Use "--report-features" in one test run per server build.

* Tue Aug 15 2006 Joerg Bruehe <joerg@mysql.com>

- The "max" server is removed from packages, effective from 5.1.12-beta.
  Delete all steps to build, package, or install it.

* Mon Jul 10 2006 Joerg Bruehe <joerg@mysql.com>

- Fix a typing error in the "make" target for the Perl script to run the tests.

* Tue Jul 04 2006 Joerg Bruehe <joerg@mysql.com>

- Use the Perl script to run the tests, because it will automatically check
  whether the server is configured with SSL.

* Tue Jun 27 2006 Joerg Bruehe <joerg@mysql.com>

- move "mysqldumpslow" from the client RPM to the server RPM (bug#20216)

- Revert all previous attempts to call "mysql_upgrade" during RPM upgrade,
  there are some more aspects which need to be solved before this is possible.
  For now, just ensure the binary "mysql_upgrade" is delivered and installed.

* Thu Jun 22 2006 Joerg Bruehe <joerg@mysql.com>

- Close a gap of the previous version by explicitly using
  a newly created temporary directory for the socket to be used
  in the "mysql_upgrade" operation, overriding any local setting.

* Tue Jun 20 2006 Joerg Bruehe <joerg@mysql.com>

- To run "mysql_upgrade", we need a running server;
  start it in isolation and skip password checks.

* Sat May 20 2006 Kent Boortz <kent@mysql.com>

- Always compile for PIC, position independent code.

* Wed May 10 2006 Kent Boortz <kent@mysql.com>

- Use character set "all" when compiling with Cluster, to make Cluster
  nodes independent on the character set directory, and the problem
  that two RPM sub packages both wants to install this directory.

* Mon May 01 2006 Kent Boortz <kent@mysql.com>

- Use "./libtool --mode=execute" instead of searching for the
  executable in current directory and ".libs".

* Fri Apr 28 2006 Kent Boortz <kent@mysql.com>

- Install and run "mysql_upgrade"

* Wed Apr 12 2006 Jim Winstead <jimw@mysql.com>

- Remove sql-bench, and MySQL-bench RPM (will be built as an independent
  project from the mysql-bench repository)

* Tue Apr 11 2006 Jim Winstead <jimw@mysql.com>

- Remove old mysqltestmanager and related programs
* Sat Apr 01 2006 Kent Boortz <kent@mysql.com>

- Set $LDFLAGS from $MYSQL_BUILD_LDFLAGS

* Wed Mar 07 2006 Kent Boortz <kent@mysql.com>

- Changed product name from "Community Edition" to "Community Server"

* Mon Mar 06 2006 Kent Boortz <kent@mysql.com>

- Fast mutexes is now disabled by default, but should be
  used in Linux builds.

* Mon Feb 20 2006 Kent Boortz <kent@mysql.com>

- Reintroduced a max build
- Limited testing of 'debug' and 'max' servers
- Berkeley DB only in 'max'

* Mon Feb 13 2006 Joerg Bruehe <joerg@mysql.com>

- Use "-i" on "make test-force";
  this is essential for later evaluation of this log file.

* Thu Feb 09 2006 Kent Boortz <kent@mysql.com>

- Pass '-static' to libtool, link static with our own libraries, dynamic
  with system libraries.  Link with the bundled zlib.

* Wed Feb 08 2006 Kristian Nielsen <knielsen@mysql.com>

- Modified RPM spec to match new 5.1 debug+max combined community packaging.

* Sun Dec 18 2005 Kent Boortz <kent@mysql.com>

- Added "client/mysqlslap"

* Mon Dec 12 2005 Rodrigo Novo <rodrigo@mysql.com>

- Added zlib to the list of (static) libraries installed
- Added check against libtool wierdness (WRT: sql/mysqld || sql/.libs/mysqld)
- Compile MySQL with bundled zlib
- Fixed %packager name to "MySQL Production Engineering Team"

* Mon Dec 05 2005 Joerg Bruehe <joerg@mysql.com>

- Avoid using the "bundled" zlib on "shared" builds:
  As it is not installed (on the build system), this gives dependency
  problems with "libtool" causing the build to fail.
  (Change was done on Nov 11, but left uncommented.)

* Tue Nov 22 2005 Joerg Bruehe <joerg@mysql.com>

- Extend the file existence check for "init.d/mysql" on un-install
  to also guard the call to "insserv"/"chkconfig".

* Thu Oct 27 2005 Lenz Grimmer <lenz@grimmer.com>

- added more man pages

* Wed Oct 19 2005 Kent Boortz <kent@mysql.com>

- Made yaSSL support an option (off by default)

* Wed Oct 19 2005 Kent Boortz <kent@mysql.com>

- Enabled yaSSL support

* Sat Oct 15 2005 Kent Boortz <kent@mysql.com>

- Give mode arguments the same way in all places
- Moved copy of mysqld.a to "standard" build, but
  disabled it as we don't do embedded yet in 5.0

* Fri Oct 14 2005 Kent Boortz <kent@mysql.com>

- For 5.x, always compile with --with-big-tables
- Copy the config.log file to location outside
  the build tree

* Fri Oct 14 2005 Kent Boortz <kent@mysql.com>

- Removed unneeded/obsolete configure options
- Added archive engine to standard server
- Removed the embedded server from experimental server
- Changed suffix "-Max" => "-max"
- Changed comment string "Max" => "Experimental"

* Thu Oct 13 2005 Lenz Grimmer <lenz@mysql.com>

- added a usermod call to assign a potential existing mysql user to the
  correct user group (BUG#12823)
- Save the perror binary built during Max build so it supports the NDB
  error codes (BUG#13740)
- added a separate macro "mysqld_group" to be able to define the
  user group of the mysql user seperately, if desired.

* Thu Sep 29 2005 Lenz Grimmer <lenz@mysql.com>

- fixed the removing of the RPM_BUILD_ROOT in the %clean section (the
  %{buildroot} variable did not get expanded, thus leaving old build roots behind)

* Thu Aug 04 2005 Lenz Grimmer <lenz@mysql.com>

- Fixed the creation of the mysql user group account in the postinstall
  section (BUG 12348)
- Fixed enabling the Archive storage engine in the Max binary

* Tue Aug 02 2005 Lenz Grimmer <lenz@mysql.com>

- Fixed the Requires: tag for the server RPM (BUG 12233)

* Fri Jul 15 2005 Lenz Grimmer <lenz@mysql.com>

- create a "mysql" user group and assign the mysql user account to that group
  in the server postinstall section. (BUG 10984)

* Tue Jun 14 2005 Lenz Grimmer <lenz@mysql.com>

- Do not build statically on i386 by default, only when adding either "--with
  static" or "--define '_with_static 1'" to the RPM build options. Static
  linking really only makes sense when linking against the specially patched
  glibc 2.2.5.

* Mon Jun 06 2005 Lenz Grimmer <lenz@mysql.com>

- added mysql_client_test to the "bench" subpackage (BUG 10676)
- added the libndbclient static and shared libraries (BUG 10676)

* Wed Jun 01 2005 Lenz Grimmer <lenz@mysql.com>

- use "mysqldatadir" variable instead of hard-coding the path multiple times
- use the "mysqld_user" variable on all occasions a user name is referenced
- removed (incomplete) Brazilian translations
- removed redundant release tags from the subpackage descriptions

* Wed May 25 2005 Joerg Bruehe <joerg@mysql.com>

- Added a "make clean" between separate calls to "BuildMySQL".

* Thu May 12 2005 Guilhem Bichot <guilhem@mysql.com>

- Removed the mysql_tableinfo script made obsolete by the information schema

* Wed Apr 20 2005 Lenz Grimmer <lenz@mysql.com>

- Enabled the "blackhole" storage engine for the Max RPM

* Wed Apr 13 2005 Lenz Grimmer <lenz@mysql.com>

- removed the MySQL manual files (html/ps/texi) - they have been removed
  from the MySQL sources and are now available seperately.

* Mon Apr 4 2005 Petr Chardin <petr@mysql.com>

- old mysqlmanager, mysqlmanagerc and mysqlmanager-pwger renamed into
  mysqltestmanager, mysqltestmanager and mysqltestmanager-pwgen respectively

* Fri Mar 18 2005 Lenz Grimmer <lenz@mysql.com>

- Disabled RAID in the Max binaries once and for all (it has finally been
  removed from the source tree)

* Sun Feb 20 2005 Petr Chardin <petr@mysql.com>

- Install MySQL Instance Manager together with mysqld, touch mysqlmanager
  password file

* Mon Feb 14 2005 Lenz Grimmer <lenz@mysql.com>

- Fixed the compilation comments and moved them into the separate build sections
  for Max and Standard

* Mon Feb 7 2005 Tomas Ulin <tomas@mysql.com>

- enabled the "Ndbcluster" storage engine for the max binary
- added extra make install in ndb subdir after Max build to get ndb binaries
- added packages for ndbcluster storage engine

* Fri Jan 14 2005 Lenz Grimmer <lenz@mysql.com>

- replaced obsoleted "BuildPrereq" with "BuildRequires" instead

* Thu Jan 13 2005 Lenz Grimmer <lenz@mysql.com>

- enabled the "Federated" storage engine for the max binary

* Tue Jan 04 2005 Petr Chardin <petr@mysql.com>

- ISAM and merge storage engines were purged. As well as appropriate
  tools and manpages (isamchk and isamlog)

* Thu Dec 31 2004 Lenz Grimmer <lenz@mysql.com>

- enabled the "Archive" storage engine for the max binary
- enabled the "CSV" storage engine for the max binary
- enabled the "Example" storage engine for the max binary

* Thu Aug 26 2004 Lenz Grimmer <lenz@mysql.com>

- MySQL-Max now requires MySQL-server instead of MySQL (BUG 3860)

* Fri Aug 20 2004 Lenz Grimmer <lenz@mysql.com>

- do not link statically on IA64/AMD64 as these systems do not have
  a patched glibc installed

* Tue Aug 10 2004 Lenz Grimmer <lenz@mysql.com>

- Added libmygcc.a to the devel subpackage (required to link applications
  against the the embedded server libmysqld.a) (BUG 4921)

* Mon Aug 09 2004 Lenz Grimmer <lenz@mysql.com>

- Added EXCEPTIONS-CLIENT to the "devel" package

* Thu Jul 29 2004 Lenz Grimmer <lenz@mysql.com>

- disabled OpenSSL in the Max binaries again (the RPM packages were the
  only exception to this anyway) (BUG 1043)

* Wed Jun 30 2004 Lenz Grimmer <lenz@mysql.com>

- fixed server postinstall (mysql_install_db was called with the wrong
  parameter)

* Thu Jun 24 2004 Lenz Grimmer <lenz@mysql.com>

- added mysql_tzinfo_to_sql to the server subpackage
- run "make clean" instead of "make distclean"

* Mon Apr 05 2004 Lenz Grimmer <lenz@mysql.com>

- added ncurses-devel to the build prerequisites (BUG 3377)

* Thu Feb 12 2004 Lenz Grimmer <lenz@mysql.com>

- when using gcc, _always_ use CXX=gcc
- replaced Copyright with License field (Copyright is obsolete)

* Tue Feb 03 2004 Lenz Grimmer <lenz@mysql.com>

- added myisam_ftdump to the Server package

* Tue Jan 13 2004 Lenz Grimmer <lenz@mysql.com>

- link the mysql client against libreadline instead of libedit (BUG 2289)

* Mon Dec 22 2003 Lenz Grimmer <lenz@mysql.com>

- marked /etc/logrotate.d/mysql as a config file (BUG 2156)

* Fri Dec 13 2003 Lenz Grimmer <lenz@mysql.com>

- fixed file permissions (BUG 1672)

* Thu Dec 11 2003 Lenz Grimmer <lenz@mysql.com>

- made testing for gcc3 a bit more robust

* Fri Dec 05 2003 Lenz Grimmer <lenz@mysql.com>

- added missing file mysql_create_system_tables to the server subpackage

* Fri Nov 21 2003 Lenz Grimmer <lenz@mysql.com>

- removed dependency on MySQL-client from the MySQL-devel subpackage
  as it is not really required. (BUG 1610)

* Fri Aug 29 2003 Lenz Grimmer <lenz@mysql.com>

- Fixed BUG 1162 (removed macro names from the changelog)
- Really fixed BUG 998 (disable the checking for installed but
  unpackaged files)

* Tue Aug 05 2003 Lenz Grimmer <lenz@mysql.com>

- Fixed BUG 959 (libmysqld not being compiled properly)
- Fixed BUG 998 (RPM build errors): added missing files to the
  distribution (mysql_fix_extensions, mysql_tableinfo, mysqldumpslow,
  mysql_fix_privilege_tables.1), removed "-n" from install section.

* Wed Jul 09 2003 Lenz Grimmer <lenz@mysql.com>

- removed the GIF Icon (file was not included in the sources anyway)
- removed unused variable shared_lib_version
- do not run automake before building the standard binary
  (should not be necessary)
- add server suffix '-standard' to standard binary (to be in line
  with the binary tarball distributions)
- Use more RPM macros (_exec_prefix, _sbindir, _libdir, _sysconfdir,
  _datadir, _includedir) throughout the spec file.
- allow overriding CC and CXX (required when building with other compilers)

* Fri May 16 2003 Lenz Grimmer <lenz@mysql.com>

- re-enabled RAID again

* Wed Apr 30 2003 Lenz Grimmer <lenz@mysql.com>

- disabled MyISAM RAID (--with-raid) - it throws an assertion which
  needs to be investigated first.

* Mon Mar 10 2003 Lenz Grimmer <lenz@mysql.com>

- added missing file mysql_secure_installation to server subpackage
  (BUG 141)

* Tue Feb 11 2003 Lenz Grimmer <lenz@mysql.com>

- re-added missing pre- and post(un)install scripts to server subpackage
- added config file /etc/my.cnf to the file list (just for completeness)
- make sure to create the datadir with 755 permissions

* Mon Jan 27 2003 Lenz Grimmer <lenz@mysql.com>

- removed unused CC and CXX variables
- CFLAGS and CXXFLAGS should honor RPM_OPT_FLAGS

* Fri Jan 24 2003 Lenz Grimmer <lenz@mysql.com>

- renamed package "MySQL" to "MySQL-server"
- fixed Copyright tag
- added mysql_waitpid to client subpackage (required for mysql-test-run)

* Wed Nov 27 2002 Lenz Grimmer <lenz@mysql.com>

- moved init script from /etc/rc.d/init.d to /etc/init.d (the majority of
  Linux distributions now support this scheme as proposed by the LSB either
  directly or via a compatibility symlink)
- Use new "restart" init script action instead of starting and stopping
  separately
- Be more flexible in activating the automatic bootup - use insserv (on
  older SuSE versions) or chkconfig (Red Hat, newer SuSE versions and
  others) to create the respective symlinks

* Wed Sep 25 2002 Lenz Grimmer <lenz@mysql.com>

- MySQL-Max now requires MySQL >= 4.0 to avoid version mismatches
  (mixing 3.23 and 4.0 packages)

* Fri Aug 09 2002 Lenz Grimmer <lenz@mysql.com>

- Turn off OpenSSL in MySQL-Max for now until it works properly again
- enable RAID for the Max binary instead
- added compatibility link: safe_mysqld -> mysqld_safe to ease the
  transition from 3.23

* Thu Jul 18 2002 Lenz Grimmer <lenz@mysql.com>

- Reworked the build steps a little bit: the Max binary is supposed
  to include OpenSSL, which cannot be linked statically, thus trying
  to statically link against a special glibc is futile anyway
- because of this, it is not required to make yet another build run
  just to compile the shared libs (saves a lot of time)
- updated package description of the Max subpackage
- clean up the BuildRoot directory afterwards

* Mon Jul 15 2002 Lenz Grimmer <lenz@mysql.com>

- Updated Packager information
- Fixed the build options: the regular package is supposed to
  include InnoDB and linked statically, while the Max package
  should include BDB and SSL support

* Fri May 03 2002 Lenz Grimmer <lenz@mysql.com>

- Use more RPM macros (e.g. infodir, mandir) to make the spec
  file more portable
- reorganized the installation of documentation files: let RPM
  take care of this
- reorganized the file list: actually install man pages along
  with the binaries of the respective subpackage
- do not include libmysqld.a in the devel subpackage as well, if we
  have a special "embedded" subpackage
- reworked the package descriptions

* Mon Oct  8 2001 Monty

- Added embedded server as a separate RPM

* Fri Apr 13 2001 Monty

- Added mysqld-max to the distribution

* Tue Jan 2  2001  Monty

- Added mysql-test to the bench package

* Fri Aug 18 2000 Tim Smith <tim@mysql.com>

- Added separate libmysql_r directory; now both a threaded
  and non-threaded library is shipped.

* Wed Sep 28 1999 David Axmark <davida@mysql.com>

- Added the support-files/my-example.cnf to the docs directory.

- Removed devel dependency on base since it is about client
  development.

* Wed Sep 8 1999 David Axmark <davida@mysql.com>

- Cleaned up some for 3.23.

* Thu Jul 1 1999 David Axmark <davida@mysql.com>

- Added support for shared libraries in a separate sub
  package. Original fix by David Fox (dsfox@cogsci.ucsd.edu)

- The --enable-assembler switch is now automatically disables on
  platforms there assembler code is unavailable. This should allow
  building this RPM on non i386 systems.

* Mon Feb 22 1999 David Axmark <david@detron.se>

- Removed unportable cc switches from the spec file. The defaults can
  now be overridden with environment variables. This feature is used
  to compile the official RPM with optimal (but compiler version
  specific) switches.

- Removed the repetitive description parts for the sub rpms. Maybe add
  again if RPM gets a multiline macro capability.

- Added support for a pt_BR translation. Translation contributed by
  Jorge Godoy <jorge@bestway.com.br>.

* Wed Nov 4 1998 David Axmark <david@detron.se>

- A lot of changes in all the rpm and install scripts. This may even
  be a working RPM :-)

* Sun Aug 16 1998 David Axmark <david@detron.se>

- A developers changelog for MySQL is available in the source RPM. And
  there is a history of major user visible changed in the Reference
  Manual.  Only RPM specific changes will be documented here.
