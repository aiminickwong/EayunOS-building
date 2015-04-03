#
# ovirt-hosted-engine-ha -- ovirt hosted engine high availability
# Copyright (C) 2013-2014 Red Hat, Inc.
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

%global         package_version 1.2.4
%global         package_name ovirt-hosted-engine-ha
%global         engine_ha_bindir  /usr/share/ovirt-hosted-engine-ha
%global         engine_ha_confdir /etc/ovirt-hosted-engine-ha
%global         engine_ha_libdir  %{python_sitelib}/ovirt_hosted_engine_ha
%global         engine_ha_logdir  /var/log/ovirt-hosted-engine-ha
%global         engine_ha_rundir  /var/run/ovirt-hosted-engine-ha
%global         engine_ha_statedir /var/lib/ovirt-hosted-engine-ha

%global         vdsm_user vdsm
%global         vdsm_group kvm

%if 0%{?fedora} >= 18 || 0%{?rhel} >= 7
%global with_systemd 1
%endif

Summary:        oVirt Hosted Engine High Availability Manager
Name:           ovirt-hosted-engine-ha
Version:        1.2.4
Release:        1%{?release_suffix}%{?dist}
License:        LGPLv2+
URL:            http://www.ovirt.org
Source:         http://resources.ovirt.org/pub/ovirt-3.5/src/%{name}/%{name}-%{package_version}.tar.gz
Group:          Applications/System

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

# FIXME any additional dependencies?
Requires:       python
Requires:       python-daemon
Requires:       sanlock >= 2.8
Requires:       sanlock-python >= 2.8
Requires:       vdsm >= 4.16.7
Requires:       vdsm-cli >= 4.16.7
Requires:       vdsm-python >= 4.16.7

BuildRequires:  python
BuildRequires:  python2-devel
BuildRequires:  python-nose
BuildRequires:  python-mock
BuildRequires:  vdsm-cli >= 4.16.4

%if 0%{?with_systemd}
%{?systemd_requires}
BuildRequires:  systemd
%endif


%description
Hosted engine manager for oVirt project.


%prep
%setup -q -n %{name}-%{package_version}


%build
%configure \
        --docdir="%{_docdir}/%{name}-%{version}" \
        --disable-python-syntax-check \
        %{?conf}
make %{?_smp_mflags}

%check
make test

%install
rm -rf "%{buildroot}"
make %{?_smp_mflags} install DESTDIR="%{buildroot}"

install -dDm 0700 %{buildroot}%{engine_ha_logdir}
install -dDm 0700 %{buildroot}%{engine_ha_rundir}
install -dDm 0700 %{buildroot}%{engine_ha_statedir}

%if 0%{?with_systemd}
# Install the systemd scripts
install -Dm 0755 initscripts/ovirt-ha-agent.init %{buildroot}/usr/lib/systemd/systemd-ovirt-ha-agent
install -Dm 0755 initscripts/ovirt-ha-broker.init %{buildroot}/usr/lib/systemd/systemd-ovirt-ha-broker
install -Dm 0644 initscripts/ovirt-ha-agent.service %{buildroot}%{_unitdir}/ovirt-ha-agent.service
install -Dm 0644 initscripts/ovirt-ha-broker.service %{buildroot}%{_unitdir}/ovirt-ha-broker.service
%else
# Install the SysV init scripts
install -Dm 0755 initscripts/ovirt-ha-agent.init %{buildroot}%{_initrddir}/ovirt-ha-agent
install -Dm 0755 initscripts/ovirt-ha-broker.init %{buildroot}%{_initrddir}/ovirt-ha-broker
%endif

install -dDm 0750 %{buildroot}%{_sysconfdir}/sudoers.d
install -Dm 0440 sudoers/sudoers %{buildroot}%{_sysconfdir}/sudoers.d/60_ovirt-ha


