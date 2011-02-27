Name:           gargoyle
Version:        2010.1
Release:        1%{?dist}
Summary:        Interactive fiction interpreter with excellent text rendering

Group:          Amusements/Games
# As Gargoyle contains several bundled interpreters, we end up with multiple licenses.
# See License.txt for an overview.
License:        GPLv2 and GPLv2+ and BSD and MIT and (Freely redistributable without restriction)
URL:            http://ccxvii.net/gargoyle/
# This is not the original source zip because the original contains non-free code
# Original download URL: http://garglk.googlecode.com/files/gargoyle-2010.1-sources.zip
Source0:        gargoyle-2010.1.tar.bz2
Source1:        gargoyle.6
Source2:        README.fedora
Patch0:         support-dir-not-needed.patch
Patch1:         fix-build.patch
Patch2:         gargoyle-fix-desktop-file.patch
Patch3:         remove-Alan.patch
Patch4:         remove-Hugo.patch
Patch5:         remove-luximono-font.patch
Patch6:         fix-font-config.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  jam,SDL-devel,SDL_sound-devel,SDL_mixer-devel,gtk2-devel,freetype-devel,libjpeg-turbo-devel,smpeg-devel,desktop-file-utils
Requires:       smpeg-libs,linux-libertine-fonts,liberation-mono-fonts

%description
Gargoyle is an interpreter for interactive fiction (text adventure) story files
which supports all major formats and places special emphasis on excellent text
rendering.

See http://ifdb.tads.org/ and http://www.ifarchive.org/ for many free works.

This package excludes the Alan 2, Alan 3 and Hugo interpreters due to licensing
restrictions.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p2
%patch1 -p2
%patch2 -p2
%patch3 -p2
%patch4 -p2
%patch5 -p2
%patch6 -p2

%build
sed -i "s/_OPTFLAGS_/%{optflags}/" Jamrules
jam

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
chmod 755 %{buildroot}/%{_libexecdir}/%{name}/*
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
%defattr(-,root,root,-)
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
* Thu Feb 24 2011 Carlo Teubner <carlo.teubner@gmail.com> 2010.1-1
- Initial creation of Fedora package
