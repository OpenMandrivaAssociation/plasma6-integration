%define plasmaver %(echo %{version} |cut -d. -f1-3)
%define stable %([ "$(echo %{version} |cut -d. -f2)" -ge 80 -o "$(echo %{version} |cut -d. -f3)" -ge 80 ] && echo -n un; echo -n stable)
#define git 20240222
%define gitbranch Plasma/6.0
%define gitbranchd %(echo %{gitbranch} |sed -e "s,/,-,g")

Summary: Qt integration framework with Plasma
Name: plasma6-integration
Version: 6.3.4
Release: %{?git:0.%{git}.}2
%if 0%{?git:1}
Source0:	https://invent.kde.org/plasma/plasma-integration/-/archive/%{gitbranch}/plasma-integration-%{gitbranchd}.tar.bz2#/plasma-integration-%{git}.tar.bz2
%else
Source0: http://download.kde.org//%{stable}/plasma/%{plasmaver}/plasma-integration-%{version}.tar.xz
%endif
Patch0: plasma-integration-5.17.5-allow-configuring-button-order.patch
URL: https://kde.org/
License: GPL
Group: System/Libraries
BuildRequires: cmake(ECM)
BuildRequires: cmake(Breeze)
BuildRequires: cmake(KF6WidgetsAddons)
BuildRequires: cmake(Wayland) >= 5.90.0
BuildRequires: cmake(KF6Notifications)
BuildRequires: cmake(KF6KIO)
BuildRequires: cmake(KF6IconThemes)
BuildRequires: cmake(KF6I18n)
BuildRequires: cmake(KF6ConfigWidgets)
BuildRequires: cmake(KF6Config)
BuildRequires: cmake(KF6WindowSystem)
BuildRequires: cmake(KF6XmlGui)
BuildRequires: cmake(KF6StatusNotifierItem)
BuildRequires: cmake(Qt6)
BuildRequires: cmake(Qt6Core)
BuildRequires: cmake(Qt6Widgets)
BuildRequires: cmake(Qt6DBus)
BuildRequires: cmake(Qt6Test)
BuildRequires: cmake(Qt6Qml)
BuildRequires: cmake(Qt6Quick)
BuildRequires: cmake(Qt6QuickControls2)
BuildRequires: pkgconfig(x11)
BuildRequires: pkgconfig(xcursor)
BuildRequires: pkgconfig(xkbcommon)
BuildRequires: pkgconfig(wayland-client)
BuildRequires: cmake(PlasmaWaylandProtocols)
BuildRequires: noto-sans-fonts
Requires: noto-sans-fonts
Requires: plasma6-breeze

%description
Framework Integration is a set of plugins responsible
for better integration of Qt applications when running
on a KDE Plasma workspace.

%package devel
Summary: Development files for plasma-key-data
Group: Development/C++ and C
Requires: %{name} = %{EVRD}

%description devel
Development files for plasma-key-data.

%prep
%autosetup -p1 -n plasma-integration-%{?git:%{gitbranchd}}%{!?git:%{version}}
%cmake \
	-DBUILD_QCH:BOOL=ON \
	-DBUILD_QT5:BOOL=OFF \
	-DBUILD_QT6:BOOL=ON \
	-DKDE_INSTALL_USE_QT_SYS_PATHS:BOOL=ON \
	-G Ninja

%build
%ninja_build -C build

%install
%ninja_install -C build

%find_lang plasmaintegration5 || touch plasmaintegration5.lang

%files -f plasmaintegration5.lang
%doc README.md
%{_qtdir}/plugins/platformthemes/KDEPlasmaPlatformTheme6.so

%files devel
