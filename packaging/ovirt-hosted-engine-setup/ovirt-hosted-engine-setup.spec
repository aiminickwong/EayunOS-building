#
# ovirt-hosted-engine-setup -- ovirt hosted engine setup
# Copyright (C) 2013-2016 Red Hat, Inc.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
#

%global         engine ovirt-engine
%global         package_version 1.3.6.1
%global         ovirt_hosted_engine_setup_templates %{_datadir}/%{name}/templates
%global         ovirt_hosted_engine_setup_scripts %{_datadir}/%{name}/scripts
%global         vdsmhooksdir %{_libexecdir}/vdsm/hooks
%global         gluster_hc_available 0


Summary:        oVirt Hosted Engine setup tool
Name:           ovirt-hosted-engine-setup
Version:        1.3.6.1
Release:        1%{?release_suffix}%{?dist}
License:        LGPLv2+
URL:            http://www.ovirt.org
Source0:        http://resources.ovirt.org/pub/ovirt-3.6/src/%{name}/%{name}-%{package_version}.tar.gz
Group:          Applications/System

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch


Requires:       bind-utils
Requires:       genisoimage
Requires:       iptables
Requires:       iptables-services
Requires:       libselinux-python
Requires:       lsof
Requires:       openssh-server
Requires:       openssl
Requires:       python
Requires:       python-ethtool >= 0.6-3
Requires:       python-netaddr
Requires:       sanlock >= 2.8
Requires:       sanlock-python >= 2.8
Requires:       sudo
Requires:       virt-viewer
BuildRequires:  gettext
BuildRequires:  python2-devel

%if 0%{?fedora}
Requires:       qemu-img
%endif
%if 0%{?rhel}
Requires:       qemu-img-rhev
%endif


Requires:       otopi >= 1.4.0
Requires:       ovirt-host-deploy >= 1.4.1
Requires:       ovirt-hosted-engine-ha >= 1.3.5.4
Requires:       %{engine}-sdk-python >= 3.6.3.0
Requires:       ovirt-setup-lib >= 1.0.1
Requires:       glusterfs-cli >= 3.7.2
Requires:       vdsm >= 4.17.28
Requires:       vdsm-cli >= 4.17.28
Requires:       vdsm-python >= 4.17.28


%if %{gluster_hc_available}
Requires:       vdsm-gluster >= 4.17.28
Requires:       glusterfs-server >= 3.7.2
%endif


# Dependencies that will be required by ovirt-host-deploy
# avoiding to have them installed in the middle of the setup
Requires:       dmidecode
Requires:       iproute
Requires:       kexec-tools
Requires:       m2crypto
Requires:       ovirt-vmconsole-host
Requires:       qemu-kvm-tools
Requires:       socat
Requires:       tar
Requires:       tuned
Requires:       util-linux

%description
Hosted Engine setup tool for oVirt project.

%prep
%setup -q -n %{name}-%{package_version}

%build
%configure \
        --docdir="%{_docdir}/%{name}-%{version}" \
        --disable-python-syntax-check \
        %{?conf}
make %{?_smp_mflags}

%install
rm -rf "%{buildroot}"
make %{?_smp_mflags} install DESTDIR="%{buildroot}"

