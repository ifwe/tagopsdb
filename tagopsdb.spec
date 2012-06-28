%define _topdir    %(pwd)
%define _tmppath   %{_topdir}
%define _builddir  %{_tmppath}
%define _buildrootdir %{_tmppath}

%define _rpmtopdir    %{_topdir}
%define _sourcedir    %{_rpmtopdir}
%define _specdir      %{_topdir}
%define _rpmdir       %{_topdir}
%define _srcrpmdir    %{_topdir}
%define _rpmfilename  %%{NAME}-%%{VERSION}-%%{RELEASE}.%%{ARCH}.rpm

%if 0%{?rhel} >= 6
%global __python python
%global pybase %{__python}
%global tagbase TAGpython
%else
%global __python python2.6
%global pybase python26
%global tagbase TAGpython26
%endif

%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from %distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:           %{tagbase}-tagopsdb
Version:        %(%{__python} setup.py --version)
Release:        1%{?dist}
Summary:        Python interface to TagOpsDB database

Group:          Development/Languages
License:        Apache License, Version 2.0
URL:            None
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  %{pybase}-devel

#Requires: %{tagbase}-oursql
#Requires: %{tagbase}-sqlalchemy


%description
A Python library that contains various methods used to access the information
in the TagOpsDB library.


%build
%{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
# Note: use --install-scripts <path> for alternate location of programs
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
 

%clean
%{__python} setup.py clean --all
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc
%{python_sitelib}/*


%changelog
* Wed Jun 27 2012 Kenneth Lareau <klareau tagged com> - 0.1.0-1
- Initial version
