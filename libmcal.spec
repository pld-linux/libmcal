Summary:	Modular Calendar Access Library
Summary(pl):	Modularna biblioteka dostêpu do kalendarzy
Name:		libmcal
Version:	0.6
Release:	1
License:	GPL
Group:		Libraries
Source0:	ftp://ftp.sourceforge.net/pub/sourceforge/libmcal/%{name}-%{version}.tar.gz
Source1:	ftp://ftp.sourceforge.net/pub/sourceforge/libmcal/mcaldrivers-0.8.tar.gz
Patch0:		%{name}-echo.patch
Patch1:		%{name}-make.patch
URL:		http://mcal.chek.com/
BuildRequires:	flex
BuildRequires:	libtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_includedir	%{_prefix}/include/mcal

%description
libmcal is a C library for accessing calendars. It's written to be
very modular, with plugable drivers.

%description -l pl
libmcal to biblioteka w C s³u¿±ca do dostêpu do kalendarzy. Jest tak
napisana, by byæ modularna, z mo¿liwo¶ci± do³±czania sterowników.

%package devel
Summary:	MCAL header files
Summary(pl):	Pliki nag³ówkowe biblioteki MCAL
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
Header files for MCAL-based programs development.

%description devel -l pl
Pliki nag³ówkowe do tworzenia programów korzystaj±cych z MCAL.

%package static
Summary:	MCAL static library
Summary(pl):	Statyczna biblioteka MCAL
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
Static version of MCAL.

%description static -l pl
Statyczna wersja biblioteki MCAL.

%prep
%setup -q -n %{name} -a1
mv -f mcal-drivers/* .
%patch0 -p1
%patch1 -p1

%build
chmod +x configure
%{__make} -C icap \
	CC="%{__cc}" OPTFLAGS="%{rpmcflags}"
%{__make} -C mstore \
	CC="%{__cc}" OPTFLAGS="%{rpmcflags}"

%configure2_13 \
	--with-icap \
	--with-mstore

%{__make} \
	CC="%{__cc}" \
	OPTFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

mv -f mstore/Changelog Changelog.mstore
mv -f mstore/README README.mstore

gzip -9nf CHANGELOG FAQ-MCAL FEATURE-IMPLEMENTATION HOW-TO-MCAL *.mstore

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc *.gz
%attr(755,root,root) %{_libdir}/lib*.so.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%attr(755,root,root) %{_libdir}/lib*.la
%{_includedir}

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
