Name: libibverbs
Version: 1.1.8
Release: 5%{?dist}
Summary: A library for direct userspace use of RDMA (InfiniBand/iWARP) hardware
Group: System Environment/Libraries
License: GPLv2 or BSD
Url: https://www.openfabrics.org/
Source: https://www.openfabrics.org/downloads/verbs/libibverbs-%{version}.tar.gz
Patch0: libibverbs-1.1.7-arg-fixes.patch
Patch1: 0001-Add-ibv_port_cap_flags.patch
Patch2: 0002-Use-neighbour-lookup-for-RoCE-UD-QPs-Eth-L2-resoluti.patch
Patch3: libibverbs-1.1.8-coverity-fixes.patch
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
%ifnarch ia64 %{sparc}
BuildRequires: valgrind-devel
%endif
BuildRequires: automake, autoconf, libnl3-devel, libtool
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
Requires: rdma
ExcludeArch: s390 s390x

%description
libibverbs is a library that allows userspace processes to use RDMA
"verbs" as described in the InfiniBand Architecture Specification and
the RDMA Protocol Verbs Specification.  This includes direct hardware
access from userspace to InfiniBand/iWARP adapters (kernel bypass) for
fast path operations.

For this library to be useful, a device-specific plug-in module should
also be installed.

%package devel
Summary: Development files for the libibverbs library
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
Header files for the libibverbs library.

%package devel-static
Summary: Static development files for the libibverbs library
Group: System Environment/Libraries
Requires: %{name}-devel = %{version}-%{release}

%description devel-static
Static libraries for the libibverbs library.

%package utils
Summary: Examples for the libibverbs library
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}
Requires: libibverbs-driver.%{_arch}

%description utils
Useful libibverbs1 example programs such as ibv_devinfo, which
displays information about RDMA devices.

%prep
%setup -q
%patch0 -p1 -b .fixes
%patch1 -p1
%patch2 -p1
%patch3 -p1 -b .coverity

