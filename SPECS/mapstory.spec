# GitHub Short Commit Hash for mapstory-geonode and geonode clone
%define mapstory_commit fdac304
# https://github.com/MapStory/mapstory-geonode.git

%define geonode_commit 24f5b40
# https://github.com/MapStory/geonode

# Define Constants
%define name mapstory
%define version 0.0
%define release 4.%{mapstory_commit}.%{geonode_commit}%{?dist}
%define _unpackaged_files_terminate_build 0
%define __os_install_post %{nil}
%define _rpmfilename %%{NAME}-%%{VERSION}-%%{RELEASE}.%%{ARCH}.rpm

Name:             %{name}
Version:          %{version}
Release:          %{release}
Summary:          MapStory is an online social cartographic platform.
Group:            Applications/Engineering
License:          CC BY-SA 2.0 and ODbL
Packager:         Daniel Berry <dberry@boundlessgeo.com>
Source0:          admin.json
Source1:          fixture_mapstory.json
Source2:          geogig-cli-app-1.0.zip
Source3:          local_settings.py
Source4:          mapstory-config
Source5:          mapstory-config.conf
Source6:          mapstory.conf
Source7:          mapstory-django
Source8:          mapstory.init
Source9:          parallax.zip
Source10:         proxy.conf
Source11:         requirements.txt
Source12:         supervisord.conf
Source13:         geonode_authorize_layer.sql
Source14:         gunicorn-app.sh
Requires(pre):    /usr/sbin/useradd
Requires(pre):    /usr/bin/getent
Requires(pre):    bash
Requires(postun): /usr/sbin/userdel
Requires(postun): bash
BuildRequires:    python27-devel
BuildRequires:    python27-virtualenv
BuildRequires:    gcc
BuildRequires:    gcc-c++
BuildRequires:    make
BuildRequires:    expat-devel
BuildRequires:    db4-devel
BuildRequires:    gdbm-devel
BuildRequires:    sqlite-devel
BuildRequires:    readline-devel
BuildRequires:    zlib-devel
BuildRequires:    bzip2-devel
BuildRequires:    openssl-devel
BuildRequires:    tk-devel
BuildRequires:    gdal-devel = 2.0.1
BuildRequires:    libxslt-devel
BuildRequires:    libxml2-devel
BuildRequires:    libjpeg-turbo-devel
BuildRequires:    zlib-devel
BuildRequires:    libtiff-devel
BuildRequires:    freetype-devel
BuildRequires:    lcms2-devel
BuildRequires:    proj-devel
BuildRequires:    geos-devel
BuildRequires:    postgresql95-devel
BuildRequires:    unzip
BuildRequires:    git
BuildRequires:    nodejs
BuildRequires:    npm
Requires:         python27
Requires:         python27-virtualenv
Requires:         gdal = 2.0.1
Requires:         postgresql95
Requires:         postgresql95-server
Requires:         postgis-postgresql95 >= 2.2
Requires:         postgresql95-contrib
Requires:         httpd
Requires:         mod_ssl
Requires:         mod_xsendfile
Requires:         libxslt
Requires:         libxml2
Requires:         libjpeg-turbo
Requires:         zlib
Requires:         libtiff
Requires:         freetype
Requires:         lcms2
Requires:         proj
Requires:         geos
Requires:         mapstory-geoserver >= 2.8
Requires:         rabbitmq-server >= 3.5.6
Requires:         erlang >= 18.1
Requires:         elasticsearch >= 1.6.0
AutoReqProv:      no

%description
MapStory is an online social cartographic platform.

%prep

%build

%install
# rogue and geonode
GEONODE_LIB=$RPM_BUILD_ROOT%{_localstatedir}/lib/geonode
mkdir -p $GEONODE_LIB/{gunicorn/{static,media/thumbs},scripts}
pushd $GEONODE_LIB

