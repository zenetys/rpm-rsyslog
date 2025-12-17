#
# License: MIT
# Author: Benoit DOLEZ <bdolez@zenetys.com>
# Copyright: 2019
#

# Supported targets: el8, el9
# Replace distro package with: dnf install rsyslog8z --allowerasing
#
# This package is not compatible with standard rsyslog packages from the
# distro nor adiscon repo. It is an alternative, mostly for liblognorm
# patches not merged upstream. Conflicts lines will handle standard redhat
# packages found in el8, el9, el10s, and packages names found in adiscon
# repo, as well as rsyslog-imhttp built in neither.

%global __requires_exclude_from ^%{_bindir}/rsyslog-recover-qi\\.pl$

%define libestr                 libestr-0.1.11
%define liblognorm              liblognorm-2.0.9
%define liblogging              liblogging-1.0.8
%define libfastjson             libfastjson-1.2304.0
%define librelp                 librelp-1.12.0
%define libmaxminddb_version    1.12.2
%define libmaxminddb            libmaxminddb-%{libmaxminddb_version}
%define civetweb_version        1.16
%define civetweb                civetweb-%{civetweb_version}
%define builddir                %{_builddir}/%{name}-%{version}
%define static_only             --enable-static --disable-shared

Summary: Rsyslog v8 package by Zenetys
Name: rsyslog8z
Version: 8.2512.0
Release: 4%{?dist}.zenetys
License: GPLv3+ and ASL 2.0
Group: System Environment/Daemons

Source0: http://www.rsyslog.com/files/download/rsyslog/rsyslog-%{version}.tar.gz
Source10: rsyslog.conf
Source11: rsyslog.sysconfig
Source12: rsyslog.logrotate.systemd
Source15: rsyslog.service
Source300: http://libestr.adiscon.com/files/download/%{libestr}.tar.gz
Source301: http://www.liblognorm.com/files/download/%{liblognorm}.tar.gz
Source302: http://download.rsyslog.com/liblogging/%{liblogging}.tar.gz
Source303: http://download.rsyslog.com/libfastjson/%{libfastjson}.tar.gz
Source304: http://download.rsyslog.com/librelp/%{librelp}.tar.gz
Source402: https://github.com/maxmind/libmaxminddb/releases/download/%{libmaxminddb_version}/%{libmaxminddb}.tar.gz
Source403: https://github.com/civetweb/civetweb/archive/refs/tags/v%{civetweb_version}.tar.gz#/%{civetweb}.tar.gz

Patch100: rsyslog-8.2508.0-fmpcre-build.patch
Patch101: rsyslog-8.2512.0-include-libfastjson.patch

URL: http://www.rsyslog.com/
Vendor: Adiscon GmbH, Deutschland
Packager: Benoit DOLEZ <bdolez@zenetys.com>

BuildRequires: apr-util-devel
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: bison
BuildRequires: gcc
BuildRequires: flex
BuildRequires: gnutls-devel
BuildRequires: libgcrypt-devel
BuildRequires: libnet-devel
BuildRequires: libtool
BuildRequires: libuuid-devel
BuildRequires: make
BuildRequires: net-snmp-devel
BuildRequires: openssl-devel
BuildRequires: pcre-devel
BuildRequires: pkgconfig
BuildRequires: pkgconfig(libcurl)
BuildRequires: pkgconfig(libzstd)
BuildRequires: zlib-devel

BuildRequires: systemd-devel >= 219-39
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

Requires: bash >= 2.0
Requires: logrotate >= 3.5.2

