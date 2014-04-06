Name: pcs		
Version: 0.9.90
Release: 902.2%{?dist}.2
License: GPLv2
URL: http://github.com/feist/pcs
Group: System Environment/Base
BuildArch: noarch
BuildRequires: python2-devel
Summary: Pacemaker Configuration System	
Source0: http://people.redhat.com/cfeist/pcs/pcs-%{version}.tar.gz
Patch1: pcs/bz1032161-Node-standby-should-use-pacemaker-list-not-corosync-.patch
Patch2: bz1038478-Added-ability-to-set-and-remove-uidgid-for-RHEL6.patch
Patch3: bz1038479-Fix-for-adding-verify-stonith-levels-on-RHEL6.patch
Patch900: pcs-transport.patch
Patch901: pcs-transport-cman.patch
Patch999: pcs-0.9.90-clones-utils.py.patch

Requires: pacemaker
Requires: ccs >= 0.16.2-69.el6_5.1	

%description
pcs is a corosync and pacemaker configuration tool.  It permits users to
easily view, modify and created pacemaker based clusters.

%prep
%setup -q
%patch1 -p1 -b .bz1032161
%patch2 -p1 -b .bz1038478
%patch3 -p1 -b .bz1038479
%patch900 -p1 -b .transport
%patch901 -p1 -b .cman
%patch999 -p1

%build


%install
rm -rf $RPM_BUILD_ROOT
pwd
make install DESTDIR=$RPM_BUILD_ROOT PYTHON_SITELIB=%{python_sitelib}
chmod 755 $RPM_BUILD_ROOT/%{python_sitelib}/pcs/pcs.py


%files
%defattr(-,root,root,-)
%{python_sitelib}/pcs
%{python_sitelib}/pcs-%{version}-py2.*.egg-info
/usr/sbin/pcs
/etc/bash_completion.d/pcs
%{_mandir}/man8/pcs.*

%doc COPYING README

%changelog
* Tue Dec 17 2013 Johnny Hughes <johnny@centos.org> - 0.9.90-2.el6.centos.2
- Modify to run on CentOS 6 as well as RHEL 6

* Fri Dec 06 2013 Chris Feist <cfeist@redhat.com> - 0.9.90-2.el6_5.2
- Fixed bug causing an issue when adding stonith level without --force
- Added ability to create/edit/remove uidgid for corosync in cluster.conf
- Fixed bug which wouldn't allow a user to standby nodes
- Resolves: rhbz#1038479 rhbz#1038478 rhbz#1032161

* Fri Oct 11 2013 Chris Feist <cfeist@redhat.com> - 0.9.90-2
- Bump version for 6.4.z stream

* Fri Oct 04 2013 Chris Feist <cfeist@redhat.com> - 0.9.90-1
- Add ability to set node attributes
- Fix issue setting meta attributes on a master when creating a resource

* Mon Sep 30 2013 Chris Feist <cfeist@redhat.com> - 0.9.89-1
- Show location constraint role in pcs status/constraint
- Disable resource before removing
- Misc man/usage fixes

* Thu Sep 26 2013 Chris Feist <cfeist@redhat.com> - 0.9.88-1
- Don't allow order/colocation constraints created for master primitives
- Check in clones for stonith resources
- Clarify 'constraint rule add' in man page/usage
- Fixed minor usage issue with colocation sets

* Fri Sep 20 2013 Chris Feist <cfeist@redhat.com> - 0.9.87-1
- Allow two ordering constraints with same resources
- Improved error messages when trying to master/clone resources
- Updated error message when attempting to move a master/slave without
  --master

* Wed Sep 18 2013 Chris Feist <cfeist@redhat.com> - 0.9.86-1
- Show useful error when attempting to move/ban/clear a resource id when
  using --master

* Wed Sep 18 2013 Chris Feist <cfeist@redhat.com> - 0.9.85-1
- Allow deleting clones/masters from 'resource delete'

* Tue Sep 17 2013 Chris Feist <cfeist@redhat.com> - 0.9.84-1
- Disable groups before removing them

