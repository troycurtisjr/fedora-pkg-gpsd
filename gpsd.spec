%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name: gpsd
Version: 2.37
Release: 3%{?dist}
Summary: Service daemon for mediating access to a GPS

Group: System Environment/Daemons
License: BSD
URL: http://developer.berlios.de/projects/gpsd/
Source0: http://download.berlios.de/gpsd/%{name}-%{version}.tar.gz
Source1: xgps.desktop
Source2: xgpsspeed.desktop
Source3: gpsd-logo.png
Patch0: python-pyexecdir-install-gpsd-2.37.patch
Patch1: zero.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: dbus-devel dbus-glib-devel ncurses-devel xmlto python-devel
BuildRequires: lesstif-devel libXaw-devel desktop-file-utils
BuildRequires: python

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

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
Summary: Client libraries in C and Python for talking to a running gpsd or GPS
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
This package provides C header files and python modules for the gpsd shared 
libraries that manage access to a GPS for applications

%package clients
Summary: Clients for gpsd
Group: Applications/System

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
%patch0 -p1
%patch1 -p0


%build
%configure --enable-dbus --disable-static
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

# X11 defaults
%{__install} -d -m 0755 %{buildroot}%{_datadir}/X11/app-defaults/
%{__install} -p -m 0644 xgps.ad %{buildroot}%{_datadir}/X11/app-defaults/xgps
%{__install} -p -m 0644 xgpsspeed.ad \
	%{buildroot}%{_datadir}/X11/app-defaults/xgpsspeed

# hotplug script
%{__install} -d -m 0755 %{buildroot}%{_sysconfdir}/hotplug.d/usb
%{__install} -p -m 0644 gpsd.hotplug gpsd.usermap \
	%{buildroot}%{_sysconfdir}/hotplug.d/usb/

# remove .la files
rm -f %{buildroot}%{_libdir}/libgps.la

# fix non-executable libraries
%{__chmod} +x %{buildroot}%{_libdir}/libgps.so.17.0.0
%{__chmod} +x %{buildroot}%{python_sitearch}/gpspacket.so

# fix non-executable python script
%{__chmod} +x %{buildroot}%{python_sitearch}/gps.py

# Install the .desktop files
desktop-file-install --vendor fedora \
	--dir %{buildroot}%{_datadir}/applications \
	--add-category X-Fedora \
	%{SOURCE1}
desktop-file-install --vendor fedora \
	--dir %{buildroot}%{_datadir}/applications \
	--add-category X-Fedora \
	%{SOURCE2}

# Install logo icon for .desktop files
%{__install} -d -m 0755 %{buildroot}%{_datadir}/gpsd
%{__install} -p -m 0644 %{SOURCE3} %{buildroot}%{_datadir}/gpsd/gpsd-logo.png


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
%{_bindir}/gpsctl
%{_libdir}/libgps.so.*
%{python_sitearch}/gps.py*
%{python_sitearch}/gpspacket.so
%{_mandir}/man8/gpsd.8*
%{_mandir}/man1/gpsprof.1*
%{_mandir}/man1/sirfmon.1*
%{_mandir}/man1/gpsctl.1*
%{_sysconfdir}/hotplug.d/usb/gpsd.hotplug
%{_sysconfdir}/hotplug.d/usb/gpsd.usermap

%files devel
%defattr(-,root,root,-)
%doc TODO
%{_bindir}/gpsfake
%{_bindir}/rtcmdecode
%{_bindir}/gpsflash
%{_libdir}/libgps.so
%{_libdir}/pkgconfig/*.pc
%{python_sitearch}/gpsfake*
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
%{_bindir}/gpscat
%{_mandir}/man1/gps.1*
%{_mandir}/man1/gpspipe.1*
%{_mandir}/man1/xgps.1*
%{_mandir}/man1/xgpsspeed.1*
%{_mandir}/man1/cgps.1*
%{_mandir}/man1/gpscat.1*
%{_mandir}/man1/cgpxlogger.1*
%{_datadir}/X11/app-defaults/xgps
%{_datadir}/X11/app-defaults/xgpsspeed
%{_datadir}/applications/*.desktop
%dir %{_datadir}/gpsd
%{_datadir}/gpsd/gpsd-logo.png


%changelog
* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.37-3
- Rebuild for Python 2.6

* Wed Mar 19 2008 Douglas E. Warner <silfreed@silfreed.net> - 2.37-2
- moving gpspacket.so python lib to main package
- adding zero.patch to make ZEROIZE error go away on fedora 7

* Wed Feb 27 2008 Douglas E. Warner <silfreed@silfreed.net> - 2.37-1
- update to 2.37
- removed install-gpsd_config.h.patch
- installed pkgconfig files in devel package
- added patch to install python modules in sitearch
- removing rpath from inclucded libtool
- moving X11 app-defaults to datadir
- using macros for commands in install; using install instead of cp and mkdir
- cleaning up spaces/tabs for rpmlint

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.34-9
- Autorebuild for GCC 4.3

* Sun Aug 19 2007 Matthew Truch <matt at truch.net> - 2.34-8
- Patch Makefile to also install gpsd_config.h as needed by
  libgpsmm.h.  Redhat BZ 253433.

* Sat Jun 30 2007 Matthew Truch <matt at truch.net> - 2.34-7
- Make sure the logo is actually included (via the spec file).
  I need to wake up before I try even trivial updates.  

* Sat Jun 30 2007 Matthew Truch <matt at truch.net> - 2.34-6
- Learn how to use search and replace (aka fix all instances of
  gpsd-logo.png spelled incorrectly as gspd-logo.png).

* Sat Jun 30 2007 Matthew Truch <matt at truch.net> - 2.34-5
- Fix desktop file and logo file name.

* Sat Jun 30 2007 Matthew Truch <matt at truch.net> - 2.34-4
- Include icon for .desktop files per BZ 241428

* Tue Mar 20 2007 Michael Schwendt <mschwendt[AT]users.sf.net> - 2.34-3
- Bump release for FE5 -> Fedora 7 upgrade path.

* Tue Feb 27 2007 Matthew Truch <matt at truch.net> - 2.34-2
- BR python-devel instead of python to make it build.  

* Tue Feb 27 2007 Matthew Truch <matt at truch.net> - 2.34-1
- Upgrade to 2.34.
- Get rid of %%makeinstall (which was never needed).
- Possibly fix hotplug issuses (BZ 219750).
- Use %%python_sitelib for python site-files stuff.

* Sat Dec 9 2006 Matthew Truch <matt at truch.net> - 2.33-6
- Rebuild to pull in new version of python.

* Tue Sep 26 2006 Matthew Truch <matt at truch.net> - 2.33-5
- Remove openmotif requirment, and switch to lesstif.

* Mon Aug 28 2006 Matthew Truch <matt at truch.net> - 2.33-4
- Bump release for rebuild in prep. for FC6.

* Thu Jul 20 2006 Matthew Truch <matt at truch.net> - 2.33-3
- Actually, was a missing BR glib-dbus-devel. Ooops.

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
