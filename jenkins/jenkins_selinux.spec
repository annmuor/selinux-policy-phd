# vim: sw=4:ts=4:et


%define relabel_files() \
restorecon -R /etc/rc.d/init.d/jenkins; \
restorecon -R /var/lib/jenkins; \
restorecon -R /var/log/jenkins; \
restorecon -R /var/cache/jenkins; \

%define selinux_policyver 3.13.1-166

Name:   jenkins_selinux
Version:	1.0.5
Release:	2%{?dist}
Summary:	SELinux policy module for jenkins

Group:	System Environment/Base
License:	GPLv2+
# This is an example. You will need to change it.
URL:		http://HOSTNAME
Source0:	jenkins.pp
Source1:	jenkins.if
Source2:	jenkins_selinux.8


Requires: policycoreutils, libselinux-utils
Requires(post): selinux-policy-base >= %{selinux_policyver}, policycoreutils
Requires(postun): policycoreutils
Requires(post): jenkins
BuildArch: noarch

%description
This package installs and sets up the  SELinux policy security module for jenkins.

%install
install -d %{buildroot}%{_datadir}/selinux/packages
install -m 644 %{SOURCE0} %{buildroot}%{_datadir}/selinux/packages
install -d %{buildroot}%{_datadir}/selinux/devel/include/contrib
install -m 644 %{SOURCE1} %{buildroot}%{_datadir}/selinux/devel/include/contrib/
install -d %{buildroot}%{_mandir}/man8/
install -m 644 %{SOURCE2} %{buildroot}%{_mandir}/man8/jenkins_selinux.8
install -d %{buildroot}/etc/selinux/targeted/contexts/users/


%post
semodule -n -i %{_datadir}/selinux/packages/jenkins.pp
if /usr/sbin/selinuxenabled ; then
    /usr/sbin/load_policy
    /usr/sbin/semanage port -m -p tcp -t jenkins_port_t 8080
    %relabel_files

fi;
exit 0

%postun
if [ $1 -eq 0 ]; then
    semodule -n -r jenkins
    if /usr/sbin/selinuxenabled ; then
       /usr/sbin/semanage port -d -p tcp 8080
       /usr/sbin/load_policy
       %relabel_files

    fi;
fi;
exit 0

%files
%attr(0600,root,root) %{_datadir}/selinux/packages/jenkins.pp
%{_datadir}/selinux/devel/include/contrib/jenkins.if
%{_mandir}/man8/jenkins_selinux.8.*


%changelog
* Mon May  7 2018 Ivan Agarkov <i_agarkov@waraming.net> 1.0.4-1
- Dontaudit rules
* Mon May  7 2018 Ivan Agarkov <i_agarkov@wargaming.net> 1.0-1
- Initial version