Provides: rsyslog
Conflicts: rsyslog
Provides: rsyslog-crypto
Conflicts: rsyslog-crypto
Provides: rsyslog-elasticsearch
Conflicts: rsyslog-elasticsearch
Provides: rsyslog-fmhash
Conflicts: rsyslog-fmhash
Provides: rsyslog-fmhttp
Conflicts: rsyslog-fmhttp
Provides: rsyslog-gnutls
Conflicts: rsyslog-gnutls
#Provides: rsyslog-gssapi
Conflicts: rsyslog-gssapi
#Provides: rsyslog-hiredis
Conflicts: rsyslog-hiredis
Provides: rsyslog-imhttp
Conflicts: rsyslog-imhttp
#Provides: rsyslog-kafka
Conflicts: rsyslog-kafka
#Provides: rsyslog-libdbi
Conflicts: rsyslog-libdbi
Provides: rsyslog-logrotate
Conflicts: rsyslog-logrotate
Provides: rsyslog-mmaudit
Conflicts: rsyslog-mmaudit
Provides: rsyslog-mmfields
Conflicts: rsyslog-mmfields
Provides: rsyslog-mmjsonparse
Conflicts: rsyslog-mmjsonparse
Provides: rsyslog-mmjsontransform
Conflicts: rsyslog-mmjsontransform
Provides: rsyslog-mmkubernetes
Conflicts: rsyslog-mmkubernetes
Provides: rsyslog-mmleefparse
Conflicts: rsyslog-mmleefparse
Provides: rsyslog-mmnormalize
Conflicts: rsyslog-mmnormalize
Provides: rsyslog-mmrm1stspace
Conflicts: rsyslog-mmrm1stspace
Provides: rsyslog-mmsnareparse
Conflicts: rsyslog-mmsnareparse
Provides: rsyslog-mmsnmptrapd
Conflicts: rsyslog-mmsnmptrapd
Provides: rsyslog-mmtaghostname
Conflicts: rsyslog-mmtaghostname
#Provides: rsyslog-mongodb
Conflicts: rsyslog-mongodb
#Provides: rsyslog-omamqp1
Conflicts: rsyslog-omamqp1
#Provides: rsyslog-omazureeventhubs
Conflicts: rsyslog-omazureeventhubs
Provides: rsyslog-omhttp
Conflicts: rsyslog-omhttp
Provides: rsyslog-openssl
Conflicts: rsyslog-openssl
#Provides: rsyslog-pgsql
Conflicts: rsyslog-pgsql
Provides: rsyslog-pmciscoios
Conflicts: rsyslog-pmciscoios
Provides: rsyslog-pmnormalize
Conflicts: rsyslog-pmnormalize
#Provides: rsyslog-rabbitmq
Conflicts: rsyslog-rabbitmq
Provides: rsyslog-relp
Conflicts: rsyslog-relp
Provides: rsyslog-snmp
Conflicts: rsyslog-snmp
Provides: rsyslog-udpspoof
Conflicts: rsyslog-udpspoof

Provides: syslog
Obsoletes: sysklogd < 1.5-11

%description
Rsyslog is an enhanced, multi-threaded syslog daemon.

%package mysql
Summary: MySQL support for rsyslog
Group: System Environment/Daemons
Requires: %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
# mysql_config is required by rsyslog configure script
# on el8, mariadb-connector-c-devel contains mysql_config;
# dependencies install libs and headers; mysql is still available
# via stream but mariadb should be preferred.
BuildRequires: mariadb-connector-c-devel

Provides: rsyslog-mysql
Conflicts: rsyslog-mysql

%description mysql
The rsyslog-mysql package contains a dynamic shared object that will add
MySQL database support to rsyslog.

%prep
%setup -c %{name}-%{version}
%setup -T -D -a 300
%setup -T -D -a 301
%setup -T -D -a 302
%setup -T -D -a 303
%setup -T -D -a 304
%setup -T -D -a 402
%setup -T -D -a 403

cd rsyslog-%{version}
# rsyslog patches
%patch100 -p1
%patch101 -p1
cd ..

%build
distro_cflags='%{?build_cflags:%{build_cflags}}'
distro_cflags+=' %{!?build_cflags:%{?optflags}}'
distro_ldflags='%{?build_ldflags:%{build_ldflags}}'
distro_ldflags+=' %{!?build_ldflags:%{?__global_ldflags}}'
rsyslog_configure_cflags="$distro_cflags -fPIC -g"
rsyslog_configure_ldflags="$distro_ldflags"
rsyslog_configure_opts=()
rsyslog_make_opts=()
libestr_configure_cflags="$distro_cflags -fPIC -g"
libestr_configure_ldflags="$distro_ldflags"
libfastjson_configure_cflags="$distro_cflags -fPIC -g"
libfastjson_configure_ldflags="$distro_ldflags"
liblognorm_configure_cflags="$distro_cflags -fPIC -g"
liblognorm_configure_ldflags="$distro_ldflags"
liblognorm_configure_opts=()
liblogging_configure_cflags="$distro_cflags -fPIC -g"
liblogging_configure_ldflags="$distro_ldflags"
librelp_configure_cflags="$distro_cflags -fPIC -g"
librelp_configure_ldflags="$distro_ldflags"
libcurl_configure_cflags="$distro_cflags -fPIC -g"
libcurl_configure_ldflags="$distro_ldflags"
libmaxminddb_configure_cflags="$distro_cflags -fPIC -g"
libmaxminddb_configure_ldflags="$distro_ldflags"
civetweb_cflags="$distro_cflags -fPIC -g"
civetweb_ldflags="$distro_ldflags"
civetweb_make_opts=()

