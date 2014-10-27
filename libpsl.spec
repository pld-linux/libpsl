Summary:	C library for the Publix Suffix List
Name:		libpsl
Version:	0.5.1
Release:	1
License:	MIT
Group:		Networking
URL:		https://rockdaboot.github.io/libpsl
Source0:	https://github.com/rockdaboot/libpsl/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
# Source0-md5:	3ef1aba32c2422b3527d86d3fb47c18e
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel
BuildRequires:	gtk-doc
BuildRequires:	libicu-devel
BuildRequires:	libxslt

%description
libpsl is a C library to handle the Public Suffix List. A "public
suffix" is a domain name under which Internet users can directly
register own names.

Browsers and other web clients can use it to

- Avoid privacy-leaking "supercookies";
- Avoid privacy-leaking "super domain" certificates;
- Domain highlighting parts of the domain in a user interface;
- Sorting domain lists by site;

Libpsl...

- has built-in PSL data for fast access;
- allows to load PSL data from files;
- checks if a given domain is a "public suffix";
- provides immediate cookie domain verification;
- finds the longest public part of a given domain;
- finds the shortest private part of a given domain;
- works with international domains (UTF-8 and IDNA2008 Punycode);
- is thread-safe;
- handles IDNA2008 UTS#46;

%package        devel
Summary:	Development files for %{name}
Requires:	%{name} = %{version}-%{release}

%description    devel
This package contains libraries and header files for developing
applications that use %{name}.

%package utils
Summary:	Commandline utility to explore the Public Suffix List
Requires:	%{name} = %{version}-%{release}

%description utils
This package contains a commandline utility to explore the Public
Suffix List, for example it checks if domains are public suffixes,
checks if cookie-domain is acceptable for domains and so on.

%prep
%setup -q

%build
./autogen.sh

%configure \
	--disable-silent-rules \
	--disable-static	   \
	--enable-man		   \
	--enable-gtk-doc

%{__make}

%{?with_tests:%{__make} check}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README.md
%attr(755,root,root) %ghost %{_libdir}/libpsl.so.0
%attr(755,root,root) %{_libdir}/libpsl.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpsl.so
%{_includedir}/libpsl.h
%{_pkgconfigdir}/libpsl.pc
%{_mandir}/man3/libpsl.3*
#%{_datadir}/gtk-doc/html/libpsl/
%{_datadir}/%{name}

%exclude %{_datadir}/libpsl/test_psl.txt

%files utils
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/psl
