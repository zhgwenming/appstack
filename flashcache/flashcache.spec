Summary: A write-back block cache for Linux
Name: flashcache
Vendor: flashcache development, https://github.com/facebook/flashcache
Version: 1.0.20131209git
Release: letv.3%{?dist}
License: GPL
Group: System Environment/Base
URL: https://github.com/facebook/flashcache/
Packager: Hajime Taira <htaira@redhat.com>
Source0: %{name}-%{version}.tar.gz
Patch0: flashcache-sysvinit.patch
Requires(post): /sbin/chkconfig
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: x86_64
BuildRequires: tar gcc make kernel-devel rpm-build
ExclusiveArch: x86_64

%description
Flashcache : A write-back block cache for Linux


%kernel_module_package

%prep
%setup -q
%patch0 -p1
grep 'shell git describe  --always --abbrev=12' * -rl | xargs sed -i 's/$(shell git describe  --always --abbrev=12)/1.0-149-g4897daafe73c/'

%build
cd src/

for flavor in %flavors_to_build ; do
	make KERNEL_TREE=%{kernel_source $flavor}
done

%install
export INSTALL_MOD_PATH=$RPM_BUILD_ROOT
export INSTALL_MOD_DIR=extra/%{name}
for flavor in %flavors_to_build ; do
	make -C %{kernel_source $flavor} modules_install \
		M=$PWD/src
done

#install -m 0755 -d %{buildroot}/%{kernel_moduledir}/extra/flashcache
#install -m 0755 src/flashcache.ko %{buildroot}/%{kernel_moduledir}/extra/flashcache/
#install -m 0755 flashcache-wt/src/flashcache-wt.ko %{buildroot}/%{kernel_moduledir}/extra/flashcache/
install -m 0755 -d %{buildroot}/sbin
install -m 0755 src/utils/flashcache_create %{buildroot}/sbin/
install -m 0755 src/utils/flashcache_destroy %{buildroot}/sbin/
install -m 0755 src/utils/flashcache_load %{buildroot}/sbin/
#install -m 0755 flashcache-wt/src/utils/flashcache_wt_create %{buildroot}/sbin/
install -m 0755 -d %{buildroot}/%{_sysconfdir}/rc.d/init.d
install -m 0755 -d %{buildroot}/%{_sysconfdir}/sysconfig
install -m 0755 src/sysvinit/flashcache %{buildroot}/%{_sysconfdir}/rc.d/init.d/flashcache
install -m 0644 src/sysconfig/flashcache %{buildroot}/%{_sysconfdir}/sysconfig/flashcache
install -m 0755 -d %{buildroot}/usr/share/doc/%{name}-%{version}
install -m 0644 doc/flashcache-doc.txt %{buildroot}/usr/share/doc/%{name}-%{version}/
install -m 0644 doc/flashcache-sa-guide.txt %{buildroot}/usr/share/doc/%{name}-%{version}/
install -m 0644 README %{buildroot}/usr/share/doc/%{name}-%{version}/

%clean
rm -rf %{buildroot}

%files
/sbin/*
/usr/share/doc/%{name}-%{version}/*
%{_sysconfdir}/rc.d/init.d/flashcache
%config(noreplace) %{_sysconfdir}/sysconfig/flashcache

%post
chkconfig --add flashcache

%changelog
* Mon Sep 11 2013 10:46:11 +0800 Wenming Zhang <zhangwenming@letv.com> 
- Dup mode

* Mon Apr 23 2012 10:46:11 +0800 Wenming Zhang <zhangwenming@letv.com> 
- set the default associativiy to 4096 for write around mode

* Mon Apr 16 2012 11:05:09 +0800 Wenming Zhang <zhangwenming@letv.com> 
- make Makefile supports branches

* Fri Apr 6 2012 15:39:08 +0800 Wenming Zhang <zhangwenming@letv.com> 
- Switch to personal repo for letv

* Tue Mar 20 2012 12:39:15 +0800 Wenming Zhang <zhangwenming@letv.com> 
- flashcache initscript update to make it work with write-through/back/around mode

* Tue Mar 20 2012 10:24:35 +0800 Wenming Zhang <zhangwenming@letv.com> 
- remove dependencies from spec file

* Tue Mar 20 2012 10:19:15 +0800 Wenming Zhang <zhangwenming@letv.com> 
- Fix long kmod name with kernel version

* Mon Mar 19 2012 23:34:29 +0800 Wenming Zhang <zhgwenming@gmail.com> 
- fix README installation issue

* Mon Mar 19 2012 23:27:08 +0800 Wenming Zhang <zhgwenming@gmail.com> 
- Change package tag to letv

* Mon Mar 19 2012 23:22:54 +0800 Wenming Zhang <zhgwenming@gmail.com> 
- fix COMMIT_REV issue which needs a complete git tree

* Mon Mar 19 2012 22:47:36 +0800 Wenming Zhang <zhgwenming@gmail.com> 
- Makefile update for building srpm from git tree

* Mon Mar 19 2012 16:43:56 +0800 Wenming Zhang <zhangwenming@letv.com> 
- Initial flashcache project

* Thu Feb 03 2011 13:00:00 +09:00 Hajime Taira <htaira@redhat.com>
- Split RPM package: flashcache and kmod-flashcache-<uname -r>

* Sun Dec 05 2010 13:00:00 +09:00 Hajime Taira <htaira@redhat.com>
- Initial build.