# libestr
(
  cd %{libestr}
  %configure %{static_only} \
    ${libestr_configure_cflags:+"CFLAGS=$libestr_configure_cflags"} \
    ${libestr_configure_ldflags:+"LDFLAGS=$libestr_configure_ldflags"}
  make V=1 %{?_smp_mflags}
)
rsyslog_configure_opts+=( LIBESTR_CFLAGS="-I%{builddir}/%{libestr}/include" )
rsyslog_configure_opts+=( LIBESTR_LIBS="-L%{builddir}/%{libestr}/src/.libs -lestr" )
liblognorm_configure_opts+=( LIBESTR_CFLAGS="-I%{builddir}/%{libestr}/include" )
liblognorm_configure_opts+=( LIBESTR_LIBS="-L%{builddir}/%{libestr}/src/.libs -lestr" )

# libfastjson
(
  cd %{libfastjson}
  %configure %{static_only} \
    ${libfastjson_configure_cflags:+"CFLAGS=$libfastjson_configure_cflags"} \
    ${libfastjson_configure_ldflags:+"LDFLAGS=$libfastjson_configure_ldflags"}
  make V=1 %{?_smp_mflags}
)
rsyslog_configure_opts+=( LIBFASTJSON_CFLAGS="-I%{builddir}/%{libfastjson}" )
rsyslog_configure_opts+=( LIBFASTJSON_LIBS="-L%{builddir}/%{libfastjson}/.libs -lfastjson" )
liblognorm_configure_opts+=( LIBFASTJSON_CFLAGS="-I%{builddir}/%{libfastjson}" )
liblognorm_configure_opts+=( LIBFASTJSON_LIBS="-L%{builddir}/%{libfastjson}/.libs -lfastjson" )
# some components may uses JSON_C variables instead
rsyslog_configure_opts+=( JSON_C_CFLAGS="-I%{builddir}/%{libfastjson}" )
rsyslog_configure_opts+=( JSON_C_LIBS="-L%{builddir}/%{libfastjson}/.libs -lfastjson" )
liblognorm_configure_opts+=( JSON_C_CFLAGS="-I%{builddir}/%{libfastjson}" )
liblognorm_configure_opts+=( JSON_C_LIBS="-L%{builddir}/%{libfastjson}/.libs -lfastjson" )

# liblognorm
(
  cd %{liblognorm}
  %configure %{static_only} \
    ${liblognorm_configure_cflags:+"CFLAGS=$liblognorm_configure_cflags"} \
    ${liblognorm_configure_ldflags:+"LDFLAGS=$liblognorm_configure_ldflags"} \
    "${liblognorm_configure_opts[@]}"
  make V=1 %{?_smp_mflags}
)
rsyslog_configure_opts+=( LIBLOGNORM_CFLAGS="-I%{builddir}/%{liblognorm}/src" )
rsyslog_configure_opts+=( LIBLOGNORM_LIBS="-L%{builddir}/%{liblognorm}/src/.libs -llognorm" )

# liblogging-stdlog
(
  cd %{liblogging}
  %configure %{static_only} \
    ${liblogging_configure_cflags:+"CFLAGS=$liblogging_configure_cflags"} \
    ${liblogging_configure_ldflags:+"LDFLAGS=$liblogging_configure_ldflags"}
  make V=1 %{?_smp_mflags}
)
rsyslog_configure_opts+=( LIBLOGGING_STDLOG_CFLAGS="-I%{builddir}/%{liblogging}/stdlog" )
rsyslog_configure_opts+=( LIBLOGGING_STDLOG_LIBS="-L%{builddir}/%{liblogging}/stdlog/.libs -llogging-stdlog" )