%files
%doc COPYING
%doc README
%dir %{_sysconfdir}/ovirt-hosted-engine-setup.env.d
%dir %{_sysconfdir}/ovirt-hosted-engine
%dir %{_localstatedir}/log/ovirt-hosted-engine-setup
%dir %{_localstatedir}/lib/ovirt-hosted-engine-setup
%dir %{_localstatedir}/lib/ovirt-hosted-engine-setup/answers
%{_sbindir}/hosted-engine
%{_sbindir}/%{name}
%{python_sitelib}/ovirt_hosted_engine_setup/
%{_datadir}/%{name}/
%{_mandir}/man8/*

#move to a separate package?
%{vdsmhooksdir}/before_vm_start/

%changelog
* Wed May 04 2016 Simone Tiraboschi <stirabos@redhat.com> - 1.3.6.1-1
- 1.3.6.1-1

* Tue Apr 26 2016 Simone Tiraboschi <stirabos@redhat.com> - 1.3.6.1-0.0.master
- 1.3.6.1-0.0.master

* Tue Apr 26 2016 Simone Tiraboschi <stirabos@redhat.com> - 1.3.6.0-1
- 1.3.6.0-1

* Tue Mar 29 2016 Simone Tiraboschi <stirabos@redhat.com> - 1.3.5.1-0.0.master
- 1.3.5.1-0.0.master

* Tue Mar 29 2016 Simone Tiraboschi <stirabos@redhat.com> - 1.3.5.0-1
- 1.3.5.0-1

* Tue Mar 15 2016 Simone Tiraboschi <stirabos@redhat.com> - 1.3.4.1-0.0.master
- 1.3.4.1-0.0.master

* Tue Mar 15 2016 Simone Tiraboschi <stirabos@redhat.com> - 1.3.4.0-1
- 1.3.4.0-1

* Tue Feb 23 2016 Rafael Martins <rmartins@redhat.com> - 1.3.3.5-0.0.master
- 1.3.3.5-0.0.master

* Tue Feb 23 2016 Rafael Martins <rmartins@redhat.com> - 1.3.3.4-1
- 1.3.3.4-1

* Wed Feb 17 2016 Sandro Bonazzola <sbonazzo@redhat.com> - 1.3.3.4-0.0.master
- 1.3.3.4-0.0.master

* Wed Feb 17 2016 Sandro Bonazzola <sbonazzo@redhat.com> - 1.3.3.3-1
- 1.3.3.3-1

* Tue Feb 16 2016 Sandro Bonazzola <sbonazzo@redhat.com> - 1.3.3.3-0.0.master
- 1.3.3.3-0.0.master

* Tue Feb 16 2016 Sandro Bonazzola <sbonazzo@redhat.com> - 1.3.3.2-1
- 1.3.3.2-1

* Tue Feb  9 2016 Sandro Bonazzola <sbonazzo@redhat.com> - 1.3.3.2-0.0.master
- 1.3.3.2-0.0.master

* Tue Feb  9 2016 Sandro Bonazzola <sbonazzo@redhat.com> - 1.3.3.1-1
- 1.3.3.1-1

* Wed Jan 27 2016 Simone Tiraboschi <stirabos@redhat.com> - 1.3.3.1-0.0.master
- 1.3.3.1-0.0.master

* Wed Jan 27 2016 Simone Tiraboschi <stirabos@redhat.com> - 1.3.3.0-1
- 1.3.3.0-1

* Tue Jan 19 2016 Sandro Bonazzola <sbonazzo@redhat.com> - 1.3.2.4-0.0.master
- 1.3.2.4-0.0.master

* Tue Jan 19 2016 Sandro Bonazzola <sbonazzo@redhat.com> - 1.3.2.3-1
- 1.3.2.3-1

* Tue Jan 12 2016 Sandro Bonazzola <sbonazzo@redhat.com> - 1.3.2.3-0.0.master
- 1.3.2.3-0.0.master

* Tue Jan 12 2016 Sandro Bonazzola <sbonazzo@redhat.com> - 1.3.2.2-2
- Updated deps

* Tue Jan 05 2016 Simone Tiraboschi <stirabos@redhat.com> - 1.3.2.2-1
- 1.3.2.2-1

* Wed Dec 23 2015 Sandro Bonazzola <sbonazzo@redhat.com> - 1.3.2.2-0.0.master
- 1.3.2.2-0.0.master

* Wed Dec 23 2015 Sandro Bonazzola <sbonazzo@redhat.com> - 1.3.2.1-1
- 1.3.2.1-1

* Tue Dec 22 2015 Sandro Bonazzola <sbonazzo@redhat.com> - 1.3.2.1-0.0.master
- 1.3.2.1-0.0.master

* Tue Dec 22 2015 Sandro Bonazzola <sbonazzo@redhat.com> - 1.3.2-1
- 1.3.2-1

* Wed Dec  9 2015 Sandro Bonazzola <sbonazzo@redhat.com> - 1.3.2-0.0.master
- 1.3.2-0.0.master

* Wed Dec  9 2015 Sandro Bonazzola <sbonazzo@redhat.com> - 1.3.1.2-1
- 1.3.1.2-1

* Tue Dec  1 2015 Sandro Bonazzola <sbonazzo@redhat.com> - 1.3.1.2-0.0.master
- 1.3.1.2-0.0.master

* Tue Dec  1 2015 Sandro Bonazzola <sbonazzo@redhat.com> - 1.3.1.1-1
- 1.3.1.1-1

* Tue Nov 24 2015 Sandro Bonazzola <sbonazzo@redhat.com> - 1.3.1.1-0.0.master
- 1.3.1.1-0.0.master

* Tue Nov 24 2015 Sandro Bonazzola <sbonazzo@redhat.com> - 1.3.1-1
- 1.3.1-1

* Tue Oct  6 2015 Sandro Bonazzola <sbonazzo@redhat.com> - 1.3.1-0.0.master
- 1.3.1-0.0.master

* Thu Sep 24 2015 Sandro Bonazzola <sbonazzo@redhat.com> - 1.3.0-1
- 1.3.0-1

* Fri Jul 11 2014 Sandro Bonazzola <sbonazzo@redhat.com> - 1.3.0-0.0.master
- 1.3.0-0.0.master
