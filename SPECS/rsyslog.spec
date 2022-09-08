#
# License: MIT
# Author: Benoit DOLEZ <bdolez@zenetys.com>
# Copyright: 2019
#

%global __requires_exclude_from ^%{_bindir}/rsyslog-recover-qi\\.pl$

%define libestr                 libestr-0.1.11
%define liblognorm              liblognorm-2.0.6
%define liblogging              liblogging-1.0.6
%define libfastjson             libfastjson-0.99.9
%define librelp                 librelp-1.10.0
%if 0%{?rhel} <= 7
%define libcurl                 curl-7.85.0
%endif
%define libmaxminddb_version    1.6.0
%define libmaxminddb            libmaxminddb-%{libmaxminddb_version}
%define civetweb_version        1.15
%define civetweb                civetweb-%{civetweb_version}
%define builddir                %{_builddir}/%{name}-%{version}
%define static_only             --enable-static --disable-shared

Summary: Rsyslog v8 package by Zenetys
Name: rsyslog8z
Version: 8.2208.0
Release: 11%{?dist}.zenetys
License: GPLv3+ and ASL 2.0
Group: System Environment/Daemons

Source0: http://www.rsyslog.com/files/download/rsyslog/rsyslog-%{version}.tar.gz
Source10: rsyslog.conf
Source11: rsyslog.sysconfig
Source12: rsyslog.logrotate.systemd
Source13: rsyslog.logrotate.init
Source14: rsyslog.init
Source15: rsyslog.service
Source300: http://libestr.adiscon.com/files/download/%{libestr}.tar.gz
Source301: http://www.liblognorm.com/files/download/%{liblognorm}.tar.gz
Source302: http://download.rsyslog.com/liblogging/%{liblogging}.tar.gz
Source303: http://download.rsyslog.com/libfastjson/%{libfastjson}.tar.gz
Source304: http://download.rsyslog.com/librelp/%{librelp}.tar.gz
%if 0%{?rhel} <= 7
Source400: https://curl.haxx.se/download/%{libcurl}.tar.xz
%endif
Source402: https://github.com/maxmind/libmaxminddb/releases/download/%{libmaxminddb_version}/%{libmaxminddb}.tar.gz
Source403: https://github.com/civetweb/civetweb/archive/refs/tags/v%{civetweb_version}.tar.gz#/%{civetweb}.tar.gz

%if 0%{?rhel} <= 6
Patch50:  rsyslog-8.2208.0-build-on-gcc-lt-5.patch
%endif

Patch200: liblognorm-cef-first-extension.patch
Patch201: liblognorm-parseNameValue-fix-no-quoting-support.patch
Patch202: liblognorm-string-rulebase-bugfix-segfault-when-using-LF-in-jso.patch
Patch203: liblognorm-custom-type-memory-leak.patch
Patch204: liblognorm-string-perm-chars-overflow.patch

%if 0%{?rhel} <= 7
# curl patches
%endif

URL: http://www.rsyslog.com/
Vendor: Adiscon GmbH, Deutschland
Packager: Benoit DOLEZ <bdolez@zenetys.com>

BuildRequires: apr-util-devel
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: bison
BuildRequires: flex
BuildRequires: gnutls-devel
BuildRequires: libgcrypt-devel
BuildRequires: libnet-devel
BuildRequires: libtool
BuildRequires: libuuid-devel
BuildRequires: net-snmp-devel
BuildRequires: openssl-devel
BuildRequires: pkgconfig
BuildRequires: zlib-devel

%if 0%{?rhel} >= 8
BuildRequires: pkgconfig(libcurl)
%endif

%if 0%{?rhel} >= 7
BuildRequires: systemd-devel >= 219-39
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
%else
Requires(post): /sbin/chkconfig
Requires(preun): /sbin/chkconfig
Requires(preun): /sbin/service
Requires(postun): /sbin/service
%endif

Requires: bash >= 2.0
Requires: gnutls
Requires: logrotate >= 3.5.2

%if 0%{?rhel} >= 7
Requires: openssl-libs
%else
Requires: openssl
%endif

