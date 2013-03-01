%global debug_package %{nil}

Name:           vsdl
Version:        1.0
Release:        1%{?dist}
Summary:        Vitual SQL Data Layer

Group:		System Environment/Daemons

License:        BSD
URL:            http://vsdl.org/
Source0:        vitess.tar.bz2
Source1:        zookeeper.tar.bz2

Source2:        vtocc.conf
Source3:        my.cnf

Patch0001:	0001-vtocc-config.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	go
BuildRequires:	mysql-libs
BuildRequires:	mysql-devel

Requires:       mysql-server
Requires:       mysql-libs

%description
Virtual SQL Data Layer



%prep
#%setup -q
# Create Directory (and change to it) Before Unpacking
#%setup -c
# Not Delete Directory Before Unpacking Sources
#%setup -D -a 1
# -T - Do Not Perform Default Archive Unpacking

# unpack source1 with default archive and create the top level dir
%setup -a 1 -c
%patch0001 -p1

mkdir -p src/launchpad.net/gozk
mkdir -p src/code.google.com/p
mv zookeeper src/launchpad.net/gozk/
mv vitess src/code.google.com/p


%build
export GOPATH=`pwd`

cd src/code.google.com/p/vitess
./bootstrap.sh
. ./dev.env
cd go
make


%install
rm -rf $RPM_BUILD_ROOT

sed -i 's/go build/go install/' src/code.google.com/p/vitess/go/Makefile

export GOBIN=%{buildroot}/usr/bin

cd src/code.google.com/p/vitess

# install configs
install -d -m 755 %{buildroot}%{_datarootdir}/%{name}
cp -a config %{buildroot}%{_datarootdir}/%{name}
cp -a data %{buildroot}%{_datarootdir}/%{name}

install -p -D -m 640 %{SOURCE2} %{buildroot}%{_sysconfdir}/%{name}/vtocc.conf
install -p -D -m 640 %{SOURCE3} %{buildroot}%{_datarootdir}/%{name}/examples/my.cnf


install -d -m 755 %{buildroot}%{_sysconfdir}/%{name}
#cp py/vttest/dbtest.json %{buildroot}%{_sysconfdir}/%{name}/vsdl.conf
. ./dev.env

cd go
make

# install python client

# install bson
cd $VTTOP/third_party/py/bson-0.3.2 && \
	python ./setup.py install --root=%{buildroot}

#install vtdb
cd $VTTOP/py && \
	python ./setup.py install --root=%{buildroot}

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
/usr/bin/*
/usr/lib/*
%doc %{_datarootdir}/%{name}

%dir %{_sysconfdir}/%{name}
%config %{_sysconfdir}/%{name}/vtocc.conf



%changelog
* Wed Feb 27 2013 Wenming Zhang <zhgwenming@gmail.com>
- Initial rpm build
