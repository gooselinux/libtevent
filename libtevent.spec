Name: libtevent
Version: 0.9.8
Release: 8%{?dist}
Group: System Environment/Daemons
Summary: The tevent library
License: LGPLv3+
URL: http://tevent.samba.org/
Source: http://samba.org/ftp/tevent/tevent-%{version}.tar.gz
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

Patch1: tevent-098-add_abi_scripts_and_fix_exports.patch
Patch3: tevent_signal_segfault.patch

BuildRequires: libtalloc-devel >= 2.0.0

%description
Tevent is an event system based on the talloc memory management library.
Tevent has support for many event types, including timers, signals, and
the classic file descriptor events.
Tevent also provide helpers to deal with asynchronous code providing the
tevent_req (Tevent Request) functions.

%package devel
Group: Development/Libraries
Summary: Developer tools for the Tevent library
Requires: libtevent = %{version}-%{release}
Requires: libtalloc-devel >= 2.0.0
Requires: pkgconfig

%description devel
Header files needed to develop programs that link against the Tevent library.

%prep
%setup -q -n tevent-%{version}

%patch1 -p1 -b .abi_checks
%patch3 -p1 -b .tevent_signal_segv

%build
%configure
make %{?_smp_mflags}

%check
make %{?_smp_mflags} check

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

ln -s libtevent.so.%{version} $RPM_BUILD_ROOT%{_libdir}/libtevent.so.0
ln -s libtevent.so.%{version} $RPM_BUILD_ROOT%{_libdir}/libtevent.so

rm -f $RPM_BUILD_ROOT%{_libdir}/libtevent.a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_libdir}/libtevent.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/tevent.h
%{_libdir}/libtevent.so
%{_libdir}/pkgconfig/tevent.pc

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%changelog
* Fri May 21 2010 Stephen Gallagher <sgallagh@redhat.com> - 0.9.8-8
- Run make check during RPM build
- Fix abi_check patch to guarantee script executability

* Wed Feb 24 2010 Stephen Gallagher <sgallagh@redhat.com> - 0.9.8-7.1
- Remove all references to ABI compatibility patch

* Wed Feb 24 2010 Stephen Gallagher <sgallagh@redhat.com> - 0.9.8-7
- Drop ABI compatibility patch (no longer needed)

* Wed Sep 23 2009 Simo Sorce <ssorce@redhat.com> - 0.9.8-5
- Add patch to fix a segfault case

* Wed Sep 16 2009 Simo Sorce <ssorce@redhat.com> - 0.9.8-2
- Fix abi compatibility with 0.9.3

* Sat Sep 8 2009 Simo Sorce <ssorce@redhat.com> - 0.9.8-1
- First independent release for tevent 0.9.8
