#!/bin/bash

VERSION=`cat version.py | grep __version__ | awk '{print $3}' | sed "s/'//g"`

docker pull dockerregistry.tagged.com/siteops/centos:6.5
docker build -t tagopsdb-centos-65 -f Dockerfile.centos65 .
docker run --name=tagopsdb-centos-65 tagopsdb-centos-65 ./.jenkins/scripts/rpm-package.sh
docker cp tagopsdb-centos-65:/opt/tagopsdb/python27-tagopsdb-$VERSION-1.tagged.el6.noarch.rpm .
docker rm tagopsdb-centos-65
docker rmi tagopsdb-centos-65

docker pull dockerregistry.tagged.com/siteops/centos:7.1
docker build -t tagopsdb-centos-71 -f Dockerfile.centos71 .
docker run --name=tagopsdb-centos-71 tagopsdb-centos-71 ./.jenkins/scripts/rpm-package.sh
docker cp tagopsdb-centos-71:/opt/tagopsdb/python-tagopsdb-$VERSION-1.tagged.el7.noarch.rpm .
docker rm tagopsdb-centos-71
docker rmi tagopsdb-centos-71
