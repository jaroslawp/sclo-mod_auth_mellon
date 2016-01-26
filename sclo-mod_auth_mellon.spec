%global scl_name_base    mod_auth_mellon
#% global scl_name_version 0
%global scl              %{scl_name_base}%{?scl_name_version}
%scl_package %scl

# do not produce empty debuginfo package
%global debug_package %{nil}

Summary:       Package that installs mod_auth_mellon
Name:          %scl_name
Version:       1.0
Release:       1%{?dist}
Group:         Development/Languages
License:       GPLv2+

Source1:       README
Source2:       LICENSE

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: scl-utils-build
BuildRequires: help2man
# Temporary work-around
BuildRequires: iso-codes

Requires:      %{?scl_prefix}mod_auth_mellon

%description
This is the main package for %scl Software Collection,
that install mod_auth_mellon.


%package runtime
Summary:   Package that handles %scl Software Collection.
Group:     Development/Languages
Requires:  scl-utils
Requires(post): policycoreutils-python libselinux-utils

%description runtime
Package shipping essential scripts to work with %scl Software Collection.


%package build
Summary:   Package shipping basic build configuration
Group:     Development/Languages
Requires:  scl-utils-build

%description build
Package shipping essential configuration macros
to build %scl Software Collection.


%package scldevel
Summary:   Package shipping development files for %scl
Group:     Development/Languages

%description scldevel
Package shipping development files, especially usefull for development of
packages depending on %scl Software Collection.


%prep
%setup -c -T

cat <<EOF | tee enable
export PATH=%{_bindir}:%{_sbindir}\${PATH:+:\${PATH}}
export MANPATH=%{_mandir}:\${MANPATH}
EOF

# generate rpm macros file for depended collections
cat << EOF | tee scldev
%%scl_%{scl_name_base}         %{scl}
%%scl_prefix_%{scl_name_base}  %{scl_prefix}
EOF

# This section generates README file from a template and creates man page
# from that file, expanding RPM macros in the template file.
cat >README <<'EOF'
%{expand:%(cat %{SOURCE1})}
EOF

# copy the license file so %%files section sees it
cp %{SOURCE2} .


%build
# generate a helper script that will be used by help2man
cat >h2m_helper <<'EOF'
#!/bin/bash
[ "$1" == "--version" ] && echo "%{scl_name} %{version} Software Collection" || cat README
EOF
chmod a+x h2m_helper

# generate the man page
help2man -N --section 7 ./h2m_helper -o %{scl_name}.7


%install
install -D -m 644 enable %{buildroot}%{_scl_scripts}/enable
install -D -m 644 scldev %{buildroot}%{_root_sysconfdir}/rpm/macros.%{scl_name_base}-scldevel
install -D -m 644 %{scl_name}.7 %{buildroot}%{_mandir}/man7/%{scl_name}.7

%scl_install


%post runtime
# Simple copy of context from system root to SCL root.
semanage fcontext -a -e /  %{?_scl_root}  &>/dev/null || :
selinuxenabled && load_policy || :
restorecon -R %{?_scl_root}  &>/dev/null || :


%files


%files runtime -f filesystem
%defattr(-,root,root)
%doc README LICENSE
%scl_files
%{_mandir}/man7/%{scl_name}.*


%files build
%defattr(-,root,root)
%{_root_sysconfdir}/rpm/macros.%{scl}-config


%files scldevel
%defattr(-,root,root)
%{_root_sysconfdir}/rpm/macros.%{scl_name_base}-scldevel


%changelog
* Tue Jan 26 2016 Jaroslaw Polok <jaroslaw.polok@cern.ch> - 1.0-1
- initial build based on php55 SC spec.

