Name:           gpsd
Version:        2.33
Release:        3%{?dist}
Summary:        Service daemon for mediating access to a GPS

Group:          System Environment/Daemons
License:        BSD
URL:            http://developer.berlios.de/projects/gpsd/
Source0:        http://download.berlios.de/gpsd/%{name}-%{version}.tar.gz
Source1:        xgps.desktop
Source2:        xgpsspeed.desktop
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: dbus-devel dbus-glib-devel ncurses-devel xmlto python
BuildRequires: openmotif-devel libXaw-devel desktop-file-utils

Requires(post):    /sbin/ldconfig
Requires(postun):  /sbin/ldconfig

%description 
gpsd is a service daemon that mediates access to a GPS sensor
connected to the host computer by serial or USB interface, making its
data on the location/course/velocity of the sensor available to be
queried on TCP port 2947 of the host computer.  With gpsd, multiple
GPS client applications (such as navigational and wardriving software)
can share access to a GPS without contention or loss of data.  Also,
gpsd responds to queries with a format that is substantially easier to
parse than NMEA 0183.  

%package devel
Summary:        Client libraries in C and Python for talking to a running gpsd or GPS
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description devel
This package provides C header files for the gpsd shared libraries
that manage access to a GPS for applications; also Python modules.

%package        clients
Summary:        Clients for gpsd
Group:          Applications/System

%description clients
xgps is a simple test client for gpsd with an X interface. It displays
current GPS position/time/velocity information and (for GPSes that
support the feature) the locations of accessible satellites.

xgpsspeed is a speedometer that uses position information from the GPS.
It accepts an -h option and optional argument as for gps, or a -v option
to dump the package version and exit. Additionally, it accepts -rv
(reverse video) and -nc (needle color) options.

cgps resembles xgps, but without the pictorial satellite display.  It
can run on a serial terminal or terminal emulator.

%prep
%setup -q

%build
%configure --enable-dbus --disable-static
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}

%makeinstall
# additional gpsd files
mkdir -p %{buildroot}%{_libdir}/X11/app-defaults/
cp xgps.ad %{buildroot}%{_libdir}/X11/app-defaults/xgps
cp xgpsspeed.ad %{buildroot}%{_libdir}/X11/app-defaults/xgpsspeed
mkdir -p %{buildroot}%{_sysconfdir}/hotplug/usb
cp gpsd.hotplug gpsd.usermap %{buildroot}%{_sysconfdir}/hotplug/usb/
# additional gpsd-devel files
mkdir -p %{buildroot}%{_datadir}/gpsd
PYVERSION=`python -c "import sys; print sys.version[:3]"`
mkdir -p %{buildroot}%{_libdir}/python${PYVERSION}/site-packages
cp gps.py gpsfake.py %{buildroot}%{_libdir}/python${PYVERSION}/site-packages

#remove nasty little .la files
rm -f %{buildroot}%{_libdir}/libgps.la

#Install the .desktop files
desktop-file-install --vendor fedora                        \
    --dir %{buildroot}%{_datadir}/applications              \
    --add-category X-Fedora                                 \
    %{SOURCE1}
desktop-file-install --vendor fedora                        \
    --dir %{buildroot}%{_datadir}/applications              \
    --add-category X-Fedora                                 \
    %{SOURCE2}

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc README INSTALL COPYING
%{_sbindir}/gpsd
%{_bindir}/gpsprof
%{_bindir}/sirfmon
%{_libdir}/libgps.so.*
%{_mandir}/man8/gpsd.8*
%{_mandir}/man1/gpsprof.1*
%{_mandir}/man1/sirfmon.1*
%{_sysconfdir}/hotplug/usb/gpsd.hotplug
%{_sysconfdir}/hotplug/usb/gpsd.usermap
%{_libdir}/python*/site-packages/gps.py*

%files devel
%defattr(-,root,root,-)
%doc HACKING TODO
%{_bindir}/gpsfake
%{_bindir}/rtcmdecode
%{_bindir}/gpsflash
%{_libdir}/python*/site-packages/gpsfake.py*
%{_libdir}/libgps.so
%{_includedir}/gps.h
%{_includedir}/libgpsmm.h
%{_includedir}/gpsd.h
%{_mandir}/man1/gpsfake.1*
%{_mandir}/man1/rtcmdecode.1*
%{_mandir}/man1/gpsflash.1*
%{_mandir}/man3/libgps.3*
%{_mandir}/man3/libgpsmm.3*
%{_mandir}/man3/libgpsd.3*
%{_mandir}/man5/rtcm-104.5*
%{_mandir}/man5/srec.5*

%files clients
%defattr(-,root,root,-)
%{_bindir}/xgps
%{_bindir}/xgpsspeed
%{_bindir}/cgps
%{_bindir}/gpspipe
%{_bindir}/gpxlogger
%{_bindir}/cgpxlogger
%{_mandir}/man1/gps.1*
%{_mandir}/man1/gpspipe.1*
%{_mandir}/man1/xgps.1*
%{_mandir}/man1/xgpsspeed.1*
%{_mandir}/man1/cgps.1*
%{_mandir}/man1/cgpxlogger.1*
%{_libdir}/X11/app-defaults/xgps
%{_libdir}/X11/app-defaults/xgpsspeed
%{_datadir}/applications/*.desktop

%changelog
* Thu Jul 20 2006 Matthew Truch <matt at truch.net> - 2.33-3
* Actually, was a missing BR glib-dbus-devel.   Ooops.

* Thu Jul 20 2006 Matthew Truch <matt at truch.net> - 2.33-2
- Missing BR glib-devel

* Thu Jul 20 2006 Matthew Truch <matt at truch.net> - 2.33-1
- Update to version 2.33

* Wed Apr 19 2006 Matthew Truch <matt at truch.net> - 2.32-5
- Don't --enable-tnt in build as it causes some gpses to not work
  properly with sattelite view mode.  See bugzilla bug 189220.

* Thu Apr 13 2006 Matthew Truch <matt at truch.net> - 2.32-4
- Add dbus-glib to BuildRequires as needed for build.

* Sun Apr 9 2006 Matthew Truch <matt at truch.net> - 2.32-3
- Include xmlto and python in buildrequires so things build right.
- Don't package static library file.  

* Wed Apr 5 2006 Matthew Truch <matt at truch.net> - 2.32-2
- Use ye olde %%{?dist} tag.

* Wed Apr 5 2006 Matthew Truch <matt at truch.net> - 2.32-1
- Initial Fedora Extras specfile
