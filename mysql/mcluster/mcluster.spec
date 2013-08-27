%scl_package %scl

Summary: Package that installs %scl
Name: %scl_name
Version: 1
Release: 1%{?dist}
License: GPLv2+
Requires: %{scl_prefix}mysql
BuildRequires: scl-utils-build

%description
This is the main package for %scl Software Collection.

%package runtime
Summary: Package that handles %scl Software Collection.
Requires: scl-utils

%description runtime
Package shipping essential scripts to work with %scl Software Collection.

%package build
Summary: Package shipping basic build configuration

%description build
Package shipping essential configuration macros to build %scl Software Collection.

%prep
%setup -c -T

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_scl_scripts}/root
cat >> %{buildroot}%{_scl_scripts}/enable << EOF
export PATH=%{_bindir}\${PATH:+:\${PATH}}
export LD_LIBRARY_PATH=%{_libdir}\${LD_LIBRARY_PATH:+:\${LD_LIBRARY_PATH}}
export MANPATH=%{_mandir}\${MANPATH:+:\${MANPATH}}
export PKG_CONFIG_PATH=%{_libdir}/pkgconfig\${PKG_CONFIG_PATH:+:\${PKG_CONFIG_PATH}}
EOF

cat >> %{buildroot}%{_scl_scripts}/service-environment << EOF
MCLUSTER_MYSQLD_SCLS_ENABLED="%{scl}"
EOF
%scl_install

%files

%files runtime
%scl_files

%files build
%{_root_sysconfdir}/rpm/macros.%{scl}-config

%changelog
* Tue Aug 27 2013 Albert Zhang <zhgwenming@gmail.com>
- Initial package
