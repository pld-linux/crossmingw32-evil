Summary:	Evil - EFL Windows compatibility layer
Summary(pl.UTF-8):	Evil - Warstwa kompatybilności EFL z Windows
Name:		crossmingw32-evil
Version:	1.0.0
Release:	1
License:	Free (see COPYING)
Group:		Development/Libraries
Source0:	http://download.enlightenment.org/releases/evil-%{version}.tar.bz2
# Source0-md5:	4772bb5ee4f9d1287a31a4e922cc7b3f
URL:		http://trac.enlightenment.org/e/wiki/EFL
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake >= 1.6
BuildRequires:	crossmingw32-gcc
BuildRequires:	libtool >= 2:2.4
BuildRequires:	rpmbuild(macros) >= 1.197
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1

%define		target			i386-mingw32
%define		target_platform 	i386-pc-mingw32

%define		_sysprefix		/usr
%define		_prefix			%{_sysprefix}/%{target}
%define		_libdir			%{_prefix}/lib
%define		_pkgconfigdir		%{_prefix}/lib/pkgconfig
%define		_dlldir			/usr/share/wine/windows/system
%define		__cc			%{target}-gcc
%define		__cxx			%{target}-g++

%ifnarch %{ix86}
# arch-specific flags (like alpha's -mieee) are not valid for i386 gcc
%define		optflags	-O2
%endif
# -z options are invalid for mingw linker
%define		filterout_ld	-Wl,-z,.*

%description
The Evil library tried to port some convenient Unix functions to the
Windows (XP or CE) platform. They are used in the Enlightenment
Foundation Libraries (EFL).

This package contains the cross version for Win32.

%description -l pl.UTF-8
Biblioteka Evil jest próbą przeniesienia niektórych wygodnych funkcji
uniksowych na platformę Windows (XP lub CE). Jest wykorzystywana w
bibliotekach EFL (Enlightenment Foundation Libraries).

Ten pakiet zawiera wersję skrośną dla Win32.

%package static
Summary:	Static Evil libraries (cross MinGW32 version)
Summary(pl.UTF-8):	Statyczne biblioteki Evil (wersja skrośna MinGW32)
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description static
Static Evil libraries (cross MinGW32 version).

%description static -l pl.UTF-8
Statyczne biblioteki Evil (wersja skrośna MinGW32).

%package dll
Summary:	DLL Evil libraries for Windows
Summary(pl.UTF-8):	Biblioteki DLL Evil dla Windows
Group:		Applications/Emulators
Requires:	wine

%description dll
DLL Evil libraries for Windows.

%description dll -l pl.UTF-8
Biblioteki DLL Evil dla Windows.

%prep
%setup -q -n evil-%{version}

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--target=%{target} \
	--host=%{target} \
	--disable-silent-rules

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_dlldir}
mv -f $RPM_BUILD_ROOT%{_prefix}/bin/*.dll $RPM_BUILD_ROOT%{_dlldir}

%if 0%{!?debug:1}
%{target}-strip --strip-unneeded -R.comment -R.note $RPM_BUILD_ROOT%{_dlldir}/*.dll
%{target}-strip -g -R.comment -R.note $RPM_BUILD_ROOT%{_libdir}/*.a
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING COPYING-PLAIN ChangeLog NEWS README
%{_libdir}/libdl.dll.a
%{_libdir}/libdl.la
%{_libdir}/libevil.dll.a
%{_libdir}/libevil.la
%{_includedir}/evil-1
%{_pkgconfigdir}/evil.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libdl.a
%{_libdir}/libevil.a

%files dll
%defattr(644,root,root,755)
%{_dlldir}/libdl-1.dll
%{_dlldir}/libevil-1.dll