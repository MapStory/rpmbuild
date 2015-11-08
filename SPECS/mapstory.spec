# Define Constants
%define name mapstory
%define version 1.0
%define release 0.1.beta%{?dist}
%define _unpackaged_files_terminate_build 0
%define __os_install_post %{nil}

Name:             %{name}
Version:          %{version}
Release:          %{release}
Summary:          MapStory is an online social cartographic platform.
Group:            Applications/Engineering
License:          GPLv2
Source0:          mapstory
Source1:          mapstory.requirements.txt
Source2:          mapstory.supervisord.conf
Source3:          mapstory.init
Source4:          mapstory.mapstory.conf
Source5:          mapstory.proxy.conf
Source6:          mapstory.README
Source7:          mapstory.local_settings.py
Source8:          mapstory.local_key.py
Source9:          mapstory.robots.txt
Packager:         Daniel Berry <dberry@boundlessgeo.com>
Requires(pre):    /usr/sbin/useradd
Requires(pre):    /usr/bin/getent
Requires(pre):    bash
Requires(postun): /usr/sbin/userdel
Requires(postun): bash
BuildRequires:    python27
BuildRequires:    python27-virtualenv
BuildRequires:    gdal-devel = 1.11.2
BuildRequires:    proj-devel
BuildRequires:    postgresql93-devel
BuildRequires:    libxslt-devel
BuildRequires:    pcre-devel
BuildRequires:    gcc
BuildRequires:    gcc-c++
BuildRequires:    git
BuildRequires:    nodejs
Requires:         python27
Requires:         python27-virtualenv
Requires:         gdal = 1.11.2
Requires:         postgresql93
Requires:         postgresql93-server
Requires:         postgis21-postgresql93
Requires:         proj
Requires:         httpd
Requires:         libxslt
Requires:         %{name}-geoserver >= %{version}-%{release}
AutoReqProv:      no
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
The MapStory platform is an online cartographic application developed using the GeoNode open-source platform. GeoNode is a spatial data infrastructure solution that extends the OpenGeo Architecture with several advanced features such as participatory or collaborative mapping, advanced customization, social network capabilities and metadata catalog solutions.

%package geoserver
Summary:       A version of GeoServer that is enhanced and designed for use with MapStory %{version}.
Group:         Development/Libraries
BuildRequires: unzip
Requires:      %{name} = %{version}-%{release}
Requires:      tomcat
Requires:      java-1.7.0-openjdk
Conflicts:     geoserver
Patch0:        mapstory.web.xml.patch
Patch1:        mapstory.context.xml.patch
BuildArch:     noarch

%description geoserver
GeoServer is built with the geoserver-geonode-ext, which extends GeoServer
with certain JSON, REST, and security capabilites specifically for MapStory %{version}-%{release}.

%prep
unzip $RPM_SOURCE_DIR/geoserver.war -d $RPM_SOURCE_DIR/geoserver
pushd $RPM_SOURCE_DIR/geoserver

%patch0 -p1
%patch1 -p1

popd

%build

