Name:           gargoyle
Version:        2011.1
Release:        1%{?dist}
Summary:        Interactive fiction interpreter with excellent text rendering

Group:          Amusements/Games
# As Gargoyle contains several bundled interpreters, we end up with multiple licenses.
# See License.txt for an overview.
License:        GPLv2 and GPLv2+ and BSD and MIT and Artistic 2.0 and Glulxe
URL:            http://ccxvii.net/gargoyle/
# This is not the upstream source zip file because it contains non-free code.
# Original download URL: http://garglk.googlecode.com/files/gargoyle-2011.1-sources.zip
# To go from upstream sources to the tarball we use, run generate-tarball.sh
# (included only for informational purposes, not used or installed)
Source0:        gargoyle-2011.1.tar.bz2
Source1:        gargoyle.6
Source2:        README.fedora
Source3:        generate-tarball.sh
Patch0:         remove-smpeg.patch
Patch1:         remove-Hugo.patch
Patch2:         remove-luximono-font.patch
Patch3:         fix-font-config.patch

BuildRequires:  jam,SDL-devel,SDL_sound-devel,SDL_mixer-devel,gtk2-devel,freetype-devel,libjpeg-turbo-devel,desktop-file-utils
Requires:       linux-libertine-fonts,liberation-mono-fonts

%description
Gargoyle is an interpreter for interactive fiction (text adventure) story files
which supports all major formats and places special emphasis on excellent text
rendering.

See http://ifdb.tads.org/ and http://www.ifarchive.org/ for many free works.

This package excludes the Hugo interpreter due to licensing restrictions.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p2
%patch1 -p2
%patch2 -p2
%patch3 -p2

%build
jam -s CFLAGS="%{optflags}"

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}
mkdir -p %{buildroot}/%{_bindir}
jam \
  -s DESTDIR=%{buildroot} \
  -s _BINDIR=%{_libexecdir}/%{name} \
  -s _APPDIR=%{_libexecdir}/%{name} \
  -s _LIBDIR=%{_libdir}/%{name} \
  install
chmod 755 %{buildroot}/%{_libexecdir}/%{name}/* %{buildroot}/%{_libdir}/%{name}/libgarglk.so
ln -s %{_libexecdir}/%{name}/%{name} %{buildroot}/%{_bindir}/%{name}
ln -s %{_libdir}/%{name}/libgarglk.so %{buildroot}/%{_libdir}/libgarglk.so

# Install config file
mkdir -p %{buildroot}/%{_sysconfdir}
install -pm 644 garglk/garglk.ini %{buildroot}/%{_sysconfdir}/

# Install man pages
mkdir -p %{buildroot}/%{_mandir}/man6
install -pm 644 %{SOURCE1} %{buildroot}/%{_mandir}/man6/
cp -p %{SOURCE2} .

# Install desktop file and icon
mkdir -p %{buildroot}/%{_datadir}/pixmaps
mkdir -p %{buildroot}/%{_datadir}/applications
install -pm 644 garglk/gargoyle-house.png %{buildroot}/%{_datadir}/pixmaps
desktop-file-install \
  --dir %{buildroot}/%{_datadir}/applications \
  garglk/gargoyle.desktop

%files
%{_bindir}/%{name}
%{_libdir}/libgarglk.so
%{_libdir}/%{name}
%{_libexecdir}/%{name}
%{_datadir}/applications/gargoyle.desktop
%{_datadir}/pixmaps/gargoyle-house.png
%{_mandir}/man6/%{name}.6*
%config(noreplace) %{_sysconfdir}/garglk.ini
%doc License.txt README.fedora

%changelog
* Wed Dec 21 2011 Carlo Teubner <carlo.teubner@gmail.com> 2011.1-1
- New upstream version 2011.1
- No longer need to exclude the Alan interpreters
- Repackage for Fedora 16
* Sat Jul 02 2011 Carlo Teubner <carlo.teubner@gmail.com> 2010.1-4
- Repackage for Fedora 15
- Fix permissions on generate-tarball.sh
- Change license for Glulxe from "Freely redistributable without restriction"
  to "Glulxe", as recommended in
  http://lists.fedoraproject.org/pipermail/legal/2011-June/001684.html
* Sat May 14 2011 Carlo Teubner <carlo.teubner@gmail.com> 2010.1-3
- Add generate-tarball.sh script to SRPM
* Sun Mar 06 2011 Carlo Teubner <carlo.teubner@gmail.com> 2010.1-2
- Do not link against smpeg, and target the official Fedora repository instead
  of RPM Fusion
* Thu Feb 24 2011 Carlo Teubner <carlo.teubner@gmail.com> 2010.1-1
- Initial creation of Fedora package