Provides: rsyslog
Provides: rsyslog-elasticsearch
Provides: rsyslog-fmhash
Provides: rsyslog-fmhttp
Provides: rsyslog-gnutls
Provides: rsyslog-mmaudit
Provides: rsyslog-mmfields
Provides: rsyslog-mmjsonparse
Provides: rsyslog-mmnormalize
Provides: rsyslog-mmrm1stspace
Provides: rsyslog-mysql
Provides: rsyslog-omhttp
Provides: rsyslog-openssl
Provides: rsyslog-pmciscoios
Provides: rsyslog-relp
Provides: rsyslog-snmp
Provides: rsyslog-udpspoof
Provides: syslog

Obsoletes: rsyslog
Obsoletes: rsyslog-elasticsearch
Obsoletes: rsyslog-fmhash
Obsoletes: rsyslog-fmhttp
Obsoletes: rsyslog-gnutls
Obsoletes: rsyslog-mmaudit
Obsoletes: rsyslog-mmfields
Obsoletes: rsyslog-mmjsonparse
Obsoletes: rsyslog-mmnormalize
Obsoletes: rsyslog-mmrm1stspace
Obsoletes: rsyslog-mysql
Obsoletes: rsyslog-omhttp
Obsoletes: rsyslog-openssl
Obsoletes: rsyslog-pmciscoios
Obsoletes: rsyslog-relp
Obsoletes: rsyslog-snmp
Obsoletes: rsyslog-udpspoof
Obsoletes: syslog

%description
Rsyslog is an enhanced, multi-threaded syslog daemon.

%package mysql
Summary: MySQL support for rsyslog
Group: System Environment/Daemons
Requires: %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
# mysql_config is required by rsyslog configure script
%if 0%{?rhel} >= 8
# on el8, mariadb-connector-c-devel contains mysql_config;
# dependencies install libs and headers; mysql is still available
# via stream but mariadb should be preferred.
BuildRequires: mariadb-connector-c-devel
%else
%if 0%{?rhel} == 7
# on el7, mariadb-devel (which provides mysql-devel) contains
# mysql_config; dependencies install libs and headers
BuildRequires: mariadb-devel
%else
%if 0%{?rhel} <= 6
# on el6, mysql contains the libs and mysql_config but does not
# depends on the headers so we need mysql-devel as well
BuildRequires: mysql
BuildRequires: mysql-devel
%endif
%endif
%endif

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
%if 0%{?rhel} <= 7
%setup -T -D -a 400
# curl patches
%endif
%setup -T -D -a 402
%setup -T -D -a 403

cd rsyslog-%{version}
# rsyslog patches
%if 0%{?rhel} <= 6
%patch50 -p1
%endif
cd ..

cd %{liblognorm}
%patch200 -p1
%patch201 -p1
%patch202 -p1
%patch203 -p1
%patch204 -p1
cd ..

%build
rsyslog_configure_cflags='-fPIC -g'
rsyslog_configure_ldflags=
rsyslog_configure_opts=()
rsyslog_make_opts=()
libestr_configure_cflags='-fPIC -g'
libfastjson_configure_cflags='-fPIC -g'
liblognorm_configure_cflags='-fPIC -g'
liblognorm_configure_opts=()
liblogging_configure_cflags='-fPIC -g'
librelp_configure_cflags='-fPIC -g'
libcurl_configure_cflags='-fPIC -g'
libmaxminddb_configure_cflags='-fPIC -g'
civetweb_cflags='-fPIC -g'
civetweb_make_opts=()

# libestr
(
    cd %{libestr}
    %configure %{static_only} \
        "CFLAGS=${libestr_configure_cflags}"
    make %{?_smp_mflags}
)
rsyslog_configure_opts+=( LIBESTR_CFLAGS="-I%{builddir}/%{libestr}/include" )
rsyslog_configure_opts+=( LIBESTR_LIBS="-L%{builddir}/%{libestr}/src/.libs -lestr" )
liblognorm_configure_opts+=( LIBESTR_CFLAGS="-I%{builddir}/%{libestr}/include" )
liblognorm_configure_opts+=( LIBESTR_LIBS="-L%{builddir}/%{libestr}/src/.libs -lestr" )