* Mon Sep 16 2013 Chris Feist <cfeist@redhat.com> - 0.9.83-1
- Fix --enable option when setting up a cluster

* Wed Sep 11 2013 Chris Feist <cfeist@redhat.com> - 0.9.82-1
- Show constraint id when printing out location rules
- Improve error messages when adding location rules with errors
- Add ability to remove constraint rules
- Allow move of master/slave resources if --master is present

* Tue Sep 10 2013 Chris Feist <cfeist@redhat.com> - 0.9.81-1
- Fix issues when updating resource with multiple operations with the same
  action
- Fixed constraint rules and improved usage documentation

* Mon Sep 09 2013 Chris Feist <cfeist@redhat.com> - 0.9.80-1
- More fixes for OCF_CHECK_LEVEL issues
- Fix traceback when adding a resourcew with a provider that doesn't exist
- Create proper two_node cluster when only two nodes are specified in cluster
  setup
- Give useful error when bad options are used with 'op'

* Thu Sep 05 2013 Chris Feist <cfeist@redhat.com> - 0.9.79-1
- Fixed OCF_CHECK_LEVEL operation setting in resource update
- Return proper error codes when stopping/starting/enable/disabling resources
- Return proper error code on auth

* Wed Sep 04 2013 Chris Feist <cfeist@redhat.com> - 0.9.78-1
- Fixed error codes and stdout/stderr output on errors from pcs resource
  enable/disable
- Automatically add interval to operations which don't specify an interval

* Tue Sep 03 2013 Chris Feist <cfeist@redhat.com> - 0.9.77-1
- Fixed managing/unmanaging groups/clones/masters of resources
- Fixed issue when using --group when creating a resource

* Thu Aug 29 2013 Chris Feist <cfeist@redhat.com> - 0.9.76-1
- Renamed resource group remove/delete to ungroup
- Fixed moving resource masters
- Allow cloing/mastering last resource in a group

* Tue Aug 27 2013 Chris Feist <cfeist@redhat.com> - 0.9.75-1
- Removing a resource that is part of a resource set is now allowed
- When you try to remove a group from a master that has more than one
  resource you now recieve a helpful error
- Unclone works on clones where constraints have been added
- Removing a group with constraints now works properly
- Master/Slave groups now have constraints properly removed before being
  deleted

* Mon Aug 26 2013 Chris Feist <cfeist@redhat.com> - 0.9.74-1
- pcs cluster edit should now work properly
- Allow removal of group and resources inside group with
  pcs resource delete <group name>

* Tue Aug 20 2013 Chris Feist <cfeist@redhat.com> - 0.9.73-1
- Cluster name is now viewable on RHEL 6
- Cluster.conf is now removed on destroy
- Misc man page & usage updates
- When removing the last resource from a group, remove any constraints still
  remaining on group

* Mon Aug 19 2013 Chris Feist <cfeist@redhat.com> - 0.9.72-1
- Allow ban and clear of masters

* Thu Aug 15 2013 Chris Feist <cfeist@redhat.com> - 0.9.71-1
- Don't print pcsd status for RHEL6

* Thu Aug 15 2013 Chris Feist <cfeist@redhat.com> - 0.9.70-1
- Pulled in old fixes for RHEL6 that missed upstream
- Require ccs during install

* Tue Aug 13 2013 Chris Feist <cfeist@redhat.com> - 0.9.68-1
- Fix fencing for RHEL6

* Tue Aug 13 2013 Chris Feist <cfeist@redhat.com> - 0.9.67-2
- Minor man page fixes

* Tue Aug 13 2013 Chris Feist <cfeist@redhat.com> - 0.9.66-1
- Resynched to upstream sources

* Tue Aug 13 2013 Chris Feist <cfeist@redhat.com> - 0.9.65-1
- Resynched to upstream sources

* Tue Aug 13 2013 Chris Feist <cfeist@redhat.com> - 0.9.64-1
- Resynched to upstream sources