# setup git archives
mkdir -p $GEONODE_LIB/git
cd git
git clone https://github.com/MapStory/mapstory-geonode.git
git clone https://github.com/MapStory/geonode.git
cd mapstory-geonode
git archive --format=tar --prefix=mapstory-geonode/ %{mapstory_commit} | (cd $GEONODE_LIB && tar xf -)
cd ../geonode
git archive --format=tar --prefix=geonode/ %{geonode_commit} | (cd $GEONODE_LIB && tar xf -)
cd ../../
rm -fr git

# add static images
unzip %{SOURCE9} -d $GEONODE_LIB/gunicorn/media

# create virtualenv
/usr/local/bin/virtualenv .
export PATH=/usr/pgsql-9.5/bin:$PATH
source bin/activate
pip install --upgrade pip

# install pip dependencies
install -m 755 %{SOURCE11} $GEONODE_LIB
pip install -r requirements.txt
rm -f $GEONODE_LIB/requirements.txt

#install mapstory-geonode and geonode dependencies
cd mapstory-geonode
pip install -r requirements.txt
cd mapstory/static
npm set progress=false
npm install
bower install --noinput --config.interactive=false
grunt less
[ -f find-node-or-install ] && rm -f find-node-or-install
[ -f makefile ] && rm -f makefile
[ -d .components ] && rm -fr .components
[ -d node_modules ] && rm -fr node_modules
cd ../../../geonode/geonode/static
npm set progress=false
npm install
bower install --noinput --config.interactive=false
grunt copy
[ -f find-node-or-install ] && rm -f find-node-or-install
[ -f makefile ] && rm -f makefile
[ -d .components ] && rm -fr .components
[ -d node_modules ] && rm -fr node_modules
cd ../../
python setup.py install
popd

# install wrapper and sql scripts
install -m 650 %{SOURCE14} $GEONODE_LIB/scripts
install -m 755 %{SOURCE13} $GEONODE_LIB/scripts

# setup supervisord configuration
SUPV_ETC=$RPM_BUILD_ROOT%{_sysconfdir}
mkdir -p $SUPV_ETC
install -m 644 %{SOURCE12} $SUPV_ETC/supervisord.conf
MAPSTORY_LOG=$RPM_BUILD_ROOT%{_localstatedir}/log/%{name}
mkdir -p $MAPSTORY_LOG
CELERY_LOG=$RPM_BUILD_ROOT%{_localstatedir}/log/celery
mkdir -p $CELERY_LOG
# setup init script
INITD=$RPM_BUILD_ROOT%{_sysconfdir}/init.d
mkdir -p $INITD
install -m 751 %{SOURCE8} $INITD/%{name}

# setup httpd configuration
HTTPD_CONFD=$RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d
mkdir -p $HTTPD_CONFD
install -m 644 %{SOURCE6} $HTTPD_CONFD/%{name}.conf
install -m 644 %{SOURCE10} $HTTPD_CONFD/proxy.conf

# adjust virtualenv to /var/lib/geonode path
VAR0=$RPM_BUILD_ROOT%{_localstatedir}/lib/geonode
VAR1=%{_localstatedir}/lib/geonode
find $VAR0 -type f -name '*pyc' -exec rm {} +
grep -rl $VAR0 $VAR0 | xargs sed -i 's|'$VAR0'|'$VAR1'|g'

# setup mapstory configuration directory
MAPSTORY_CONF=$RPM_BUILD_ROOT%{_sysconfdir}/%{name}
mkdir -p $MAPSTORY_CONF
# local_settings.py
install -m 775 %{SOURCE3} $MAPSTORY_CONF/local_settings.py

# Add Content Security Policy to sit_base.html to allow http tiles (MapBox) to be used with https
sed -i.bak "s|{% block head %}|{% block head %}\\n\
<meta http-equiv="Content-Security-Policy" content="upgrade-insecure-requests">|" $RPM_BUILD_ROOT%{_localstatedir}/lib/geonode/mapstory-geonode/mapstory/templates/site_base.html