# librelp
(
  cd %{librelp}
  %configure %{static_only} \
    ${librelp_configure_cflags:+"CFLAGS=$librelp_configure_cflags"} \
    ${librelp_configure_ldflags:+"LDFLAGS=$librelp_configure_ldflags"}
  make V=1 %{?_smp_mflags}
)
rsyslog_configure_opts+=( RELP_CFLAGS="-I%{builddir}/%{librelp}/src" )
rsyslog_configure_opts+=( RELP_LIBS="-L%{builddir}/%{librelp}/src/.libs -lrelp -lrt -lgnutls -lssl -lcrypto" )

# libmaxminddb
(
  cd %{libmaxminddb}
  %configure %{static_only} \
    ${libmaxminddb_configure_cflags:+"CFLAGS=$libmaxminddb_configure_cflags"} \
    ${libmaxminddb_configure_ldflags:+"LDFLAGS=$libmaxminddb_configure_ldflags"}
  make V=1 %{?_smp_mflags}
)
rsyslog_configure_cflags+=" -I%{builddir}/%{libmaxminddb}/include"
rsyslog_configure_ldflags+=" -L%{builddir}/%{libmaxminddb}/src/.libs"

# civetweb
civetweb_make_opts+=( ${civetweb_cflags:+"WITH_CFLAGS=$civetweb_cflags"} )
civetweb_make_opts+=( ${civetweb_ldflags:+"LDFLAGS=$civetweb_ldflags"} )
civetweb_make_opts+=( COPT='-DNO_SSL_DL' )
(
  cd %{civetweb}
  make lib V=1 %{?_smp_mflags} \
    "${civetweb_make_opts[@]}"
)
rsyslog_configure_cflags+=" -I%{builddir}/%{civetweb}/include"
rsyslog_make_opts+=( CIVETWEB_LIBS="-L%{builddir}/%{civetweb} -lcivetweb -lssl -lcrypto" )

# rsyslog

# apr-util pkgconfig file gives -lldap_r in ldflags, it introduces
# a useless dependency, so force APU_LIBS to overcome that issue
rsyslog_configure_opts+=( APU_LIBS='-laprutil-1' )

OPTIONS=(
  --enable-regexp
  --enable-fmhash
  # --enable-fmhash-xxhash
  --enable-fmunflatten
  --enable-fmpcre
  # --enable-gssapi-krb5
  --enable-klog
  --enable-kmsg
  # --disable-journal-tests
  --enable-inet
  # --enable-jemalloc
  # --enable-unlimited-select
  # --enable-debug
  # --enable-debugless
  # --enable-valgrind
  --enable-diagtools
  --enable-usertools
  --enable-mysql
  # --enable-pgsql
  # --enable-libdbi
  --enable-snmp
  --enable-uuid
  --enable-elasticsearch
  --enable-clickhouse
  --enable-openssl
  --enable-opensslcrypto
  --enable-gnutls
  # --enable-mbedtls
  --enable-libgcrypt
  --enable-libzstd
  --enable-rsyslogrt
  --enable-rsyslogd
  # --enable-extended-tests
  # --enable-mysql-tests
  # --enable-pgsql-tests
  --enable-mail
  --enable-fmhttp

  --enable-mmnormalize
  --enable-mmleefparse
  --enable-mmjsonparse
  --enable-mmjsontransform
  # --enable-mmgrok
  --enable-mmaudit
  --enable-mmanon
  --enable-mmrm1stspace
  --enable-mmutf8fix
  --enable-mmcount
  --enable-mmsequence
  --enable-mmtaghostname
  --enable-mmdblookup
  --enable-mmfields
  --enable-mmpstrucdata
  # --enable-mmaitag
  --enable-mmrfc5424addhmac
  --enable-mmsnareparse
  --enable-mmsnmptrapd
  --enable-mmkubernetes

  --enable-omhttp
  # --enable-omfile-hardened
  --enable-relp
  --enable-omrelp-default-port
  # --enable-ksi-ls12
  --enable-liblogging-stdlog
  # --enable-rfc3195
  # --enable-testbench
  --enable-libfaketime
  # --enable-helgrind
  --enable-imdiag
  --enable-imdocker
  --enable-imdtls
  --enable-imfile
  --enable-imhttp
  --enable-improg
  # --enable-imsolaris
  --enable-imptcp
  --enable-impstats
  # --enable-imtuxedoulog
  --enable-omdtls
  --enable-omprog
  --enable-omstdout
  # --enable-journal-tests
  --enable-pmlastmsg
  # --enable-pmcisconames
  --enable-pmciscoios
  --enable-pmdb2diag
  --enable-pmnull
  --enable-pmnormalize
  --enable-pmaixforwardedfrom
  --enable-pmsnare
  --enable-pmpanngfw
  --enable-omudpspoof
  --enable-omsendertrack
  --enable-omruleset
  --enable-omuxsock
  # --enable-omhdfs
  # --enable-omkafka
  # --enable-imkafka
  # --enable-kafka-tests
  # --enable-kafka-static
  # --enable-ommongodb
  # --enable-imczmq
  # --enable-omczmq
  # --enable-omrabbitmq
  # --enable-omhiredis
  # --enable-omhttpfs
  # --enable-omamqp1
  # --enable-omtcl

  --enable-libsystemd
  --enable-imjournal
  --enable-omjournal
)

