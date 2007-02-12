%define	drvver	0.9
Summary:	Modular Calendar Access Library
Summary(pl.UTF-8):   Modularna biblioteka dostępu do kalendarzy
Name:		libmcal
Version:	0.7
Release:	3
License:	GPL
Group:		Libraries
Source0:	http://dl.sourceforge.net/libmcal/%{name}-%{version}.tar.gz
# Source0-md5:	8d8f16e59a7e859c1407df3d72052825
Source1:	http://dl.sourceforge.net/libmcal/mcaldrivers-%{drvver}.tar.gz
# Source1-md5:	c8c96f6cd574139b88a13f6084164cfa
Patch0:		%{name}-make.patch
Patch1:		%{name}-define.patch
Patch2:		%{name}-dirs.patch
Patch3:		%{name}-gcc4.patch
URL:		http://mcal.chek.com/
BuildRequires:	flex
BuildRequires:	libtool
BuildRequires:	pam-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libmcal is a C library for accessing calendars. It's written to be
very modular, with plugable drivers.

%description -l pl.UTF-8
libmcal to biblioteka w C służąca do dostępu do kalendarzy. Jest tak
napisana, by być modularna, z możliwością dołączania sterowników.

%package devel
Summary:	MCAL header files
Summary(pl.UTF-8):   Pliki nagłówkowe biblioteki MCAL
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for MCAL-based programs development.

%description devel -l pl.UTF-8
Pliki nagłówkowe do tworzenia programów korzystających z MCAL.

%package static
Summary:	MCAL static library
Summary(pl.UTF-8):   Statyczna biblioteka MCAL
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static version of MCAL.

%description static -l pl.UTF-8
Statyczna wersja biblioteki MCAL.

%prep
%setup -q -n %{name} -a1
mv -f mcal-drivers/* .
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

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
install -d $RPM_BUILD_ROOT%{_libdir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

mv -f mstore/Changelog Changelog.mstore
mv -f mstore/README README.mstore

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGELOG FAQ-MCAL FEATURE-IMPLEMENTATION HOW-TO-MCAL *.mstore
%attr(755,root,root) %{_libdir}/lib*.so.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/mcal

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