# libfastjson
(
    cd %{libfastjson}
    %configure %{static_only} \
        "CFLAGS=${libfastjson_configure_cflags}"
    make %{?_smp_mflags}
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
        "CFLAGS=${liblognorm_configure_cflags}" \
        "${liblognorm_configure_opts[@]}"
    make %{?_smp_mflags}
)
rsyslog_configure_opts+=( LIBLOGNORM_CFLAGS="-I%{builddir}/%{liblognorm}/src" )
rsyslog_configure_opts+=( LIBLOGNORM_LIBS="-L%{builddir}/%{liblognorm}/src/.libs -llognorm" )

# liblogging-stdlog
(
    cd %{liblogging}
    %configure %{static_only} \
        "CFLAGS=${liblogging_configure_cflags}"
    make %{?_smp_mflags}
)
rsyslog_configure_opts+=( LIBLOGGING_STDLOG_CFLAGS="-I%{builddir}/%{liblogging}/stdlog" )
rsyslog_configure_opts+=( LIBLOGGING_STDLOG_LIBS="-L%{builddir}/%{liblogging}/stdlog/.libs -llogging-stdlog" )

# librelp
(
    cd %{librelp}
    %configure %{static_only} \
        "CFLAGS=${librelp_configure_cflags}"
    make %{?_smp_mflags}
)
rsyslog_configure_opts+=( RELP_CFLAGS="-I%{builddir}/%{librelp}/src" )
rsyslog_configure_opts+=( RELP_LIBS="-L%{builddir}/%{librelp}/src/.libs -lrelp -lgnutls -lssl -lcrypto" )

# libcurl
%if 0%{?rhel} <= 7
(
    cd %{libcurl}
    %configure %{static_only} \
        --with-openssl \
        --disable-ldap \
        --disable-ldaps \
        "CFLAGS=${libcurl_configure_cflags}"
    make %{?_smp_mflags}
)
rsyslog_configure_opts+=( CURL_CFLAGS="-I%{builddir}/%{libcurl}/include" )
rsyslog_configure_opts+=( CURL_LIBS="-L%{builddir}/%{libcurl}/lib/.libs -lcurl -lz -lssl -lcrypto" )
%endif

# libmaxminddb
(
    cd %{libmaxminddb}
    %configure %{static_only} \
        "CFLAGS=${libmaxminddb_configure_cflags}"
    make %{?_smp_mflags}
)
rsyslog_configure_cflags+=" -I%{builddir}/%{libmaxminddb}/include"
rsyslog_configure_ldflags+=" -L%{builddir}/%{libmaxminddb}/src/.libs"

# civetweb
civetweb_make_opts+=( COPT='-DNO_SSL_DL' )
civetweb_make_opts+=( WITH_CFLAGS="$civetweb_cflags" )
%if 0%{?rhel} <= 7
civetweb_make_opts+=( WITH_OPENSSL_API_1_0=1 )
%endif
(
    cd %{civetweb}
    make lib %{?_smp_mflags} \
        "${civetweb_make_opts[@]}"
)
rsyslog_configure_cflags+=" -I%{builddir}/%{civetweb}/include"
rsyslog_make_opts+=( CIVETWEB_LIBS="-L%{builddir}/%{civetweb} -lcivetweb -lssl -lcrypto" )

# apr-util pkgconfig file gives -lldap_r in ldflags, it introduces
# a useless dependency, so force APU_LIBS to overcome that issue
rsyslog_configure_opts+=( APU_LIBS='-laprutil-1' )

