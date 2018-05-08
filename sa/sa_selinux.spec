# vim: sw=4:ts=4:et

%define selinux_policyver 3.13.1-166

Name:   sa_selinux
Version:	1.0
Release:	1%{?dist}
Summary:	SELinux policy module for sa

Group:	System Environment/Base		
License:	GPLv2+	
# This is an example. You will need to change it.
URL:		http://HOSTNAME
Source0:	sa.pp
Source1:	sa.if
Source2:	sa_selinux.8
Source3:	sa_u

Requires: policycoreutils, libselinux-utils
Requires(post): selinux-policy-base >= %{selinux_policyver}, policycoreutils
Requires(postun): policycoreutils
BuildArch: noarch

%description
This package installs and sets up the  SELinux policy security module for sa.

%install
install -d %{buildroot}%{_datadir}/selinux/packages
install -m 644 %{SOURCE0} %{buildroot}%{_datadir}/selinux/packages
install -d %{buildroot}%{_datadir}/selinux/devel/include/contrib
install -m 644 %{SOURCE1} %{buildroot}%{_datadir}/selinux/devel/include/contrib/
install -d %{buildroot}%{_mandir}/man8/
install -m 644 %{SOURCE2} %{buildroot}%{_mandir}/man8/sa_selinux.8
install -d %{buildroot}/etc/selinux/targeted/contexts/users/
install -m 644 %{SOURCE3} %{buildroot}/etc/selinux/targeted/contexts/users/sa_u 

%post
semodule -n -i %{_datadir}/selinux/packages/sa.pp
if /usr/sbin/selinuxenabled ; then
    /usr/sbin/load_policy
    
    /usr/sbin/semanage user -a -R sa_r sa_u
fi;
exit 0

%postun
if [ $1 -eq 0 ]; then
    semodule -n -r sa
    if /usr/sbin/selinuxenabled ; then
       /usr/sbin/load_policy
       
       /usr/sbin/semanage user -d sa_u
    fi;
fi;
exit 0

%files
%attr(0600,root,root) %{_datadir}/selinux/packages/sa.pp
%{_datadir}/selinux/devel/include/contrib/sa.if
%{_mandir}/man8/sa_selinux.8.*
/etc/selinux/targeted/contexts/users/sa_u 

%changelog
* Tue May  8 2018 YOUR NAME <YOUR@EMAILADDRESS> 1.0-1
- Initial version