(
  cd rsyslog-%{version}
  export > config.exports # save environments vars
  autoreconf -i
  %configure --enable-static=no --enable-shared=yes "${OPTIONS[@]}" \
    ${rsyslog_configure_cflags:+"CFLAGS=$rsyslog_configure_cflags"} \
    ${rsyslog_configure_ldflags:+"LDFLAGS=$rsyslog_configure_ldflags"} \
    "${rsyslog_configure_opts[@]}"
  make V=1 %{?_smp_mflags} \
    pkglibdir=%{_libdir}/rsyslog \
    "${rsyslog_make_opts[@]}"
)

%install
(
  cd %{liblognorm}
  install -d -m 755 %{buildroot}%{_bindir}/
  install -p -m 755 src/lognormalizer %{buildroot}%{_bindir}/
)
(
  cd rsyslog-%{version}
  %make_install pkglibdir=%{_libdir}/rsyslog
)
rm -f %{buildroot}%{_libdir}/rsyslog/*.la

gzip %{buildroot}%{_mandir}/*/*.[0-9]

install -d -m 700 %{buildroot}%{_var}/lib/rsyslog
install -d -m 755 %{buildroot}%{_sysconfdir}/rsyslog.d
install -p -m 644 %{SOURCE10} %{buildroot}%{_sysconfdir}/rsyslog.conf
install -D -p -m 644 %{SOURCE11} %{buildroot}%{_sysconfdir}/sysconfig/rsyslog
sed -i -e 's/^#imjournal# //' %{buildroot}%{_sysconfdir}/rsyslog.conf
sed -i -e '/^#imklog# /d' %{buildroot}%{_sysconfdir}/rsyslog.conf
%if 0%{?rhel} <= 8
install -D -p -m 644 %{SOURCE12} %{buildroot}%{_sysconfdir}/logrotate.d/syslog
%else
install -D -p -m 644 %{SOURCE12} %{buildroot}%{_sysconfdir}/logrotate.d/rsyslog
%endif
install -D -p -m 755 %{SOURCE15} %{buildroot}%{_unitdir}/rsyslog.service

cat rsyslog-%{version}/tools/recover_qi.pl |
  tr -d '\r' > %{buildroot}%{_bindir}/rsyslog-recover-qi.pl
chmod 755 %{buildroot}%{_bindir}/rsyslog-recover-qi.pl

%post
for n in /var/log/{messages,secure,maillog,spooler}
do
  [ -f $n ] && continue
  ( umask 066 && touch $n )
done

%systemd_post rsyslog.service

%preun
%systemd_preun rsyslog.service

%postun
%systemd_postun_with_restart rsyslog.service