%build
autoreconf -i
%ifnarch ia64 %{sparc}
%configure --with-valgrind
%else
%configure
%endif
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags} CFLAGS="$CFLAGS -fno-strict-aliasing"

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install
mkdir -p -m755 %{buildroot}%{_sysconfdir}/libibverbs.d
# remove unpackaged files from the buildroot
rm -f %{buildroot}%{_libdir}/*.la

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%dir %{_sysconfdir}/libibverbs.d
%{_libdir}/libibverbs*.so.*
%doc AUTHORS COPYING ChangeLog README

%files devel
%defattr(-,root,root,-)
%{_libdir}/lib*.so
%{_includedir}/*
%{_mandir}/man3/*

%files devel-static
%defattr(-,root,root,-)
%{_libdir}/*.a

%files utils
%defattr(-,root,root,-)
%{_bindir}/*
%{_mandir}/man1/*

%changelog
* Tue Dec 23 2014 Doug Ledford <dledford@redhat.com> - 1.1.8-5
- Add a specific requires on the rdma package
- Related: bz1164618

* Fri Oct 17 2014 Doug Ledford <dledford@redhat.com> - 1.1.8-4
- Fix one of the coverity bugs in a different way (the original fix
  caused a problem in libmlx4)
- Related: bz1137044

* Thu Oct 09 2014 Doug Ledford <dledford@redhat.com> - 1.1.8-3
- Additional coverity fix
- Related: bz1137044

* Thu Oct 09 2014 Doug Ledford <dledford@redhat.com> - 1.1.8-2
- Update RoCE IP addressing patches to latest version under review
- Build against valgrind on ppc64le
- Fix a coverity found issue
- Resolves: bz1137044

* Tue Jul 22 2014 Doug Ledford <dledford@redhat.com> - 1.1.8-1
- Grab official upstream release.  This includes all of the pre-release
  items we had in the last release except for the IP based RoCE GID
  addressing changes.  So we are still carrying patches for those two
  items
- Upstream fixed the copy-n-paste error that broke flow steering
- Related: bz1094988
- Resolves: bz947308

* Fri Feb 28 2014 Doug Ledford <dledford@redhat.com> - 1.1.7-6
- Add in support for flow steering and IP addressing of UD RoCE QPs
- Resolves: bz1058537, bz1062281

* Thu Jan 23 2014 Doug Ledford <dledford@redhat.com> - 1.1.7-5
- Bring in XRC support from Roland's git repo
- Related: bz1046820

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.1.7-4
- Mass rebuild 2013-12-27

* Wed Jul 31 2013 Doug Ledford <dledford@redhat.com> - 1.1.7-3
- Misc fixes to arg processing

* Wed Jul 17 2013 Doug Ledford <dledford@redhat.com> - 1.1.7-2
- Add -fno-strict-aliasing to CFLAGS
- Fix date mismatch on old changelog entry

* Wed Jul 17 2013 Doug Ledford <dledford@redhat.com> - 1.1.7-1
- Update to latest upstream, drop unneeded patches

* Thu Jun 6 2013 Jon Stanley <jonstanley@gmail.com> - 1.1.6-7
- Fix build on aarch64 (bz969687)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 26 2012 Doug Ledford <dledford@redhat.com> - 1.1.6-5
- Correct the Url and Source tags now that the openfabrics server no longer
  responds if you don't include the www in the link

* Mon Nov 26 2012 Doug Ledford <dledford@redhat.com> - 1.1.6-4
- Minor fixes not yet taken upstream

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jan 03 2012 Doug Ledford <dledford@redhat.com> - 1.1.6-1
- Update to latest upstream release (adds IBoE and FDR/EDR support)

* Mon Aug 15 2011 Kalev Lember <kalevlember@gmail.com> - 1.1.5-5
- Rebuilt for rpm bug #728707

* Wed Jul 20 2011 Doug Ledford <dledford@redhat.com> - 1.1.5-4
- Improve selection of when/where to use valgrind based upon where it is
  available

* Wed Jul 20 2011 Doug Ledford <dledford@redhat.com> - 1.1.5-3
- Change which package actually requires the driver psuedoprovide
  so that a driver library is not needed in order to build the
  base libibverbs package in the build system

* Wed Jul 20 2011 Doug Ledford <dledford@redhat.com> - 1.1.5-2
- Fix rpath in binaries
- Add valgrind support

* Tue Jul 19 2011 Doug Ledford <dledford@redhat.com> - 1.1.5-1
- Update to latest upstream release

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 11 2010 Doug Ledford <dledford@redhat.com> - 1.1.3-4
- Don't try to build on s390(x) as the hardware doesn't exist there

* Sat Dec 05 2009 Doug Ledford <dledford@redhat.com> - 1.1.3-3
- Own the /etc/libibverbs.d directory

* Fri Nov 06 2009 Doug Ledford <dledford@redhat.com> - 1.1.3-2
- Add Requires of -devel package to -devel-static package
- Add Requires of libibverbs-driver (this pulls in the various driver packages
  automatically when the libibverbs package is installed)

* Thu Oct 29 2009 Roland Dreier <rdreier@cisco.com> - 1.1.3-1
- New upstream release

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Apr 16 2008 Roland Dreier <rdreier@cisco.com> - 1.1.2-1
- New upstream release
- Update description to mention RDMA and iWARP, not just InfiniBand
- Add "Requires" tag for libibverbs base package to -devel

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.1.1-3
- Autorebuild for GCC 4.3

* Tue Aug 28 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 1.1.1-2
- Rebuild for selinux ppc32 issue.

* Fri Jun 15 2007 Roland Dreier <rdreier@cisco.com> - 1.1.1-1
- New upstream release

* Wed Apr 11 2007 Roland Dreier <rdreier@cisco.com> - 1.1-1
- New upstream release

* Mon May 22 2006 Roland Dreier <rdreier@cisco.com> - 1.1-0.1.rc2
- New upstream release
- Remove dependency on libsysfs, since it is no longer used
- Put section 3 manpages in devel package.
- Spec file cleanups: remove unused ver macro, improve BuildRoot, add
  Requires for /sbin/ldconfig, split static libraries into
  devel-static package, and don't use makeinstall any more (all
  suggested by Doug Ledford <dledford@redhat.com>).

* Thu May  4 2006 Roland Dreier <rdreier@cisco.com> - 1.0.4-1
- New upstream release

* Tue Mar 14 2006 Roland Dreier <rdreier@cisco.com> - 1.0.3-1
- New upstream release

* Mon Mar 13 2006 Roland Dreier <rdreier@cisco.com> - 1.0.1-1
- New upstream release

* Thu Feb 16 2006 Roland Dreier <rdreier@cisco.com> - 1.0-1
- New upstream release

* Wed Feb 15 2006 Roland Dreier <rolandd@cisco.com> - 1.0-0.5.rc7
- New upstream release

* Sun Jan 22 2006 Roland Dreier <rolandd@cisco.com> - 1.0-0.4.rc6
- New upstream release

* Tue Oct 25 2005 Roland Dreier <rolandd@cisco.com> - 1.0-0.3.rc5
- New upstream release

* Wed Oct  5 2005 Roland Dreier <rolandd@cisco.com> - 1.0-0.2.rc4
- Update to upstream 1.0-rc4 release

* Mon Sep 26 2005 Roland Dreier <rolandd@cisco.com> - 1.0-0.1.rc3
- Initial attempt at Fedora Extras-compliant spec file
