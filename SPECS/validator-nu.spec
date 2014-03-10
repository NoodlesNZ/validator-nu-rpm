%define builddate   20140222

Name:           validator-nu
Version:        1.0
Release:        %{builddate}%{?dist}
Summary:        Standalone validator.nu
Group:          Applications/Internet
License:        GPL
URL:            https://github.com/validator/validator.github.io/releases/download/%{builddate}/vnu-%{builddate}.zip
Packager:       Nick Le Mouton <nick.lemouton@drugs.com>
Source0:        vnu-%{builddate}.zip
Source1:				vnu-init.d
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      noarch
Requires:       java

%description
Standalone java service for validating HTML5

%prep
%setup -q -n vnu

%build

%install
%{__rm} -rf %{buildroot}

%{__mkdir_p} %{buildroot}/opt/validator-nu
%{__install} -Dp -m0644 vnu.jar %{buildroot}/opt/validator-nu/
%{__install} -Dp -m0755 %{SOURCE1} %{buildroot}%{_sysconfdir}/rc.d/init.d/validator-nu
%{__install} -d -m0750 %{buildroot}%{_localstatedir}/log/validator

%pre
getent group validator >/dev/null || groupadd -r validator
getent passwd validator >/dev/null || \
    useradd -r -g validator -d /opt/validator-nu \
    -s /sbin/nologin -c "%{name} daemon" validator
exit 0

%preun
service %{name} stop
exit 0

%postun
if [ $1 = 0 ]; then
	chkconfig --del %{name}
	getent passwd validator >/dev/null && \
	userdel -r validator 2>/dev/null
fi
exit 0

%clean
%{__rm} -rf %{buildroot}

%files
/opt/validator-nu/vnu.jar
%config %{_initrddir}/validator-nu
%defattr(-, validator, validator, 0750)
%{_localstatedir}/log/validator


%changelog
* Mon Mar 10 2014 Nick Le Mouton <nick@noodles.net.nz> 1.0-20140222
- initial build
