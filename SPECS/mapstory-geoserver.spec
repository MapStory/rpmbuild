# Define Constants
%define name mapstory-geoserver
%define realname geoserver
%define mapstory_ver 0.0
%define version 2.8
%define release 2.1%{?dist}
%define _unpackaged_files_terminate_build 0
%define __os_install_post %{nil}
%define _rpmfilename %%{NAME}-%%{VERSION}-%%{RELEASE}.%%{ARCH}.rpm

Name:          %{name}
Version:       %{version}
Release:       %{release}
Summary:       A version of GeoServer that is enhanced and designed for use with MapStory %{mapstory_ver}.
Group:         Development/Libraries
License:       GPLv2
BuildRequires: unzip
Requires:      %{name} = %{version}-%{release}
Requires:      tomcat8
Conflicts:     geoserver
Source0:       geoserver-mapstory-2.8.war
Source1:       geowebcache.xml
Source2:       geogig.zip
Source3:       mapstory_data.zip
Source4:       rest.properties
Patch0:        web.xml.patch
Patch1:        context.xml.patch
BuildArch:     noarch

%description
GeoServer is built with the geoserver-geonode-ext, which extends GeoServer
with certain JSON, REST, and security capabilites specifically for MapStory.

%prep
[ -d $RPM_SOURCE_DIR/geoserver ] && rm -rf $RPM_SOURCE_DIR/geoserver
unzip $RPM_SOURCE_DIR/%{realname}-mapstory-%{version}.war -d $RPM_SOURCE_DIR/geoserver
pushd $RPM_SOURCE_DIR/geoserver

%patch0 -p1
%patch1 -p1

popd

%build

%install
WEBAPPS=$RPM_BUILD_ROOT%{_localstatedir}/lib/tomcat8/webapps
GS=$RPM_SOURCE_DIR/geoserver
DATA=$RPM_BUILD_ROOT%{_localstatedir}/lib/geoserver_data
GEOSERVER_DATA=$RPM_SOURCE_DIR/geoserver/data
mkdir -p $WEBAPPS
cp -rp $GS $WEBAPPS
if [ ! -d $DATA ]; then
  mkdir -p $DATA
  cp -R $GEOSERVER_DATA/* $DATA
fi
sed -i.bak "s|http://localhost|https://localhost|g" $DATA/security/auth/geonodeAuthProvider/config.xml
mkdir -p $DATA/gwc
install -m 755 %{SOURCE1} $DATA/gwc/geowebcache.xml
unzip -d $DATA %{SOURCE2}
unzip -d $DATA/workspaces/geonode %{SOURCE3}
install -m 755 %{SOURCE4} $DATA/security

%pre

%post
if [ $1 -eq 1 ] ; then
  # add Java specific options
  echo '# Next line added for geonode service' >> %{_sysconfdir}/sysconfig/tomcat8
  echo 'JAVA_OPTS="-Djava.awt.headless=true -Xms256m -Xmx1024m -Xrs -XX:PerfDataSamplingInterval=500 -XX:+UseParNewGC -XX:+UseConcMarkSweepGC -XX:SoftRefLRUPolicyMSPerMB=36000 -Duser.home=/var/lib/geoserver_data/geogig"' >> %{_sysconfdir}/sysconfig/tomcat8
fi

%preun
if [ $1 -eq 0 ] ; then
  /sbin/service tomcat8 stop > /dev/null 2>&1
  rm -fr %{_localstatedir}/lib/tomcat8/webapps/geoserver
fi

%postun
if [ $1 -eq 1 ] ; then
  /sbin/service tomcat8 condrestart >/dev/null 2>&1
fi

%clean
[ ${RPM_BUILD_ROOT} != "/" ] && rm -rf ${RPM_BUILD_ROOT}
[ -d $RPM_SOURCE_DIR/geoserver ] && rm -rf $RPM_SOURCE_DIR/geoserver

%files
%defattr(-,root,root,-)
%attr(-,tomcat,tomcat) %{_localstatedir}/lib/tomcat8/webapps/geoserver
%attr(775,tomcat,tomcat) %{_localstatedir}/lib/geoserver_data

%changelog

