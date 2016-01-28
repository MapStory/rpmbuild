#!/usr/bin/env bash
pushd /etc/yum.repos.d
wget http://yum.boundlessps.com/geoshape.repo
popd
sudo yum -y update
sudo yum -y install rpmdevtools zip python27-devel python27-virtualenv gcc gcc-c++ make expat-devel db4-devel gdbm-devel sqlite-devel readline-devel zlib-devel bzip2-devel openssl-devel tk-devel gdal-devel libxslt-devel libxml2-devel libjpeg-turbo-devel zlib-devel libtiff-devel freetype-devel lcms2-devel proj-devel geos-devel postgresql95-devel unzip git
sudo yum -y install http://dl.fedoraproject.org/pub/epel/epel-release-latest-6.noarch.rpm
sudo yum -y install nodejs npm
sudo npm install -g grunt bower grunt-cli