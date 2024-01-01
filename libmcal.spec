%define	drvver	0.9
Summary:	Modular Calendar Access Library
Summary(pl.UTF-8):	Modularna biblioteka dostępu do kalendarzy
Name:		libmcal
Version:	0.7
Release:	7
License:	LGPL v2+
Group:		Libraries
Source0:	http://downloads.sourceforge.net/libmcal/%{name}-%{version}.tar.gz
# Source0-md5:	8d8f16e59a7e859c1407df3d72052825
Source1:	http://downloads.sourceforge.net/libmcal/mcaldrivers-%{drvver}.tar.gz
# Source1-md5:	c8c96f6cd574139b88a13f6084164cfa
Patch0:		%{name}-make.patch
Patch1:		%{name}-define.patch
Patch2:		%{name}-dirs.patch
Patch3:		%{name}-gcc4.patch
Patch4:		%{name}-types.patch
URL:		http://libmcal.sourceforge.net/
BuildRequires:	flex
BuildRequires:	libtool
BuildRequires:	pam-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# cc_vdlog(), cc_vlog(), cc_searched(), cc_login() callbacks to be defined by user
%define		skip_post_check_so	libmcal.so.0.0.0

%description
libmcal is a C library for accessing calendars. It's written to be
very modular, with plugable drivers.

%description -l pl.UTF-8
libmcal to biblioteka w C służąca do dostępu do kalendarzy. Jest tak
napisana, by być modularna, z możliwością dołączania sterowników.

%package devel
Summary:	MCAL header files
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki MCAL
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for MCAL-based programs development.

%description devel -l pl.UTF-8
Pliki nagłówkowe do tworzenia programów korzystających z MCAL.

%package static
Summary:	MCAL static library
Summary(pl.UTF-8):	Statyczna biblioteka MCAL
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static version of MCAL.

%description static -l pl.UTF-8
Statyczna wersja biblioteki MCAL.

%prep
%setup -q -n %{name} -a1
%{__mv} mcal-drivers/* .
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
chmod +x configure

%{__make} -C icap \
	CC="%{__cc}" \
	OPTFLAGS="%{rpmcflags}"

%{__make} -C mstore \
	CC="%{__cc}" \
	OPTFLAGS="%{rpmcflags}"

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

%{__mv} mstore/Changelog Changelog.mstore
%{__mv} mstore/README README.mstore

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGELOG FAQ-MCAL FEATURE-IMPLEMENTATION HOW-TO-MCAL *.mstore
%attr(755,root,root) %{_libdir}/libmcal.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmcal.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmcal.so
%{_libdir}/libmcal.la
%{_includedir}/mcal

%files static
%defattr(644,root,root,755)
%{_libdir}/libmcal.a