* Wed Aug 07 2013 Chris Feist <cfeist@redhat.com> - 0.9.62-1
- Resynched to upstream sources

* Mon Jul 29 2013 Chris Feist <cfeist@redhat.com> - 0.9.60-1
- Resynched to upstream sources
- Added pcsd wizards

* Thu Jul 25 2013 Chris Feist <cfeist@redhat.com> - 0.9.59-1
- Resynched to upstream sources

* Tue Jan 29 2013 Chris Feist <cfeist@redhat.com> - 0.9.26-11
- Fixed missing master/slave resources in 'pcs config'
- Resolves: rhbz#bz903712

* Tue Jan 22 2013 Chris Feist <cfeist@redhat.com> - 0.9.26-10
- Removed one extra place where pcs incorrectly deleted resources from the lrm
- Resolves: rhbz#893221

* Tue Jan 15 2013 Chris Feist <cfeist@redhat.com> - 0.9.26-9
- pcs now allows assigning constraints to group/clone/multistate resources
- pcs no longer deletes resources from the lrm during resource removal
- Resolves: rhbz#894174 rhbz#893221

* Mon Dec 17 2012 Chris Feist <cfeist@redhat.com> - 0.9.26-8
- Fixed issue with error when listing resource providers and standards
- Resolves: rhbz#bz887870

* Tue Dec 04 2012 Chris Feist <cfeist@redhat.com> - 0.9.26-7
- Fixed minor issue with pcs resource move/unmove display
- Resolves: rhbz#878681

* Tue Dec 04 2012 Chris Feist <cfeist@redhat.com> - 0.9.26-6
- Added additional specific steps for configuring pcs on Red Hat Enterprise
  Linux 6
- Resolves: rhbz#878682 

* Wed Nov 14 2012 Chris Feist <cfeist@redhat.com> - 0.9.26-3
- Added in missing pcs resource move/unmove functionality
- Resolves: rhbz#878681

* Tue Sep 25 2012 Chris Feist <cfeist@redhat.com> - 0.9.26-2
- Updates to fix issues with RHEL6 and pcs/corosync/pacemaker

* Tue Sep 25 2012 Chris Feist <cfeist@redhat.com> - 0.9.26-1
- Resync to latest version of pcs

* Mon Sep 24 2012 Chris Feist <cfeist@redhat.com> - 0.9.25-1
- Resync to latest version of pcs

* Thu Sep 20 2012 Chris Feist <cfeist@redhat.com> - 0.9.24-1
- Resync to latest version of pcs

* Thu Sep 20 2012 Chris Feist <cfeist@redhat.com> - 0.9.23-1
- Resync to latest version of pcs

* Wed Sep 12 2012 Chris Feist <cfeist@redhat.com> - 0.9.22-1
- Resync to latest version of pcs

* Thu Sep 06 2012 Chris Feist <cfeist@redhat.com> - 0.9.19-1
- Resync to latest version of pcs

* Tue Aug 07 2012 Chris Feist <cfeist@redhat.com> - 0.9.12-1
- Resync to latest version of pcs

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu May 24 2012 Chris Feist <cfeist@redhat.com> - 0.9.4-1
- Resync to latest version of pcs
- Move cluster creation options to cluster sub command.

* Mon May 07 2012 Chris Feist <cfeist@redhat.com> - 0.9.3.1-1
- Resync to latest version of pcs which includes fixes to work with F17.

* Mon Mar 19 2012 Chris Feist <cfeist@redhat.com> - 0.9.2.4-1
- Resynced to latest version of pcs

* Mon Jan 23 2012 Chris Feist <cfeist@redhat.com> - 0.9.1-1
- Updated BuildRequires and %doc section for fedora

* Fri Jan 20 2012 Chris Feist <cfeist@redhat.com> - 0.9.0-2
- Updated spec file for fedora specific changes

* Mon Jan 16 2012 Chris Feist <cfeist@redhat.com> - 0.9.0-1
- Initial Build