OPTIONS=(
  --enable-regexp
  --enable-fmhash
  --enable-fmhash-xxhash
  --enable-fmunflatten
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
  # --enable-clickhouse
  --enable-openssl
  --enable-gnutls
  --enable-libgcrypt
  --enable-rsyslogrt
  --enable-rsyslogd
  # --enable-extended-tests
  --enable-mysql-tests
  --enable-pgsql-tests
  --enable-mail
  --enable-fmhttp

  --enable-mmnormalize
  --enable-mmjsonparse
  # --enable-mmgrok
  --enable-mmaudit
  --enable-mmanon
  --enable-mmrm1stspace
  --enable-mmutf8fix
  --enable-mmcount
  --enable-mmsequence
  --enable-mmdblookup
  --enable-mmfields
  --enable-mmpstrucdata
  --enable-mmrfc5424addhmac
  --enable-mmsnmptrapd
  # --enable-mmkubernetes

  --enable-omhttp
  #--enable-omfile-hardened
  --enable-relp
  --enable-omrelp-default-port
  # --enable-ksi-ls12
  --enable-liblogging-stdlog
  # --enable-rfc3195
  # --enable-testbench
  --enable-libfaketime
  # --enable-helgrind
  --enable-imdiag
  --enable-imfile
  --enable-imhttp
  --enable-improg
  # --enable-imsolaris
  --enable-imptcp
  --enable-impstats
  --enable-omprog
  --enable-omstdout
  # --enable-journal-tests
  --enable-pmlastmsg
  # --enable-pmcisconames
  --enable-pmciscoios
  --enable-pmnull
  --enable-pmnormalize
  # --enable-pmaixforwardedfrom
  # --enable-pmsnare
  --enable-pmpanngfw
  --enable-omudpspoof
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

%if 0%{?rhel} >= 7
  --enable-libsystemd
  --enable-imjournal
  --enable-omjournal
%endif

  CFLAGS="${rsyslog_configure_cflags}"
  LDFLAGS="${rsyslog_configure_ldflags}"
  "${rsyslog_configure_opts[@]}"
)

(
  cd rsyslog-%{version}
  export > config.exports # save environments vars
  autoreconf -i
  %configure --enable-static=no --enable-shared=yes "${OPTIONS[@]}"
  make %{?_smp_mflags} pkglibdir=%{_libdir}/rsyslog "${rsyslog_make_opts[@]}"
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
  install -d -m 755 %{buildroot}%{_docdir}
  install -p -m 644 AUTHORS %{buildroot}%{_docdir}
  install -p -m 644 COPYING* %{buildroot}%{_docdir}
  install -p -m 644 ChangeLog %{buildroot}%{_docdir}
)
rm -f %{buildroot}%{_libdir}/rsyslog/*.la
rm -f %{buildroot}%{_bindir}/rscryutil

gzip %{buildroot}%{_mandir}/*/*.[0-9]

install -d -m 700 %{buildroot}%{_var}/lib/rsyslog
install -d -m 755 %{buildroot}%{_sysconfdir}/rsyslog.d
install -p -m 644 %{SOURCE10} %{buildroot}%{_sysconfdir}/rsyslog.conf
install -D -p -m 644 %{SOURCE11} %{buildroot}%{_sysconfdir}/sysconfig/rsyslog
%if 0%{?rhel} >= 7
sed -i -e 's/^#imjournal# //' %{buildroot}%{_sysconfdir}/rsyslog.conf
sed -i -e '/^#imklog# /d' %{buildroot}%{_sysconfdir}/rsyslog.conf
install -D -p -m 644 %{SOURCE12} %{buildroot}%{_sysconfdir}/logrotate.d/syslog
install -D -p -m 755 %{SOURCE15} %{buildroot}%{_unitdir}/rsyslog.service
%else
sed -i -e '/^#imjournal# /d' %{buildroot}%{_sysconfdir}/rsyslog.conf
sed -i -e 's/^#imklog# //' %{buildroot}%{_sysconfdir}/rsyslog.conf
install -D -p -m 644 %{SOURCE13} %{buildroot}%{_sysconfdir}/logrotate.d/syslog
install -D -p -m 755 %{SOURCE14} %{buildroot}%{_initrddir}/rsyslog
rm -rf %{buildroot}%{_unitdir}
%endif

cat rsyslog-%{version}/tools/recover_qi.pl |
  tr -d '\r' > %{buildroot}%{_bindir}/rsyslog-recover-qi.pl
chmod 755 %{buildroot}%{_bindir}/rsyslog-recover-qi.pl

%post
for n in /var/log/{messages,secure,maillog,spooler}
do
  [ -f $n ] && continue
  ( umask 066 && touch $n )
done

%if 0%{?rhel} >= 7
%systemd_post rsyslog.service
%else
/sbin/chkconfig --add rsyslog
%endif

