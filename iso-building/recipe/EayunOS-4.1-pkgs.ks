# remove

# rhbz#641494 RFE - add libguestfs
libguestfs

net-tools
iproute
ltrace
firewalld

# keyboard layout
system-config-keyboard-base

# firmware
linux-firmware

#default plugins
ovirt-node-plugin-snmp
ovirt-node-plugin-cim
ovirt-node-plugin-vdsm
ovirt-node-plugin-hosted-engine

# To disable hostonly mode
dracut-config-generic

# Plymouth
plymouth
plymouth-core-libs
plymouth-scripts

# Add EFi support
shim
grub2-efi
efibootmgr

# VDSM hooks
vdsm-hook-checkimages
vdsm-hook-directlun
vdsm-hook-ethtool-options
vdsm-hook-extnet
vdsm-hook-faqemu
vdsm-hook-fileinject
vdsm-hook-floppy
vdsm-hook-hostusb
vdsm-hook-hugepages
vdsm-hook-isolatedprivatevlan
vdsm-hook-macbind
vdsm-hook-macspoof
vdsm-hook-nestedvt
vdsm-hook-numa
vdsm-hook-openstacknet
vdsm-hook-pincpu
vdsm-hook-promisc
vdsm-hook-qemucmdline
vdsm-hook-qos
vdsm-hook-scratchpad
vdsm-hook-smbios
vdsm-hook-spiceoptions
vdsm-hook-sriov
vdsm-hook-vmdisk
vdsm-hook-vmfex

# OpenStack Neutron Integration
openstack-selinux
python-neutron
python-neutronclient
openstack-neutron
openstack-neutron-openvswitch
openstack-neutron-linuxbridge

# EayunOS
-centos-release
eayunos-release
## avoid upstream packages updating
ovirt-hosted-engine-ha = 1.2.4-1.el7

#gluster
vdsm-gluster