%files
%defattr(-,root,root,-)
%doc rsyslog-%{version}/AUTHORS
%doc rsyslog-%{version}/COPYING*
%doc rsyslog-%{version}/ChangeLog
%doc %{_mandir}/*/*
%{_bindir}/lognormalizer
%{_bindir}/rscryutil
%{_bindir}/rsyslog-recover-qi.pl
%dir %{_libdir}/rsyslog
%{_libdir}/rsyslog/fmhash.so
%{_libdir}/rsyslog/fmhttp.so
%{_libdir}/rsyslog/fmpcre.so
%{_libdir}/rsyslog/fmunflatten.so
%{_libdir}/rsyslog/imdiag.so
%{_libdir}/rsyslog/imdtls.so
%{_libdir}/rsyslog/imdocker.so
%{_libdir}/rsyslog/imfile.so
%{_libdir}/rsyslog/imhttp.so
%{_libdir}/rsyslog/imjournal.so
%{_libdir}/rsyslog/imklog.so
%{_libdir}/rsyslog/imkmsg.so
%{_libdir}/rsyslog/immark.so
%{_libdir}/rsyslog/improg.so
%{_libdir}/rsyslog/impstats.so
%{_libdir}/rsyslog/imptcp.so
%{_libdir}/rsyslog/imrelp.so
%{_libdir}/rsyslog/imtcp.so
%{_libdir}/rsyslog/imudp.so
%{_libdir}/rsyslog/imuxsock.so
%{_libdir}/rsyslog/lmcry_gcry.so
%{_libdir}/rsyslog/lmnet.so
%{_libdir}/rsyslog/lmnetstrms.so
%{_libdir}/rsyslog/lmnsd_gtls.so
%{_libdir}/rsyslog/lmnsd_ossl.so
%{_libdir}/rsyslog/lmnsd_ptcp.so
%{_libdir}/rsyslog/lmregexp.so
%{_libdir}/rsyslog/lmtcpclt.so
%{_libdir}/rsyslog/lmtcpsrv.so
%{_libdir}/rsyslog/lmzlibw.so
%{_libdir}/rsyslog/lmzstdw.so
%{_libdir}/rsyslog/mmanon.so
%{_libdir}/rsyslog/mmaudit.so
%{_libdir}/rsyslog/mmcount.so
%{_libdir}/rsyslog/mmdblookup.so
%{_libdir}/rsyslog/mmexternal.so
%{_libdir}/rsyslog/mmfields.so
%{_libdir}/rsyslog/mmjsonparse.so
%{_libdir}/rsyslog/mmjsontransform.so
%{_libdir}/rsyslog/mmkubernetes.so
%{_libdir}/rsyslog/mmleefparse.so
%{_libdir}/rsyslog/mmnormalize.so
%{_libdir}/rsyslog/mmpstrucdata.so
%{_libdir}/rsyslog/mmsnareparse.so
%{_libdir}/rsyslog/mmrfc5424addhmac.so
%{_libdir}/rsyslog/mmrm1stspace.so
%{_libdir}/rsyslog/mmsequence.so
%{_libdir}/rsyslog/mmsnmptrapd.so
%{_libdir}/rsyslog/mmtaghostname.so
%{_libdir}/rsyslog/mmutf8fix.so
%{_libdir}/rsyslog/omclickhouse.so
%{_libdir}/rsyslog/omdtls.so
%{_libdir}/rsyslog/omelasticsearch.so
%{_libdir}/rsyslog/omhttp.so
%{_libdir}/rsyslog/omjournal.so
%{_libdir}/rsyslog/ommail.so
%{_libdir}/rsyslog/omprog.so
%{_libdir}/rsyslog/omrelp.so
%{_libdir}/rsyslog/omruleset.so
%{_libdir}/rsyslog/omsendertrack.so
%{_libdir}/rsyslog/omsnmp.so
%{_libdir}/rsyslog/omstdout.so
%{_libdir}/rsyslog/omtesting.so
%{_libdir}/rsyslog/omudpspoof.so
%{_libdir}/rsyslog/omuxsock.so
%{_libdir}/rsyslog/pmaixforwardedfrom.so
%{_libdir}/rsyslog/pmciscoios.so
%{_libdir}/rsyslog/pmdb2diag.so
%{_libdir}/rsyslog/pmlastmsg.so
%{_libdir}/rsyslog/pmnormalize.so
%{_libdir}/rsyslog/pmnull.so
%{_libdir}/rsyslog/pmsnare.so
%{_libdir}/rsyslog/pmpanngfw.so
%{_sbindir}/msggen
%{_sbindir}/rsyslog_diag_hostname
%{_sbindir}/rsyslogd
%config(noreplace) %{_sysconfdir}/rsyslog.conf
%dir %{_sysconfdir}/rsyslog.d
%config(noreplace) %{_sysconfdir}/sysconfig/rsyslog
%if 0%{?rhel} <= 8
%config(noreplace) %{_sysconfdir}/logrotate.d/syslog
%else
%config(noreplace) %{_sysconfdir}/logrotate.d/rsyslog
%endif
%{_unitdir}/rsyslog.service
%dir %{_var}/lib/rsyslog

%files mysql
%{_libdir}/rsyslog/ommysql.so