# Adjust get-involved image with a world.png
sed -i.bak "s|{% remote_content 'static_img/get-involved-cropped.jpg' %}|{{ STATIC_URL }}mapstory/img/world.png|" $RPM_BUILD_ROOT%{_localstatedir}/lib/geonode/mapstory-geonode/mapstory/templates/index.html

# mapstory-config command and conf file
USER_BIN=$RPM_BUILD_ROOT%{_prefix}/bin
mkdir -p $USER_BIN
install -m 755 %{SOURCE4} $USER_BIN/
install -m 755 %{SOURCE7} $USER_BIN/
install -m 755 %{SOURCE5} $MAPSTORY_CONF/

# geogig-cli
unzip -d $RPM_BUILD_ROOT%{_localstatedir}/lib %{SOURCE2}
PROFILE_D=$RPM_BUILD_ROOT%{_sysconfdir}/profile.d
mkdir -p $PROFILE_D
find $RPM_BUILD_ROOT%{_localstatedir}/lib/geogig -type f -name '*bat' -exec rm {} +
echo  'export GEOGIG_HOME="/var/lib/geogig" && PATH="$PATH:$GEOGIG_HOME/bin"' > $PROFILE_D/geogig.sh

# django fixtures
install -m 755 %{SOURCE0} $MAPSTORY_CONF/
install -m 755 %{SOURCE1} $MAPSTORY_CONF/

%pre
getent group geoservice >/dev/null || groupadd -r geoservice
usermod -a -G geoservice tomcat
usermod -a -G geoservice apache
getent passwd %{name} >/dev/null || useradd -r -d %{_localstatedir}/lib/geonode/mapstory-geonode -g geoservice -s /bin/bash -c "MapStory Daemon User" %{name}

%post
if [ $1 -eq 1 ] ; then
  ln -s %{_sysconfdir}/%{name}/local_settings.py %{_localstatedir}/lib/geonode/mapstory-geonode/%{name}/settings/local_settings.py
  source %{_sysconfdir}/profile.d/geogig.sh
  chgrp -hR geoservice /var/lib/geoserver_data
  chmod -R 775 /var/lib/geoserver_data
fi

%preun
find %{_localstatedir}/lib/geonode -type f -name '*pyc' -exec rm {} +
if [ $1 -eq 0 ] ; then
  /sbin/service tomcat8 stop > /dev/null 2>&1
  /sbin/service %{name} stop > /dev/null 2>&1
  /sbin/service httpd stop > /dev/null 2>&1
  /sbin/chkconfig --del %{name}
  #remove soft link and virtual environment
  rm -fr %{_localstatedir}/lib/geonode/mapstory-geonode/%{name}/settings/local_settings.py
fi

%postun

%clean
[ ${RPM_BUILD_ROOT} != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(755,%{name},geoservice,755)
%{_localstatedir}/lib/geogig
%{_sysconfdir}/profile.d/geogig.sh
%{_localstatedir}/lib/geonode
%config(noreplace) %{_sysconfdir}/%{name}/local_settings.py
%{_sysconfdir}/%{name}/admin.json
%{_sysconfdir}/%{name}/fixture_mapstory.json
%{_sysconfdir}/%{name}/%{name}-config.conf
%defattr(775,%{name},geoservice,775)
%dir %{_localstatedir}/lib/geonode/gunicorn/static
%dir %{_localstatedir}/lib/geonode/gunicorn/media
%defattr(744,%{name},geoservice,744)
%dir %{_localstatedir}/log/celery
%dir %{_localstatedir}/log/%{name}
%dir %{_sysconfdir}/%{name}/
%defattr(644,apache,apache,644)
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%config(noreplace) %{_sysconfdir}/httpd/conf.d/proxy.conf
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/supervisord.conf
%defattr(-,root,root,-)
%config %{_sysconfdir}/init.d/%{name}
%{_prefix}/bin/%{name}-config
%{_prefix}/bin/%{name}-django

%changelog
* Fri Jan 22 2016 BerryDaniel <dberry@boundlessgeo.com> [0.0-1]
- Updated to 0.0
