%define snap r2137

#Module-Specific definitions
%define mod_name mod_stats
%define mod_conf B17_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Apache module collecting buildservice download statistics
Name:		apache-%{mod_name}
Version:	1.1
Release:	%mkrel 0.%{snap}.1
Group:		System/Servers
License:	Apache License
URL:		http://en.opensuse.org/Build_Service/Redirector
Source0:	%{mod_name}.tar.gz
Source1:	%{mod_conf}
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.2.0
Requires(pre):	apache-mpm-prefork >= 2.2.0
Requires(pre):	apache-mod_zrkadlo
Requires:	apache-conf >= 2.2.0
Requires:	apache >= 2.2.0
Requires:	apache-mod_zrkadlo
BuildRequires:	apache-devel >= 2.2.0
BuildRequires:	apache-mod_form-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Apache module collecting download statistics for packages downloaded from an
OpenSUSE build service. At this time, it is probably only useful on
software.opensuse.org.

%prep

%setup -q -n %{mod_name}

cp %{SOURCE1} %{mod_conf}

%build

%{_sbindir}/apxs -c mod_stats.c

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/httpd/modules.d
install -d %{buildroot}%{_libdir}/apache-extramodules

install -m0755 .libs/%{mod_so} %{buildroot}%{_libdir}/apache-extramodules/
install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
    fi
fi

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README TODO mod_dbd.conf mod_stats.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}