%if 0%{?rhel} == 7
if [ -f /etc/rsyslog.d/listen.conf ]; then
    # This file is brought by the systemd package and produces
    # a warning at rsyslog start. Comment out the directive.
    sed -i -re 's,^\s*(\$SystemLogSocketName\s),# \1,' /etc/rsyslog.d/listen.conf
fi
%endif

%preun
%if 0%{?rhel} >= 7
%systemd_preun rsyslog.service
%else
if [ "$1" = 0 ]; then
  /sbin/service rsyslog stop >/dev/null 2>&1 || :
  /sbin/chkconfig --del rsyslog
fi
%endif

%postun
%if 0%{?rhel} >= 7
%systemd_postun_with_restart rsyslog.service
%else
if [ "$1" -ge 1 ]; then
  /sbin/service rsyslog condrestart >/dev/null 2>&1 || :
fi
%endif

%files
%defattr(-,root,root,-)
%doc %{_docdir}/AUTHORS
%doc %{_docdir}/COPYING*
%doc %{_docdir}/ChangeLog
%doc %{_mandir}/*/*
%{_sbindir}/rsyslogd
%{_sbindir}/msggen
%dir %{_libdir}/rsyslog
%{_libdir}/rsyslog/omelasticsearch.so
%{_libdir}/rsyslog/pmlastmsg.so
%{_libdir}/rsyslog/fmhash.so
%{_libdir}/rsyslog/fmhttp.so
%{_libdir}/rsyslog/fmunflatten.so
%{_libdir}/rsyslog/imdiag.so
%{_libdir}/rsyslog/imfile.so
%{_libdir}/rsyslog/imhttp.so
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
%{_libdir}/rsyslog/mmanon.so
%{_libdir}/rsyslog/mmaudit.so
%{_libdir}/rsyslog/mmcount.so
%{_libdir}/rsyslog/mmdblookup.so
%{_libdir}/rsyslog/mmexternal.so
%{_libdir}/rsyslog/mmfields.so
%{_libdir}/rsyslog/mmjsonparse.so
%{_libdir}/rsyslog/mmnormalize.so
%{_libdir}/rsyslog/mmpstrucdata.so
%{_libdir}/rsyslog/mmrfc5424addhmac.so
%{_libdir}/rsyslog/mmrm1stspace.so
%{_libdir}/rsyslog/mmsequence.so
%{_libdir}/rsyslog/mmsnmptrapd.so
%{_libdir}/rsyslog/mmutf8fix.so
%{_libdir}/rsyslog/omhttp.so
%{_libdir}/rsyslog/ommail.so
%{_libdir}/rsyslog/omprog.so
%{_libdir}/rsyslog/omrelp.so
%{_libdir}/rsyslog/omruleset.so
%{_libdir}/rsyslog/omsnmp.so
%{_libdir}/rsyslog/omstdout.so
%{_libdir}/rsyslog/omtesting.so
%{_libdir}/rsyslog/omudpspoof.so
%{_libdir}/rsyslog/omuxsock.so
%{_libdir}/rsyslog/pmciscoios.so
%{_libdir}/rsyslog/pmnormalize.so
%{_libdir}/rsyslog/pmnull.so
%{_libdir}/rsyslog/pmpanngfw.so
%{_sbindir}/rsyslog_diag_hostname
%if 0%{?rhel} >= 7
%{_libdir}/rsyslog/imjournal.so
%{_libdir}/rsyslog/omjournal.so
%endif
%{_bindir}/lognormalizer
%{_bindir}/rsyslog-recover-qi.pl
%config(noreplace) %{_sysconfdir}/rsyslog.conf
%dir %{_sysconfdir}/rsyslog.d
%config(noreplace) %{_sysconfdir}/sysconfig/rsyslog
%config(noreplace) %{_sysconfdir}/logrotate.d/syslog
%if 0%{?rhel} >= 7
%{_unitdir}/rsyslog.service
%else
%{_initrddir}/rsyslog
%endif
%dir %{_var}/lib/rsyslog

%files mysql
%{_libdir}/rsyslog/ommysql.so
