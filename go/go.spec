# The libraries and binaries produced by this compiler are not compatible
# with coreutils strip (yet).
%global _enable_debug_package 0
%global debug_package %{nil}
%global __os_install_post /usr/lib/rpm/brp-compress %{nil}

Name:           go
Version:        1.0.3
Release:        4%{?dist}
Summary:        The Go programming language
Group:          Development/Languages
License:        BSD
URL:            http://golang.org/

# Currently available using 
# hg clone -r release.r59 https://go.googlecode.com/hg go
# cd go
# hg archive ../go-1.0.3.tar.bz2
# https://go.googlecode.com/files/go1.0.3.src.tar.gz
#Source0:        %{name}-%{version}.tar.bz2
Source0:        https://go.googlecode.com/files/%{name}%{version}.src.tar.gz

BuildRequires:  ed%{?_isa}
BuildRequires:  bison%{?_isa}
BuildRequires:  mercurial
%ifarch x86_64
BuildRequires:  glibc-devel
BuildRequires:  libgcc
%endif

Requires:       %{name}-src = %{version}-%{release}

ExclusiveArch: %ix86 x86_64

%description
The Go programming language is an open source project to make programmers
more productive. Go is expressive, concise, clean, and efficient. Its
concurrency mechanisms make it easy to write programs that get the most
out of multi-core and networked machines, while its novel type system
enables flexible and modular program construction. Go compiles quickly
to machine code yet has the convenience of garbage collection and the
power of run-time reflection. It's a fast, statically typed, compiled
language that feels like a dynamically typed, interpreted language.


%package src
Summary:        Go documentation
Group:          Development/Languages

%description src
Go source code

%package doc
Summary:        Go documentation
Group:          Documentation
Requires:       %{name} = %{version}-%{release}

%description doc
Go examples and documentation.


%package	vim
Summary:        Go syntax files for vim
Group:          Applications/Editors
Requires:       vim-common%{?_isa}
Requires:       %{name} = %{version}-%{release}

%description	vim
Go syntax for vim.


%package	emacs
Summary:        Go syntax files for emacs
Group:          Applications/Editors
Requires:       emacs-common%{?_isa}
Requires:       %{name} = %{version}-%{release}

%description	emacs
Go syntax for emacs.


%prep
%setup -q -n go
# todo patch based on OpenSuse's  build is needed for godoc to work

# Create a README.Fedora
cat << EOF > README.Fedora
# Instructions
Please, visit http://golang.org/ in order to 
learn more about this language.

# Documentation
In order to access documentation about the libraries, please, use the 'godoc'
command. More documentation about it here: http://golang.org/cmd/godoc/
EOF

# Create a go.sh for /etc/profile.d
%ifarch x86_64
    %global goarch amd64
    
    echo '# Go environment vars
export GOROOT=%{_libdir}/go
export GOBIN=%{_bindir}
export GOOS=linux
export GOARCH=%{goarch}' > go.sh
%else
    %global goarch 386

    echo '# Go environment vars
export GOROOT=%{_libdir}/go
export GOBIN=%{_bindir}
export GOOS=linux
export GOARCH=%{goarch}' > go.sh
%endif

%build
# clean env
unset GOROOT GOBIN

# set env (not entirely necessary)
export GOOS=linux

# go's final expected path
export GOROOT_FINAL=%{_libdir}/go

# give CFLAGS in their required way and ommit ggdb
export HOST_EXTRA_CFLAGS="-ggdb"

# noexecstack so SELinux doesn't complain
export HOST_EXTRA_LDFLAGS="-Wl -z noexecstack"

# issue #1464
ulimit -v unlimited

# build
#%ifarch x86_64
#    # amd64 primary in this case, so build it second (i.e., get 64-bit cgo)
#    cd src && GOARCH=386 ./make.bash
#              GOARCH=%{goarch} ./make.bash
#%else
#    cd src && GOARCH=%{goarch} ./make.bash
#%endif

cd src && GOARCH=%{goarch} ./make.bash

%install
# create dirs
install -d -p -m 755 %{buildroot}%{_bindir}
install -d -p -m 755 %{buildroot}%{_datadir}/go
install -d -p -m 755 %{buildroot}%{_libdir}/go
install -d -p -m 755 %{buildroot}%{_libdir}/go/pkg
ln -s ../../share/go/src %{buildroot}%{_libdir}/go/src
ln -s ../../share/go/include %{buildroot}%{_libdir}/go/include
#install -d -p -m 755 %{buildroot}%{_libdir}/go/src