%files
%defattr(-, root, root, -)
%doc COPYING
%doc README
%doc doc/*.html doc/*.js

%dir %{engine_ha_confdir}
%config(noreplace) %{engine_ha_confdir}/agent-log.conf
%config(noreplace) %{engine_ha_confdir}/agent.conf
%config(noreplace) %{engine_ha_confdir}/broker-log.conf
%config(noreplace) %{engine_ha_confdir}/broker.conf

%dir %{engine_ha_confdir}/notifications
%config(noreplace) %{engine_ha_confdir}/notifications/*

%dir %{engine_ha_bindir}
%{engine_ha_bindir}/ovirt-ha-agent
%{engine_ha_bindir}/ovirt-ha-broker

%dir %{engine_ha_libdir}
%{engine_ha_libdir}/*

%if 0%{?with_systemd}
/usr/lib/systemd/systemd-ovirt-ha-agent
/usr/lib/systemd/systemd-ovirt-ha-broker
%{_unitdir}/ovirt-ha-agent.service
%{_unitdir}/ovirt-ha-broker.service
%else
%{_initrddir}/ovirt-ha-agent
%{_initrddir}/ovirt-ha-broker
%endif

%config(noreplace) %{_sysconfdir}/sudoers.d/60_ovirt-ha


%defattr(-, %{vdsm_user}, %{vdsm_group}, -)
%dir %{engine_ha_logdir}
%ghost %dir %{engine_ha_rundir}

%dir %{engine_ha_statedir}
%config(noreplace) %{engine_ha_statedir}/ha.conf


%post
%if 0%{?with_systemd}
%systemd_post ovirt-ha-agent.service
%systemd_post ovirt-ha-broker.service
if [ "$1" -eq 1 ] ; then
#We don't want the service to be started by default before the system
#is configured and Hosted Engine VM deployed
    /usr/bin/systemctl --no-reload disable ovirt-ha-agent.service
    /usr/bin/systemctl --no-reload disable ovirt-ha-broker.service
fi
%endif


%preun
%if 0%{?with_systemd}
%systemd_preun ovirt-ha-agent.service
%systemd_preun ovirt-ha-broker.service
%else
if [ "$1" -eq 0 ]
then
    /sbin/service ovirt-ha-agent stop > /dev/null 2>&1 || :
    /sbin/service ovirt-ha-broker stop > /dev/null 2>&1 || :
    /sbin/chkconfig --del ovirt-ha-agent
    /sbin/chkconfig --del ovirt-ha-broker
fi
%endif


%postun
%if 0%{?with_systemd}
%systemd_postun_with_restart ovirt-ha-agent.service
%systemd_postun_with_restart ovirt-ha-broker.service
%else
if [ "$1" -ge 1 ]; then
    /sbin/service ovirt-ha-agent condrestart > /dev/null 2>&1
    /sbin/service ovirt-ha-broker condrestart > /dev/null 2>&1
fi
exit 0
%endif


%changelog
* Thu Oct  9 2014 Sandro Bonazzola <sbonazzo@redhat.com> - 1.2.4-1
- 1.2.4-1

* Mon Oct  6 2014 Sandro Bonazzola <sbonazzo@redhat.com> - 1.2.3-1
- 1.2.3-1

* Fri Oct  3 2014 Sandro Bonazzola <sbonazzo@redhat.com> - 1.2.3-0.0.master
- 1.2.3-0.0.master

* Thu Oct  2 2014 Sandro Bonazzola <sbonazzo@redhat.com> - 1.2.2-1
- 1.2.2-1

* Tue Sep 30 2014 Sandro Bonazzola <sbonazzo@redhat.com> - 1.2.2-0.0.master
- 1.2.2-0.0.master

* Mon Sep 22 2014 Sandro Bonazzola <sbonazzo@redhat.com> - 1.2.1-1
- 1.2.1-1

* Fri Sep 12 2014 Sandro Bonazzola <sbonazzo@redhat.com> - 1.2.1-0.3.master
- 1.2.1-0.3.master

* Fri Jul 11 2014 Sandro Bonazzola <sbonazzo@redhat.com> - 1.2.1-0.2.master
- 1.2.1-0.2.master

* Fri Jun 20 2014 David Caro <dcaro@redhat.com> - 1.2.1-0.1.master
- Fix missing macro systemd_requires

* Tue Mar 25 2014 Martin Sivak <msivak@redhat.com> - 1.2.1-0.0.master
- Fix in haClient direct API

* Mon Mar 24 2014 Martin Sivak <msivak@redhat.com> - 1.2.0-0.0.master
- New backend interface

* Thu Dec 19 2013 Greg Padgett <gpadgett@redhat.com> - 1.1.0-0.0.master
- New version after 1.0 branch

* Tue Dec 17 2013 Greg Padgett <gpadgett@redhat.com> - 0.1.0-0.10.beta2
- 0.1.0-0.10.beta2

* Tue Dec 10 2013 Sandro Bonazzola <sbonazzo@redhat.com> - 0.1.0-0.9.beta1
- 0.1.0-0.9.beta1

* Tue Dec  3 2013 Sandro Bonazzola <sbonazzo@redhat.com> - 0.1.0-0.8.beta1
- 0.1.0-0.8.beta1

* Fri Nov 22 2013 Sandro Bonazzola <sbonazzo@redhat.com> - 0.1.0-0.7.beta1
- 0.1.0-0.7.beta1

* Tue Nov 19 2013 Sandro Bonazzola <sbonazzo@redhat.com> - 0.1.0-0.6.beta1
- 0.1.0-0.6.beta1

* Tue Nov  5 2013 Sandro Bonazzola <sbonazzo@redhat.com> - 0.1.0-0.5.beta1
- 0.1.0-0.5.beta1

* Tue Oct 29 2013 Sandro Bonazzola <sbonazzo@redhat.com> - 0.1.0-0.4.beta1
- 0.1.0-0.4.beta1

* Tue Oct 15 2013 Yedidyah Bar David <didi@redhat.com> - 0.1.0-0.3.1.beta1
- 0.1.0-0.3.1.beta1

* Tue Oct 15 2013 Sandro Bonazzola <sbonazzo@redhat.com> - 0.1.0-0.3.beta1
- 0.1.0-0.3.beta1

* Fri Sep 27 2013 Sandro Bonazzola <sbonazzo@redhat.com> - 0.1.0-0.2.beta1
- 0.1.0-0.2.beta1

* Fri Sep 13 2013 Sandro Bonazzola <sbonazzo@redhat.com> - 0.1.0-0.1.beta
- 0.1.0-0.1.beta

* Fri May 31 2013 Greg Padgett <gpadgett@redhat.com> - 0.0.0-0.0.master
- Initial add.
