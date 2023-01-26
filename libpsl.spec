#
# Conditional build:
%bcond_without	apidocs		# don't build api docs
%bcond_without	static_libs	# static library
%bcond_with	icu		# use ICU instead of libidn2+libunistring for IDNA2008

Summary:	C library for the Publix Suffix List
Summary(pl.UTF-8):	Biblioteka C do obsługi listy przyrostków publicznych (Public Suffix List)
Name:		libpsl
Version:	0.21.2
Release:	1
License:	MIT
Group:		Networking
#Source0Download: https://github.com/rockdaboot/libpsl/releases
Source0:	https://github.com/rockdaboot/libpsl/releases/download/%{version}/%{name}-%{version}.tar.lz
# Source0-md5:	074379959be1bfe5355db6c331f10829
%if 0
# not required if packaged with libpsl release
%define	psl_ref	1fc1ed365818a6a77d6f31d425ff03ca54cdc7f3
%define	psldate	20150827
Source1:	https://github.com/publicsuffix/list/archive/%{psl_ref}/publicsuffix_list-%{psldate}.tar.gz
# Source1-md5:	ee9a591d4545d9f6ca350bd9df2c2e51
%endif
URL:		https://rockdaboot.github.io/libpsl
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.10
BuildRequires:	gettext-tools >= 0.19.3
BuildRequires:	glib2-devel
%{?with_apidocs:BuildRequires:	gtk-doc >= 1.15}
%{?with_icu:BuildRequires:	libicu-devel}
%{!?with_icu:BuildRequires:	libidn2-devel}
BuildRequires:	libtool >= 2:2
BuildRequires:	libxslt-progs
BuildRequires:	pkgconfig
BuildRequires:	python >= 1:2.7
BuildRequires:	sed >= 4.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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

%description -l pl.UTF-8
libpsl to biblioteka C do obsługi listy przyrostków publicznych
(Public Suffix List). "Przyrostek publiczny" to nazwa domeny, poniżej
której bezpośrednio użytkownicy Internetu mogą rejestrować własne
nazwy.

Przeglądarki i inni klienci WWW mogą jej używać w celu:
- zapobieganiu "superciasteczek" naruszającym prywatność
- zapobieganiu certyfikatom "superdomenowym" naruszającym prywatność
- podświetlania części domen w interfejsie użytkownika
- sortowania listy domen według serwisu.

Libpsl:
- ma wbudowane dane PSL dla szybkiego dostępu
- pozwala na wczytywanie danych PSL z plików
- sprawdza, czy dana domena jest "przyrostkiem publicznym"
- zapewnia natychmiastową weryfikację domeny ciasteczka
- znajduje najdłuższą publiczną część podanej domeny
- znajduje najkrótszą prywatną część podanej domeny
- działa z domenami międzynarodowymi (UTF-8 i IDNA2008 Punycode)
- jest bezpieczna względem wątków
- obsługuje IDNA2008 UTS#46.

%package devel
Summary:	Development files for libpsl
Summary(pl.UTF-8):	Pliki programistyczne biblioteki libpsl
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the header file for developing applications that
use libpsl.

%description devel -l pl.UTF-8
Ten pakiet zawiera plik nagłówkowy do tworzenia aplikacji
wykorzystujących bibliotekę libpsl.

%package static
Summary:	Static libpsl library
Summary(pl.UTF-8):	Statyczna biblioteka libpsl
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libpsl library.

%description static -l pl.UTF-8
Statyczna biblioteka libpsl.

%package apidocs
Summary:	API documentation for libpsl library
Summary(pl.UTF-8):	Dokumentacja API biblioteki libpsl
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for libpsl library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libpsl.

%package utils
Summary:	Commandline utility to explore the Public Suffix List
Summary(pl.UTF-8):	Narzędzie linii poleceń do eksplorowania listy przyrostków publicznych
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}

%description utils
This package contains a commandline utility to explore the Public
Suffix List, for example it checks if domains are public suffixes,
checks if cookie-domain is acceptable for domains and so on.

%description utils -l pl.UTF-8
Ten pakiet zawiera narzędzie linii poleceń do eksplorowania listy
przyrostków publicznych (Public Suffix List); sprawdza ono na
przykład, czy domeny są przyrostkami publicznymi, czy domena
ciasteczka jest akceptowalna dla domen itp.

%prep
%setup -q

%if 0
rmdir list
%{__tar} xf %{SOURCE1}
%{__mv} list-%{psl_ref} list
%endif

%build
%{__gettextize}
%{?with_apidocs:%{__gtkdocize}}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static} \
	%{?with_apidocs:--enable-gtk-doc} \
	--enable-man \
	--enable-builtin=%{?with_icu:libicu}%{!?with_icu:libidn2} \
	--enable-runtime=%{?with_icu:libicu}%{!?with_icu:libidn2} \
	--with-html-dir=%{_gtkdocdir}

%{__make}

%{?with_tests:%{__make} check}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%if !%{with apidocs}
install -d $RPM_BUILD_ROOT%{_mandir}/man3
install -c -m 644 docs/libpsl/libpsl.3 $RPM_BUILD_ROOT%{_mandir}/man3
%endif

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libpsl.la
# tool not installed
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/psl-make-dafsa.1

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING NEWS
%attr(755,root,root) %{_libdir}/libpsl.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpsl.so.5

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpsl.so
%{_includedir}/libpsl.h
%{_pkgconfigdir}/libpsl.pc
%{_mandir}/man3/libpsl.3*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libpsl.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/libpsl
%endif

%files utils
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/psl
%{_mandir}/man1/psl.1*
