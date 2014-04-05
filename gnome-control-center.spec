Summary:	GNOME Control Center
Name:		gnome-control-center
Version:	3.12.0
Release:	1
Epoch:		1
License:	GPL v2+
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/gnome/sources/gnome-control-center/3.12/%{name}-%{version}.tar.xz
# Source0-md5:	d1c0a71bad910e0c03975f5597220d23
URL:		http://www.gnome.org/
BuildRequires:	ModemManager-devel
BuildRequires:	NetworkManager-applet-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	cheese-devel >= 3.12.0
BuildRequires:	colord-gtk-devel
BuildRequires:	dbus-glib-devel
BuildRequires:	evolution-data-server-devel >= 3.12.0
BuildRequires:	flex
BuildRequires:	gettext-devel
BuildRequires:	gnome-desktop-devel >= 3.12.0
BuildRequires:	gnome-menus-devel
BuildRequires:	gnome-settings-daemon-devel >= 1:3.12.0
BuildRequires:	gsettings-desktop-schemas-devel >= 3.12.0
BuildRequires:	gstreamer-plugins-base-devel >= 1.2.0
BuildRequires:	intltool
BuildRequires:	krb5-devel
BuildRequires:	libcanberra-gtk3-devel
BuildRequires:	libgtop-devel
BuildRequires:	libpwquality-devel
BuildRequires:	libsocialweb-devel
BuildRequires:	libtool
BuildRequires:	libwacom-devel
BuildRequires:	libxml2-devel
BuildRequires:	nautilus-devel >= 3.12.0
BuildRequires:	polkit-devel
BuildRequires:	pulseaudio-devel
BuildRequires:	tzdata
BuildRequires:	upower-devel
BuildRequires:	xorg-libXxf86misc-devel
BuildRequires:	xorg-libxkbfile-devel
Requires(post,postun):	/usr/bin/gtk-update-icon-cache
Requires(post,postun):	desktop-file-utils
Requires:	gnome-settings-daemon
Requires:	gstreamer-plugins-base
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_libdir}/gnome-control-center

%description
A Configuration tool for easily setting up your GNOME environment.

%package devel
Summary:	GNOME Control Center header files
Group:		X11/Development/Libraries

%description devel
GNOME Control-Center header files.

%prep
%setup -q

# kill gnome common deps
%{__sed} -i -e 's/GNOME_COMPILE_WARNINGS.*//g'	\
    -i -e 's/GNOME_MAINTAINER_MODE_DEFINES//g'	\
    -i -e 's/GNOME_COMMON_INIT//g'		\
    -i -e 's/GNOME_DEBUG_CHECK//g' configure.ac

%build
%{__glib_gettextize}
%{__intltoolize}
%{__libtoolize}
%{__aclocal} -I m4 -I libgd
%{__autoheader}
%{__autoconf}
%{__automake}
%configure \
	--disable-ibus		\
	--disable-silent-rules	\
	--disable-static	\
	--disable-update-mimedb	\
	--with-cheese
%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/locale/{ca@valencia,en@shaw}

%find_lang %{name} --with-gnome --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database
%update_icon_cache hicolor

%postun
%update_desktop_database
%update_icon_cache hicolor

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/gnome-control-center

%dir %{_libexecdir}
%attr(755,root,root) %{_libexecdir}/cc-remote-login-helper
%attr(755,root,root) %{_libexecdir}/gnome-control-center-search-provider

%{_datadir}/polkit-1/actions/org.gnome.controlcenter.datetime.policy
%{_datadir}/polkit-1/actions/org.gnome.controlcenter.remote-login-helper.policy
%{_datadir}/polkit-1/actions/org.gnome.controlcenter.user-accounts.policy
%{_datadir}/polkit-1/rules.d/gnome-control-center.rules

%{_datadir}/dbus-1/services/org.gnome.ControlCenter.SearchProvider.service
%{_datadir}/dbus-1/services/org.gnome.ControlCenter.service
%{_datadir}/gnome-control-center
%{_datadir}/gnome-shell/search-providers/gnome-control-center-search-provider.ini
%{_datadir}/sounds/gnome

%{_iconsdir}/hicolor/*/*/*.*
%{_desktopdir}/*.desktop
%{_pixmapsdir}/faces

%{_mandir}/man1/gnome-control-center.1*

%files devel
%defattr(644,root,root,755)
%{_npkgconfigdir}/*.pc