%install
MAPSTORY_LIB=$RPM_BUILD_ROOT%{_localstatedir}/lib/%{name}
mkdir -p $MAPSTORY_LIB/media
cp -rp $RPM_SOURCE_DIR/%{name}/*  $MAPSTORY_LIB
pushd $MAPSTORY_LIB

# create virtualenv
virtualenv-2.7 .venv
export PATH=/usr/pgsql-9.3/bin:$PATH
source .venv/bin/activate
install -m 755 %{SOURCE1} ./requirements.txt

# install python dependencies
pip install --no-index --find-links=pkgs -r requirements.txt
rm -fr pkgs
rm -f requirements.txt
popd

# compile geonode static files
pushd $MAPSTORY_LIB/geonode/geonode/static
npm install
bower install --noinput --config.interactive=false
grunt copy
popd

# compile mapstory static files
pushd $MAPSTORY_LIB/%{name}-geonode/%{name}/static
npm install
bower install --noinput --config.interactive=false
grunt less
popd

# setup supervisord configuration
SUPV_ETC=$RPM_BUILD_ROOT%{_sysconfdir}
mkdir -p $SUPV_ETC
install -m 644 %{SOURCE2} $SUPV_ETC/supervisord.conf
MAPSTORY_LOG=$RPM_BUILD_ROOT%{_localstatedir}/log/%{name}
mkdir -p $MAPSTORY_LOG

# setup init script
INITD=$RPM_BUILD_ROOT%{_sysconfdir}/init.d
mkdir -p $INITD
install -m 751 %{SOURCE3} $INITD/%{name}

# setup httpd configuration
HTTPD_CONFD=$RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d
mkdir -p $HTTPD_CONFD
install -m 644 %{SOURCE4} $HTTPD_CONFD/%{name}.conf
install -m 644 %{SOURCE5} $HTTPD_CONFD/proxy.conf

# adjust virtualenv to /var/lib/geonode path
VAR0=$RPM_BUILD_ROOT%{_localstatedir}/lib/%{name}
VAR1=%{_localstatedir}/lib/%{name}
find $VAR0 -type f -name '*pyc' -exec rm {} +
grep -rl $VAR0 $VAR0 | xargs sed -i 's|'$VAR0'|'$VAR1'|g'

# setup mapstory configuration directory
MAPSTORY_CONF=$RPM_BUILD_ROOT%{_sysconfdir}/%{name}
mkdir -p $MAPSTORY_CONF
install -m 755 %{SOURCE6} $MAPSTORY_CONF/README

# additions to mapstory directory
# local_settings.py
install -m 755 %{SOURCE7} $MAPSTORY_LIB/%{name}-geonode/%{name}/settings/local_settings.py
# local_key.py
install -m 755 %{SOURCE8} $MAPSTORY_LIB/%{name}-geonode/%{name}/settings/local_key.py
# robots.txt
install -m 755 %{SOURCE9} $MAPSTORY_LIB/%{name}-geonode/%{name}/templates/robots.txt
# add robots.txt as a TemplateView in django original file is urls.py.bak
sed -i.bak "s|urlpatterns = patterns('',|urlpatterns = patterns('',\\n\
url(r'^/robots\\\.txt$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),|" $RPM_BUILD_ROOT%{_localstatedir}/lib/%{name}/%{name}-geonode/%{name}/urls.py

# setup envionment for mapstory user
echo "export PYTHONPATH=/var/lib/%{name}/.venv:/var/lib/%{name}/.venv/lib/python2.7/site-packages" >> $MAPSTORY_LIB/.bash_profile
echo "alias python='/var/lib/%{name}/.venv/bin/python'" >> $MAPSTORY_LIB/.bash_profile
echo "alias pip='python /var/lib/%{name}/.venv/bin/pip'" >> $MAPSTORY_LIB/.bash_profile
echo "alias activate='source /var/lib/%{name}/.venv/bin/activate'" >> $MAPSTORY_LIB/.bash_profile
echo "alias collectstatic='python /var/lib/%{name}/%{name}-geonode/manage.py collectstatic'" >> $MAPSTORY_LIB/.bash_profile
echo "alias syncdb='python /var/lib/%{name}/%{name}-geonode/manage.py syncdb'" >> $MAPSTORY_LIB/.bash_profile
echo "alias createsuperuser='python /var/lib/%{name}/%{name}-geonode/manage.py createsuperuser'" >> $MAPSTORY_LIB/.bash_profile

# GeoServer Install
CX_ROOT=$RPM_BUILD_ROOT%{_sysconfdir}/tomcat/Catalina/localhost
WEBAPPS=$RPM_BUILD_ROOT%{_localstatedir}/lib/tomcat/webapps
GS=$RPM_SOURCE_DIR/geoserver
DATA=$RPM_BUILD_ROOT%{_localstatedir}/lib/geoserver
WAR_DATA=$RPM_BUILD_ROOT%{_localstatedir}/lib/tomcat/webapps/geoserver/data
CX=$RPM_SOURCE_DIR/geoserver/WEB-INF/classes/org/geonode/security/geoserver.xml
SQL=$RPM_SOURCE_DIR/geoserver/WEB-INF/classes/org/geonode/security/geonode_authorize_layer.sql
mkdir -p $CX_ROOT $WEBAPPS
cp -rp $CX $CX_ROOT
cp -rp $GS $WEBAPPS
if [ ! -d $DATA ]; then
  mkdir -p $DATA
  cp -R $WAR_DATA/* $DATA
fi
cp -rp $SQL $DATA
rm -fr $GS

%pre
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || useradd -r -d %{_localstatedir}/lib/%{name} -g %{name} -s /bin/bash -c "MapStory Daemon User" %{name}

%post
if [ $1 -eq 1 ] ; then
  /sbin/chkconfig --add %{name}
  ln -s %{_localstatedir}/lib/%{name}/%{name}-geonode/%{name}/settings/local_settings.py %{_sysconfdir}/%{name}/local_settings.py
  echo ""
  echo " MapStory Version - %{version}-%{release}"
  echo ""
  echo "     -------------------------------     "
  echo "              Important!!!               "
  echo "                                         "
  echo "     Reference /etc/mapstory/README      "
  echo "         for post configuration          "
  echo "     -------------------------------     "
  echo ""
  echo ""
fi

%post geoserver
if [ $1 -eq 1 ] ; then
  # add Java specific options
  echo '# Next line added for mapstory service' >> %{_sysconfdir}/tomcat/tomcat.conf
  echo 'JAVA_OPTS="-Xmx1024m -XX:MaxPermSize=256m"' >> %{_sysconfdir}/tomcat/tomcat.conf
fi

%preun
if [ $1 -eq 0 ] ; then
  /sbin/service %{name} stop > /dev/null 2>&1
  /sbin/service httpd stop > /dev/null 2>&1
  /sbin/chkconfig --del %{name}
  rm -fr %{_localstatedir}/lib/%{name}
  rm -fr %{_sysconfdir}/%{name}
  rm -f %{_sysconfdir}/init.d/%{name}
  rm -f %{_sysconfdir}/supervisord.conf
  rm -f %{_sysconfdir}/httpd/conf.d/%{name}.conf
  rm -f %{_sysconfdir}/httpd/conf.d/proxy.conf
fi

%preun geoserver
if [ $1 -eq 0 ] ; then
  /sbin/service tomcat stop > /dev/null 2>&1
  rm -fr %{_localstatedir}/lib/tomcat/webapps/geoserver
  rm -f %{_sysconfdir}/tomcat/Catalina/localhost/geoserver.xml
  echo ""
  echo ""
  echo "  -------------------------------"
  echo "           Important!!!          "
  echo "                                 "
  echo "     Uninstall does not delete   "
  echo "   files from /var/lib/geoserver "
  echo "  -------------------------------"
  echo ""
  echo ""
fi

%postun

%postun geoserver
if [ $1 -eq 1 ] ; then
  /sbin/service tomcat condrestart >/dev/null 2>&1
fi

%clean
[ ${RPM_BUILD_ROOT} != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(755,%{name},%{name},-)
%{_localstatedir}/lib/%{name}/
%config(noreplace) %{_localstatedir}/lib/%{name}/%{name}-geonode/%{name}/settings/local_settings.py
%defattr(775,%{name},%{name},-)
%{_localstatedir}/lib/%{name}/media
%defattr(744,%{name},%{name},-)
%{_localstatedir}/log/%{name}/
%defattr(644,%{name},%{name},-)
%dir %{_sysconfdir}/%{name}/
%{_sysconfdir}/%{name}/README
%defattr(644,apache,apache,-)
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%config(noreplace) %{_sysconfdir}/httpd/conf.d/proxy.conf
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/supervisord.conf
%defattr(-,root,root,-)
%config %{_sysconfdir}/init.d/%{name}

%files geoserver
%defattr(-,root,root,-)
%attr(-,tomcat,tomcat) %{_localstatedir}/lib/tomcat/webapps/geoserver
%attr(-,tomcat,tomcat) %{_localstatedir}/lib/geoserver
%dir %{_sysconfdir}/tomcat/Catalina/localhost
%attr(-,tomcat,tomcat) %{_sysconfdir}/tomcat/Catalina/localhost/geoserver.xml
%doc ../SOURCES/license/geoserver/GPL
%doc ../SOURCES/license/GNU

%changelog
* Thu Nov 5 2015 Daniel Berry <dberry@boundlessgeo.com> 1.0-0.1.beta
- add comments

