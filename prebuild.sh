#!/bin/bash -xe

case "$DIST" in
    el6)
        # EPEL6: libnet
        build_dl "https://dl.fedoraproject.org/pub/epel/epel-release-latest-$DIST_VERSION.noarch.rpm"
        rpm -Uvh "$CACHEDIR/epel-release-latest-$DIST_VERSION.noarch.rpm"
        ;;
esac
