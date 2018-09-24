Name:		portal-pycurl
Version:	1.0.0.0
Release:	1
Summary:	None

Group:	None
License:	None
URL:		None
Source0:	pycurl.tar.gz

BuildRequires:	python2
Requires:	python2

%description


%global debug_package %{nil}

%prep
%setup -q -c -n %{name}-%{version}


%build


%install
mkdir -p %{buildroot}/usr/bin
cp %{_builddir}/%{name}-%{version}/pycurl.py %{buildroot}/usr/bin/pycurl.py

%files
%attr(755,root,root) /usr/bin/pycurl.py


%changelog

