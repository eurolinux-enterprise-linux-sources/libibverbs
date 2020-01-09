Name: libibverbs
Version: 1.1.8
Release: 4%{?dist}
Summary: A library for direct userspace use of RDMA (InfiniBand/iWARP) hardware
Group: System Environment/Libraries
License: GPLv2 or BSD
Url: https://www.openfabrics.org/
Source: https://www.openfabrics.org/downloads/verbs/libibverbs-%{version}-rhmodified.tar.gz
Patch0: libibverbs-1.1.7-arg-fixes.patch
Patch1: 0001-Add-ibv_port_cap_flags.patch
Patch2: 0002-Use-neighbour-lookup-for-RoCE-UD-QPs-Eth-L2-resoluti.patch
Patch3: libibverbs-1.1.8-coverity-fixes.patch
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
Requires: rdma
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires: valgrind-devel libnl-devel
ExcludeArch: s390 s390x
Obsoletes: libibverbs-rocee < 1.1.8

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
Obsoletes: libibverbs-rocee-devel < 1.1.8

%description devel
Header files for the libibverbs library.

%package devel-static
Summary: Static development files for the libibverbs library
Group: System Environment/Libraries
Requires: %{name}-devel = %{version}-%{release}
Obsoletes: libibverbs-rocee-devel-static < 1.1.8

%description devel-static
Static libraries for the libibverbs library.

%package utils
Summary: Examples for the libibverbs library
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}
Obsoletes: libibverbs-rocee-utils < 1.1.8
Requires: libibverbs-driver.%{_arch}

%description utils
Useful libibverbs example programs such as ibv_devinfo, which
displays information about RDMA devices.

%prep
%setup -q
#%patch0 -p1 -b .fixes
#%patch1 -p1
#%patch2 -p1
%patch3 -p1 -b .coverity

%build
#autoreconf -i
%configure --with-valgrind
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make CFLAGS="$CFLAGS -fno-strict-aliasing" %{?_smp_mflags}

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
* Tue Feb 24 2015 Doug Ledford <dledford@redhat.com> - 1.1.8-4
- Update RoCE IP addressing patches to latest version under review
- Fix a coverity found issue
- Resolves: bz1119105

* Wed Jul 30 2014 Doug Ledford <dledford@redhat.com> - 1.1.8-3
- Fix the obsoletes tag so it exists on subpackages too
- Related: bz1051211

* Thu Jul 24 2014 Doug Ledford <dledford@redhat.com> - 1.1.8-2
- Add the RoCE IP Address GID support patches
- Create our own tarball that is the three patches we needed
  then autoreconf run with an acceptable version of autotools
  as the version in the build system is too old
- Resolves: bz1051211

* Fri May 30 2014 Doug Ledford <dledford@redhat.com> - 1.1.8-1
- Update to latest upstream release (which adds XRC support,
  infrastructure for verbs extensions, core support for usNIC
  nodes and transports, uverbs extensions, and receive flow
  steering extension)
- The HPN channel in rhel6 is going away and the RoCE capability
  is being folded back into the base OS channel package (aka
  this one).  Provide an Obsoletes tag to cause this package
  to replace the older libibverbs-rocee package from the HPN
  channel
- Resolves: bz854655

* Wed Jul 31 2013 Doug Ledford <dledford@redhat.com> - 1.1.7-1
- Update to latest upstream release
- Remove patches that are now part of upstream
- Fix ibv_srq_pingpong with negative value to -s option
- Resolves: bz879191

* Sun Oct 14 2012 Doug Ledford <dledford@redhat.com> - 1.1.6-5
- Don't print link state on iWARP links as it's always invalid
- Don't try to do ud transfers in excess of port MTU
- Resolves: bz822781

* Thu Apr 05 2012 Doug Ledford <dledford@redhat.com> - 1.1.6-4
- Make passing ib-port=0 an error as ib ports always start with 1
- Related: bz755459

* Wed Mar 21 2012 Doug Ledford <dledford@redhat.com> - 1.1.6-3
- Bump and rebuild against later glibc to quite warning when debugging
- Resolves: bz803136

* Wed Feb 29 2012 Doug Ledford <dledford@redhat.com> - 1.1.6-2
- Make ibv_devinfo return an error when it can't find the requested port
- Resolves: bz755459

* Fri Jan 20 2012 Doug Ledford <dledford@redhat.com> - 1.1.6-1
- Update to latest upstream release (includes FDR link speed capability)
- Related: bz751220, bz750609

* Tue Aug 02 2011 Doug Ledford <dledford@redhat.com> - 1.1.5-3
- Fix the bug for real this time
- Related: bz725016
- Resolves: bz727336

* Mon Aug 01 2011 Doug Ledford <dledford@redhat.com> - 1.1.5-2
- Fix a bug found by rpmdiff
- Related: bz725016

* Fri Jul 22 2011 Doug Ledford <dledford@redhat.com> - 1.1.5-1
- Update to latest upstream version (1.1.4 to 1.1.5)
- Drop libibverbs cow.patch as it is in 1.1.5 already
- Enable valgrind support so memory corruption is easier to debug
- Make sure RPATH entries are removed from programs
- Related: bz725016

* Tue Aug 03 2010 Doug Ledford <dledford@redhat.com> - 1.1.4-2
- Fix COW protection for large pages (bz605276)
- Resolves: bz605276

* Wed Jun 16 2010 Doug Ledford <dledford@redhat.com> - 1.1.4-1
- Update to latest upstream version
- Internal test build

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

* Mon Mar 14 2006 Roland Dreier <rdreier@cisco.com> - 1.0.3-1
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