# install essential
install -D -p -m 755   bin/*                               %{buildroot}%{_bindir}
cp -pR                 pkg                                 %{buildroot}%{_libdir}/go
#install -D -p -m 664   src/Make.*                          %{buildroot}%{_libdir}/go/src
install -D -p -m 664   go.sh                               %{buildroot}%{_sysconfdir}/profile.d/go.sh

# install extras
install -D -p -m 644   misc/bash/go                        %{buildroot}/%{_sysconfdir}/bash_completion.d/go.bash
install -D -p -m 644   misc/emacs/go-mode.el               %{buildroot}/%{_datadir}/emacs/site-lisp/go-mode.el
install -D -p -m 644   misc/emacs/go-mode-load.el          %{buildroot}/%{_datadir}/emacs/site-lisp/go-mode-load.el
install -D -p -m 644   misc/vim/ftdetect/gofiletype.vim    %{buildroot}/%{_datadir}/vim/vimfiles/ftdetect/gofiletype.vim
install -D -p -m 644   misc/vim/syntax/go.vim              %{buildroot}/%{_datadir}/vim/vimfiles/syntax/go.vim

# documentation
install -d -p -m 755   doc/examples
mv                     misc/cgo                            doc/examples
#chmod 644              doc/codelab/wiki/test.sh
#find src -name *.go -exec cp -p --parents {}  %{buildroot}%{_datadir}/go/src \;
cp -a src  %{buildroot}%{_datadir}/go/
cp -a include  %{buildroot}%{_datadir}/go/

%files
%defattr(-,root,root,-)
%{_bindir}/
%{_libdir}/go
%{_sysconfdir}/bash_completion.d/go.bash
%{_sysconfdir}/profile.d/go.sh
%doc AUTHORS CONTRIBUTORS LICENSE README README.Fedora

%files doc
%defattr(-,root,root,-)
%doc doc/*

%files src
%defattr(-,root,root,-)
%{_datadir}/go/*

%files vim
%defattr(-,root,root,-)
%doc LICENSE
%{_datadir}/vim/vimfiles/syntax/go.vim
%{_datadir}/vim/vimfiles/ftdetect/gofiletype.vim

%files emacs
%defattr(-,root,root,-)
%doc LICENSE
%{_datadir}/emacs/site-lisp/go-mode-load.el
%{_datadir}/emacs/site-lisp/go-mode.el


%changelog
* Wed Jan 21 2013 Albert Zhang <zhgwenming@gmail.com> - 1.0.3-4
- Build for x86_64
- upgrade to upstream version 1.0.3

* Wed Aug 31 2011 W. Michael Petullo <mike@flyn.org> - release.r59-3
- Require glibc-devel.i686 on x86_64
- Do not try to build 64-bit on i686

* Wed Aug 31 2011 W. Michael Petullo <mike@flyn.org> - release.r59-2
- Require mercurial to build

* Tue Aug 30 2011 W. Michael Petullo <mike@flyn.org> - release.r59-1
- Updated to release.r59
- Use make.bash, not all.bash, to speed up build
- Build both 32- and 64-bit compilers
- Remove _smp_mflags and --build-id; broke build on F15
- Small formatting fixes

* Sun Apr 03 2011 Renich Bon Ciric <renich@woralelandia.com> - release.r56-1
- Updated to release.r56
- Added -p to install statements
- Removed old stuff (BuildRoot)
- Added the specific arch macro on BuildRequires

* Fri Feb 04 2011 Renich Bon Ciric <renich@woralelandia.com> - 20110201.1-1
- source upgrade to release 2011-02-01.1

* Fri Feb 04 2011 Renich Bon Ciric <renich@woralelandia.com> - 20110120-9
- documentation package first build

* Fri Feb 04 2011 Renich Bon Ciric <renich@woralelandia.com> - 20110120-8
- added lib/godoc

* Fri Feb 04 2011 Renich Bon Ciric <renich@woralelandia.com> - 20110120-7
- Added go.sh to /etc/profile.d again (for environment)
- Removed email from README.Fedora
- Reorganized spec file a bit

* Mon Jan 31 2011 Renich Bon Ciric <renich@woralelandia.com> - 20110120-6
- Changed names from go-emacs and vim-emacs to emacs-go and vim-go
- Added info about godoc to README.Fedora

* Fri Jan 28 2011 Renich Bon Ciric <renich@woralelandia.com> - 20110120-5
- Added src/Make.* to the mix; it seems some apps need them

* Thu Jan 27 2011 Renich Bon Ciric <renich@woralelandia.com> - 20110120-4
- Removed comments (and it's macros)
- Added the Make.inc and Make.pkg files to the src dir; under libraries
- Changed bash_completion.d/go to bash_completion.d/go.bash
- Eliminated exec files in doc

* Thu Jan 27 2011 Renich Bon Ciric <renich@woralelandia.com> - 20110120-3
- Removed GOROOT, GOARCH and GOBIN vars and left GOROOT_FINAL only
- Removed /etc/profile.d/go.sh

* Tue Jan 25 2011 Renich Bon Ciric <renich@woralelandia.com> - 20110120-2
- Added etc/profile.d/go.sh
- Implemented ifarch for go.sh generation and GOROOT and GOARCH vars

* Tue Jan 25 2011 Renich Bon Ciric <renich@woralelandia.com> - 20110120-1
- Initial build
- Took stuff from petullo and meyer spec files
