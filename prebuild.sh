#!/bin/bash -xe

case "$DIST" in
    el6)
        # EPEL6: libnet
        build_dl https://archives.fedoraproject.org/pub/archive/epel/6/x86_64/epel-release-6-8.noarch.rpm
        rpm -Uvh "$CACHEDIR/epel-release-6-8.noarch.rpm"
        # el6 EOL, use archive repositories
        sed -i -re 's,mirror\.centos\.org,vault.centos.org,; s,^(mirrorlist),#\1,; s,^#(baseurl),\1,' \
            /etc/yum.repos.d/CentOS-Base.repo
        ;;
esac
