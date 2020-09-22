# TODO:
# - configure: Using jni: no (JNI requires --enable-module-ecdh, which is experimental)

# Conditional build:
%bcond_without	static_libs	# static library
%bcond_without	tests		# unit tests
#
Summary:	Optimized C library for EC operations on curve secp256k1
Summary(pl.UTF-8):	Zoptymalizowana biblioteka C do operacji EC na krzywej secp256k1
Name:		libsecp256k1
Version:	0.1.0.16
%define	gitref	5a373e416025ae6465b00aea18dd6d69111e54ca
%define	snap	20191026
%define	rel	1
Release:	0.%{snap}.%{rel}
License:	MIT
Group:		Libraries
#Source0Download: https://github.com/libbitcoin/secp256k1/releases
# releases
#Source0:	https://github.com/libbitcoin/secp256k1/archive/v%{version}/secp256k1-%{version}.tar.gz
# no tag for 0.1.0.16, use snapshot
Source0:	https://github.com/libbitcoin/secp256k1/archive/%{gitref}/secp256k1-%{snap}.tar.gz
# Source0-md5:	692fb5624b5c49bd1648d9cc04d798b9
URL:		https://libbitcoin.org/
BuildRequires:	autoconf >= 2.60
BuildRequires:	automake
BuildRequires:	gmp-devel
BuildRequires:	libtool >= 2:2
BuildRequires:	pkgconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Optimized C library for EC operations on curve secp256k1.

%description -l pl.UTF-8
Zoptymalizowana biblioteka C do operacji EC na krzywej secp256k1.

%package devel
Summary:	Header files for secp256k1 library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki secp256k1
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	gmp-devel

%description devel
Header files for secp256k1 library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki secp256k1.

%package static
Summary:	Static secp256k1 library
Summary(pl.UTF-8):	Statyczna biblioteka secp256k1
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static secp256k1 library.

%description static -l pl.UTF-8
Statyczna biblioteka secp256k1.

%prep
%setup -q -n secp256k1-%{gitref}

%build
%{__libtoolize}
%{__aclocal} -I build-aux/m4
%{__autoconf}
%{__autoheader}
%{__automake}
# NOTE: --enable-module-recovery to avoid: https://github.com/libbitcoin/libbitcoin/issues/397
%configure \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static} \
	--enable-module-recovery
%{__make}

%if %{with tests}
./tests
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libsecp256k1.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING README.md TODO
%attr(755,root,root) %{_libdir}/libsecp256k1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsecp256k1.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsecp256k1.so
%{_includedir}/secp256k1.h
%{_includedir}/secp256k1_preallocated.h
%{_includedir}/secp256k1_recovery.h
%{_pkgconfigdir}/libsecp256k1.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libsecp256k1.a
%endif
