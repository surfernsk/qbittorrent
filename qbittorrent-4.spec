Name: qbittorrent
Summary:  A Bittorrent Client
Version:  4.1.0
Epoch:    1
Release:  3%{?dist}
License:  GPLv2+
URL:  http://sourceforge.net/projects/qbittorrent
Source0:  https://github.com/qbittorrent/qBittorrent/archive/release-%{version}.tar.gz#/qBittorrent-release-%{version}.tar.gz
Source1:  qbittorrent-nox.README

Patch0: QBT-Fix_o_dest_fold.patch

BuildRequires: boost-devel >= 1.60
BuildRequires: asio-devel
BuildRequires: rb_libtorrent-devel >= 1.1.4
BuildRequires: GeoIP-devel
BuildRequires: pkgconfig(Qt5Core) >= 5.5.1
BuildRequires: pkgconfig(Qt5Gui)
BuildRequires: pkgconfig(Qt5Svg)
BuildRequires: qt5-linguist
BuildRequires: qtsingleapplication-qt5-devel
BuildRequires: qtsinglecoreapplication-qt5-devel
BuildRequires: desktop-file-utils
BuildRequires: automake

Requires: python3
%{?_qt5_version:Requires: qt5-qtbase >= %{_qt5_version}}

%description
A Bittorrent client using rb_libtorrent and a Qt5 Graphical User Interface.
It aims to be as fast as possible and to provide multi-OS, unicode support.

%package nox
Summary: A Headless Bittorrent Client
Group: Applications/Internet
BuildRequires: qtsinglecoreapplication-devel

%description nox
A Headless Bittorrent client using rb_libtorrent.
It aims to be as fast as possible and to provide multi-OS, unicode support.

%prep
%setup -q -n "qBittorrent-release-%{version}"
%patch0 -p1
./bootstrap.sh
cp -p %{SOURCE1} .

%build
# use ./configure instead of %%configure as it doesn't work
# configure and make headless first
mkdir -p build-nox
cd build-nox

../configure \
  --prefix=%{_prefix} \
  --disable-gui \
  --disable-silent-rules \
  --with-qtsingleapplication=system \
  --enable-systemd \
  --enable-debug

cp conf.pri ..
make %{?_smp_mflags}
mv -f ../conf.pri ../conf.pri.nox

# configure and make gui version
cd ..
mkdir -p build-gui
cd build-gui

../configure --prefix=%{_prefix}  \
  --disable-silent-rules \
  --with-qtsingleapplication=system \
  --enable-debug

cp conf.pri ..
make %{?_smp_mflags}
mv -f ../conf.pri ../conf.pri.gui

%install
rm -rf $RPM_BUILD_ROOT
# install headless version
mv -f conf.pri.nox conf.pri
cd build-nox
make INSTALL_ROOT=%{buildroot} install
# install gui version
cd ..
mv -f conf.pri.gui conf.pri
cd build-gui
make INSTALL_ROOT=%{buildroot} install

%post nox
%systemd_post %{name}-nox@.service

%preun nox
%systemd_preun %{name}-nox@.service

%postun nox
%systemd_postun %{name}-nox@.service

%post
/usr/bin/update-desktop-database &> /dev/null || :
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
/usr/bin/update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
/usr/bin/update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :


%files
%doc AUTHORS Changelog COPYING NEWS README.md TODO
%doc %{_mandir}/man1/%{name}.1.gz
%{_bindir}/qbittorrent
%{_datadir}/applications/qbittorrent.desktop
%{_datadir}/appdata/qbittorrent.appdata.xml
%{_datadir}/icons/hicolor/*/apps/qbittorrent.png
%{_datadir}/icons/hicolor/*/status/qbittorrent-tray.png
%{_datadir}/icons/hicolor/*/status/qbittorrent-tray-dark.svg
%{_datadir}/icons/hicolor/*/status/qbittorrent-tray-light.svg
%{_datadir}/icons/hicolor/*/status/qbittorrent-tray.svg
%{_datadir}/pixmaps/qbittorrent.png

%files nox
%doc AUTHORS Changelog COPYING NEWS README.md TODO
%doc %{_mandir}/man1/%{name}-nox.1.gz
%{_unitdir}/%{name}-nox@.service
%{_bindir}/qbittorrent-nox


%changelog
* Mon May 14 2018 Evgeny Lensky <surfernsk@gmail.com> - 4.1.0-3
- edit fix open dest folder with gnome >= 3.28

* Mon May 14 2018 Evgeny Lensky <surfernsk@gmail.com> - 4.1.0-2
- add fix open dest folder with gnome >= 3.28

* Sat May 05 2018 Evgeny Lensky <surfernsk@gmail.com> - 4.1.0-1
- bump 4.1.0

* Fri Feb 16 2018 Evgeny Lensky <surfernsk@gmail.com> - 4.0.4-1
- release 4.0.4

* Wed Jan 17 2018 Evgeny Lensky <surfernsk@gmail.com> - 4.0.3-3
- UpIssueFIX f4.0.4:
- Fix natural sorting #8080 #6732.
- Fix application of speed limits on LAN and μTP connections #7745.
- Make peer information flags in peerlist more readable.
- Simplify sorting code.
- Fix sorting of country flags column in Peers tab.

* Mon Jan 01 2018 Evgeny Lensky <surfernsk@gmail.com> - 4.0.3-2
- rebuild with rb_libtorrent 1.1.6

* Mon Dec 18 2017 Evgeny Lensky <surfernsk@gmail.com> - 4.0.3-1
- release 4.0.3

* Fri Dec 01 2017 Evgeny Lensky <surfernsk@gmail.com> - 4.0.2-1
- release to 4.0.2

* Wed Nov 22 2017 Evgeny Lensky <surfernsk@gmail.com> - 4.0.1-1
- release to 4.0.1

* Mon Nov 20 2017 Evgeny Lensky <surfernsk@gmail.com> - 4.0.0-1
- release to 4.0.0
