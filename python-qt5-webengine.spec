%define _empty_manifest_terminate_build 0
%define _disable_lto 1
%define _disable_ld_no_undefined 1
%define major %(echo %{version} |cut -d. -f1-2)

Summary:	Set of Python bindings for Trolltech's Qt application framework
Name:		python-qt5-webengine
Version:	5.15.2
Release:	3
License:	GPLv2+
Group:		Development/KDE and Qt
Url:		http://www.riverbankcomputing.co.uk/software/pyqt/intro
Source0:	https://pypi.io/packages/source/P/PyQtWebEngine/PyQtWebEngine-%{version}.tar.gz

BuildRequires:	python-sip >= 5.1.0
BuildRequires:	python-qt5-devel
#BuildRequires:	python-qt5-qscintilla
BuildRequires:	python-qt-builder
BuildRequires:	python-sip-qt5
BuildRequires:	qmake5
BuildRequires:	qt5-qtbase-macros
BuildRequires:	sed
BuildRequires:	pkgconfig(python3)
BuildRequires:	pkgconfig(Qt5Core)
BuildRequires:	pkgconfig(Qt5DBus)
BuildRequires:	cmake(Qt5Designer)
BuildRequires:	cmake(Qt5WebEngine)
BuildRequires:	cmake(Qt5WebEngineCore)
BuildRequires:	cmake(Qt5WebEngineWidgets)
BuildRequires:	pkgconfig(Qt5Gui)
BuildRequires:	pkgconfig(Qt5Help)
BuildRequires:	pkgconfig(Qt5Location)
BuildRequires:	pkgconfig(Qt5Multimedia)
BuildRequires:	pkgconfig(Qt5MultimediaWidgets)
BuildRequires:	pkgconfig(Qt5Network)
BuildRequires:	pkgconfig(Qt5NetworkAuth)
BuildRequires:	pkgconfig(Qt5Nfc)
BuildRequires:	pkgconfig(Qt5OpenGL)
BuildRequires:	pkgconfig(Qt5Positioning)
BuildRequires:	pkgconfig(Qt5PrintSupport)
BuildRequires:	pkgconfig(Qt5Qml)
BuildRequires:	pkgconfig(Qt5Quick)
BuildRequires:	pkgconfig(Qt5QuickWidgets)
BuildRequires:	pkgconfig(Qt5Sensors)
BuildRequires:	pkgconfig(Qt5SerialPort)
BuildRequires:	pkgconfig(Qt5Sql)
BuildRequires:	pkgconfig(Qt5Svg)
BuildRequires:	pkgconfig(Qt5Test)
BuildRequires:	pkgconfig(Qt5RemoteObjects)
BuildRequires:	pkgconfig(Qt5WebChannel)
BuildRequires:	pkgconfig(Qt5WebEngineWidgets)
BuildRequires:	pkgconfig(Qt5WebKit)
BuildRequires:	pkgconfig(Qt5WebKitWidgets)
BuildRequires:	pkgconfig(Qt5WebSockets)
BuildRequires:	pkgconfig(Qt5Widgets)
BuildRequires:	pkgconfig(Qt5XmlPatterns)
BuildRequires:	pkgconfig(Qt5X11Extras)

%description
PyQt is a set of Python bindings for Trolltech's Qt application framework.

%files
%{python_sitearch}/PyQt5/QtWebEngineCore.*
%{python_sitearch}/PyQt5/QtWebEngine.*
%{python_sitearch}/PyQtWebEngine-*.dist-info

#------------------------------------------------------------

%package widgets
Summary:	PyQt 5 widgets
Group:		Development/KDE and Qt
Requires:	%{name} = %{EVRD}

%description widgets
PyQt 5 widgets.

%files widgets
%{python_sitearch}/PyQt5/QtWebEngineWidgets.*

#------------------------------------------------------------

%package devel
Summary:	PyQt 5 devel
Group:		Development/KDE and Qt
Requires:	%{name} = %{EVRD}
Requires:	qt5-designer

%description devel
PyQt 5 devel utilities.

%files devel
%{python_sitearch}/PyQt5/bindings/QtWebEngine
%{python_sitearch}/PyQt5/bindings/QtWebEngineCore
%{python_sitearch}/PyQt5/bindings/QtWebEngineWidgets

#------------------------------------------------------------

%prep
%autosetup -n PyQtWebEngine-%{version} -p1
sip-build --no-make

%build
%make_build -C build

%install
%make_install INSTALL_ROOT=%{buildroot} -C build

# ensure .so modules are executable for proper -debuginfo extraction
for i in %{buildroot}%{python_sitearch}/PyQt5/*.so ; do
    test -x $i  || chmod a+rx $i
done
