#
# Conditional build:
%bcond_without	static_libs	# static library

%define	api_version	1.4.363.0
%define	gitref		vulkan-sdk-%{api_version}

Summary:	Tools for parsing and converting SPIR-V to other shader languages
Summary(pl.UTF-8):	Narzędzia do analizy i konwersji SPIR-V do innych języków shaderów
Name:		spirv-cross
# CMakeLists.txt /SPIRV_CROSS_VERSION
Version:	0.68.0
Release:	1
License:	Apache v2.0
Group:		Development/Tools
#Source0Download: https://github.com/KhronosGroup/SPIRV-Cross/tags
Source0:	https://github.com/KhronosGroup/SPIRV-Cross/archive/%{gitref}/SPIRV-Cross-%{gitref}.tar.gz
# Source0-md5:	4049053c7b27ec33aee89aec7ebcf7b1
URL:		https://github.com/KhronosGroup/SPIRV-Cross
BuildRequires:	cmake >= 3.10
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	python3 >= 1:3
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	sed >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SPIRV-Cross is a tool designed for parsing and converting SPIR-V to
other shader languages. Features:
- Convert SPIR-V to readable, usable and efficient GLSL
- Convert SPIR-V to readable, usable and efficient Metal Shading
  Language (MSL)
- Convert SPIR-V to readable, usable and efficient HLSL
- Convert SPIR-V to a JSON reflection format
- Convert SPIR-V to debuggable C++ (DEPRECATED)
- Reflection API to simplify the creation of Vulkan pipeline layouts
- Reflection API to modify and tweak OpDecorations
- Supports "all" of vertex, fragment, tessellation, geometry and
  compute shaders.

%description -l pl.UTF-8
SPIR-V Tools to projekt udostępniający API i polecenia do
przetwarzania modułów SPIR-V. Możliwości:
- konwersja SPIR-V do czytelnego, używalnego i wydajnego GLSL
- konwersja SPIR-V do czytelnego, używalnego i wydajnego MSL (Metal
  Shading Language)
- konwersja SPIR-V do czytelnego, używalnego i wydajnego HLSL
- konwersja SPIR-V do formatu refleksji JSON
- konwersja SPIR-V do nadającego się do śledzenia C++ (PRZESTARZAŁE)
- API refleksji upraszczające tworzenie układów potoków Vulkan
- API refleksji do modyfikowania i dostosowywania OpDecorations
- obsługa "wszystkiego" spośród shaderów: wierzchołków, fragmentów,
  teselacji, geometrii oraz obliczeń

%package devel
Summary:	Header files for SPIR-V Cross library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki SPIR-V Cross
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
Header files for SPIR-V Cross library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki SPIR-V Cross.

%package static
Summary:	Static SPIR-V Cross libraries
Summary(pl.UTF-8):	Statyczne biblioteki SPIR-V Cross
Group:		Development/Libraries
Requires:	%{name}devel%{?_isa} = %{version}-%{release}

%description static
Static SPIR-V Cross libraries.

%description static -l pl.UTF-8
Statyczne biblioteki SPIR-V Cross.

%prep
%setup -q -n SPIRV-Cross-%{gitref}

%build
install -d build
cd build
# .pc file generation expects relative CMAKE_INSTALL_*DIR
%cmake .. \
	-DCMAKE_INSTALL_INCLUDEDIR:PATH=include \
	-DCMAKE_INSTALL_LIBDIR:PATH=%{_lib} \
	-DSPIRV_CROSS_SHARED=ON \
	%{!?with_static_libs:-DSPIRV_CROSS_STATIC=OFF}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/spirv-cross
%{_libdir}/libspirv-cross-c-shared.so.*.*.*
%ghost %{_libdir}/libspirv-cross-c-shared.so.0

%files devel
%defattr(644,root,root,755)
%{_libdir}/libspirv-cross-c-shared.so
%{_includedir}/spirv_cross
%{_pkgconfigdir}/spirv-cross-c-shared.pc
%{_datadir}/spirv_cross_c_shared

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libspirv-cross-c.a
%{_libdir}/libspirv-cross-core.a
%{_libdir}/libspirv-cross-cpp.a
%{_libdir}/libspirv-cross-glsl.a
%{_libdir}/libspirv-cross-hlsl.a
%{_libdir}/libspirv-cross-msl.a
%{_libdir}/libspirv-cross-reflect.a
%{_libdir}/libspirv-cross-util.a
%{_pkgconfigdir}/spirv-cross-c.pc
%{_datadir}/spirv_cross_c
%{_datadir}/spirv_cross_core
%{_datadir}/spirv_cross_cpp
%{_datadir}/spirv_cross_glsl
%{_datadir}/spirv_cross_hlsl
%{_datadir}/spirv_cross_msl
%{_datadir}/spirv_cross_reflect
%{_datadir}/spirv_cross_util
%endif
