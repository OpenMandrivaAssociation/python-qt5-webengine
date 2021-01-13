%define _enable_debug_packages %{nil}
%define debug_package %{nil}
%define _disable_lto 1
%define _disable_ld_no_undefined 1
%define major %(echo %{version} |cut -d. -f1-2)
%bcond_with python2
%if %{with python2}
# While we build python2 bits that aren't
# compatible with the py3 bytecompiler
%define _python_bytecompile_errors_terminate_build 0
%endif

Summary:	Set of Python bindings for Trolltech's Qt application framework
Name:		python-qt5-webengine
Version:	5.15.2
Release:	1
License:	GPLv2+
Group:		Development/KDE and Qt
Url:		http://www.riverbankcomputing.co.uk/software/pyqt/intro
Source0:	https://pypi.io/packages/source/P/PyQtWebEngine/PyQtWebEngine-%{version}.tar.gz

BuildRequires:	python-sip >= 4.19.10
BuildRequires:	python-qt5-devel
BuildRequires:	python-qt5-qscintilla
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
%{_datadir}/sip/PyQt5/QtWebEngine
%{_datadir}/sip/PyQt5/QtWebEngineCore
%{python_sitearch}/PyQt5/QtWebEngineCore.*
%{python_sitearch}/PyQt5/QtWebEngine.*

#------------------------------------------------------------

%package widgets
Summary:	PyQt 5 widgets
Group:		Development/KDE and Qt
Requires:	%{name} = %{EVRD}

%description widgets
PyQt 5 widgets.

%files widgets
%{_datadir}/sip/PyQt5/QtWebEngineWidgets
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
%{_datadir}/qt5/qsci/api/python/PyQtWebEngine.api

#------------------------------------------------------------

%if %{with python2}
### python2-qt5-webengine

%define py2_name python2-qt5-webengine

%package -n  python2-qt5-webengine
Summary:	Set of Python 2 bindings for Trolltech's Qt application framework
Group:		Development/KDE and Qt
BuildRequires:	pkgconfig(python2)
BuildRequires:	python2dist(enum34)
BuildRequires:	python2-sip >= 4.19.10
BuildRequires:	python2-qt5
BuildRequires:		python2-dbus

%description -n python2-qt5-webengine
PyQt is a set of Python 2 bindings for Trolltech's Qt application framework.

%files -n python2-qt5-webengine
%{_datadir}/python2-sip/PyQt5/QtWebEngine
%{_datadir}/python2-sip/PyQt5/QtWebEngineCore
%{py2_platsitedir}/PyQt5/QtWebEngineCore.*
%{py2_platsitedir}/PyQt5/QtWebEngine.*

#------------------------------------------------------------

%package -n python2-qt5-webengine-widgets
Summary:	PyQt 5 widgets
Group:		Development/KDE and Qt
Requires:	python2-qt5-webengine = %{EVRD}

%description -n python2-qt5-webengine-widgets
PyQt WebEngine 5 widgets.

%files -n python2-qt5-webengine-widgets
%{_datadir}/python2-sip/PyQt5/QtWebEngineWidgets
%{py2_platsitedir}/PyQt5/QtWebEngineWidgets.*
%endif

#------------------------------------------------------------

%prep
%autosetup -n PyQtWebEngine-%{version} -p1

%if %{with python2}
cp -a . %{py2dir}
%endif

%build
python ./configure.py \
	--no-dist-info \
	--qmake="%{_qt5_bindir}/qmake" \
	--pyqt-sipdir="%{_datadir}/sip/PyQt5" \
	--sip="%{_bindir}/sip5" \
	--verbose

#sed -i -e "s,-fstack-protector-strong,,g" _Q*/Makefile
sed -i -e "s,^LIBS .*= ,LIBS = $(python-config --libs) ,g" */Makefile
sed -i -e "s#^LFLAGS .*= #LFLAGS = %{ldflags} #g" */Makefile
sed -i -e "s#-flto##g" */Makefile
%make_build


%if %{with python2}
pushd %{py2dir}
%{__python2} configure.py \
	--qmake="%{_qt5_bindir}/qmake" \
	--pyqt-sipdir="%{_datadir}/python2-sip/PyQt5" \
	--sip="%{_bindir}/python2-sip" \
	--no-dist-info

sed -i -e "s,^LIBS .*= ,LIBS = $(python2-config --libs) ,g" Qt*/Makefile
sed -i -e "s#^LFLAGS .*= #LFLAGS = %{ldflags} #g" */Makefile
sed -i -e "s#-flto##g" */Makefile
%make_build
%endif

%install

%if %{with python2}
### python2-qt5 install
pushd %{py2dir}
%make_install INSTALL_ROOT=%{buildroot} -C %{py2dir}
popd
%endif

%make_install INSTALL_ROOT=%{buildroot}

# ensure .so modules are executable for proper -debuginfo extraction
for i in %{buildroot}%{python_sitearch}/PyQt5/*.so ; do
    test -x $i  || chmod a+rx $i
done
