#
# License: MIT
# Author: Benoit DOLEZ <bdolez@zenetys.com>
# Copyright: 2019
#

%define libestr                 libestr-0.1.11
%define liblognorm              liblognorm-2.0.6
%define liblogging              liblogging-1.0.6
%define libfastjson             libfastjson-0.99.8
%define librelp                 librelp-1.2.18
%define libcurl                 curl-7.67.0
%define libnet_version          1.1.6
%define libnet                  libnet-%{libnet_version}
%define libmaxminddb_version    1.4.2
%define libmaxminddb            libmaxminddb-%{libmaxminddb_version}
%define builddir                %{_builddir}/%{name}-%{version}
%define static_only             --enable-static --disable-shared

Summary: Rsyslog v8 package by Zenetys
Name: rsyslog8z
Version: 8.1903.0
Release: 1%{?dist}.zenetys
License: GPLv3+ and ASL 2.0
Group: System Environment/Daemons

Source0: http://www.rsyslog.com/files/download/rsyslog/rsyslog-%{version}.tar.gz
Source10: rsyslog.conf
Source11: rsyslog.sysconfig
Source12: rsyslog.log
Source300: http://libestr.adiscon.com/files/download/%{libestr}.tar.gz
Source301: http://www.liblognorm.com/files/download/%{liblognorm}.tar.gz
Source302: http://download.rsyslog.com/liblogging/%{liblogging}.tar.gz
Source303: http://download.rsyslog.com/libfastjson/%{libfastjson}.tar.gz
Source304: http://download.rsyslog.com/librelp/%{librelp}.tar.gz
Source400: https://curl.haxx.se/download/%{libcurl}.tar.xz
Source401: https://github.com/libnet/libnet/releases/download/v%{libnet_version}/%{libnet}.tar.gz
Source402: https://github.com/maxmind/libmaxminddb/releases/download/%{libmaxminddb_version}/%{libmaxminddb}.tar.gz

%if 0%{?rhel} >= 7
Patch0: rsyslog-systemd-centos7.patch
%endif

URL: http://www.rsyslog.com/
Vendor: Adiscon GmbH, Deutschland
Packager: Benoit DOLEZ <bdolez@zenetys.com>

BuildRequires: automake
BuildRequires: autoconf
BuildRequires: libtool
BuildRequires: bison
BuildRequires: flex
BuildRequires: libuuid-devel
BuildRequires: pkgconfig
BuildRequires: zlib-devel
BuildRequires: libgcrypt-devel
BuildRequires: libuuid-devel
BuildRequires: gnutls-devel
BuildRequires: net-snmp-devel
BuildRequires: openssl-devel

%if 0%{?rhel} >= 7
BuildRequires: systemd-devel >= 219-39
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
%endif

Requires: logrotate >= 3.5.2
Requires: openssl-libs
Requires: gnutls
Requires: bash >= 2.0
Provides: config(rsyslog) = %version-%release
Provides: rsyslog = %version-%release
Provides: rsyslog(x86-64) = %version-%release
Provides: syslog

%description
Rsyslog is an enhanced, multi-threaded syslog daemon.

%prep
%setup -c %{name}-%{version}
%setup -T -D -a 300
%setup -T -D -a 301
%setup -T -D -a 302
%setup -T -D -a 303
%setup -T -D -a 304
%setup -T -D -a 400
%setup -T -D -a 401
%setup -T -D -a 402

%if 0%{?rhel} >= 7
cd rsyslog-%{version}
%patch0 -p1
cd ..
%endif

%build
export CFLAGS="-fPIC"

( cd %{libestr} && %configure %{static_only} && make %{?_smp_mflags} )

export LIBESTR_CFLAGS="-I%{builddir}/%{libestr}/include"
export LIBESTR_LIBS="%{builddir}/%{libestr}/src/.libs/libestr.a -L%{builddir}/%{libestr}/src/.libs/"

( cd %{libfastjson} && %configure %{static_only} && make %{?_smp_mflags} )

export LIBFASTJSON_CFLAGS="-I%{builddir}/%{libfastjson}"
export LIBFASTJSON_LIBS="%{builddir}/%{libfastjson}/.libs/libfastjson.a -L%{builddir}/%{libfastjson}/.libs/"

export JSON_C_CFLAGS="-I%{builddir}/%{libfastjson}"
export JSON_C_LIBS="%{builddir}/%{libfastjson}/.libs/libfastjson.a -L%{builddir}/%{libfastjson}/.libs/"

( cd %{liblognorm} && %configure %{static_only} && make %{?_smp_mflags} )

export LIBLOGNORM_CFLAGS="-I%{builddir}/%{liblognorm}/src"
export LIBLOGNORM_LIBS="%{builddir}/%{liblognorm}/src/.libs/liblognorm.a -L%{builddir}/%{liblognorm}/src/.libs"

( cd %{liblogging} && %configure %{static_only} && make %{?_smp_mflags} )

export LIBLOGGING_STDLOG_CFLAGS="-I%{builddir}/%{liblogging}/stdlog"
export LIBLOGGING_STDLOG_LIBS="%{builddir}/%{liblogging}/stdlog/.libs/liblogging-stdlog.a -L%{builddir}/%{liblogging}/stdlog/.libs"

( cd %{librelp} && %configure %{static_only} && make %{?_smp_mflags} )

export RELP_CFLAGS="-I%{builddir}/%{librelp}/src"
export RELP_LIBS="%{builddir}/%{librelp}/src/.libs/librelp.a -L%{builddir}/%{librelp}/src/.libs -lgnutls"

( cd %{libnet} && %configure %{static_only} && make %{?_smp_mflags} )

export LIBNET_CFLAGS="-I%{builddir}/%{libnet}/include"
export LIBNET_LIBS="%{builddir}/%{libnet}/src/.libs/libnet.a -L%{builddir}/%{libnet}/src/.libs"

export UDPSPOOF_CFLAGS="${LIBNET_CFLAGS}"
export UDPSPOOF_LIBS="${LIBNET_LIBS}"

( cd %{libcurl} && %configure %{static_only} && make %{?_smp_mflags} )

export CURL_CFLAGS="-I%{builddir}/%{libcurl}/include"
export CURL_LIBS="%{builddir}/%{libcurl}/lib/.libs/libcurl.a -L%{builddir}/%{libcurl}/lib/.libs -lz -lssl -lcrypto"

( cd %{libmaxminddb} && %configure %{static_only} && make %{?_smp_mflags} )

export MAXMINDDB_CFLAGS="-I%{builddir}/%{libmaxminddb}/include"
export MAXMINDDB_LIBS="%{builddir}/%{libmaxminddb}/src/.libs/libmaxminddb.a -L%{builddir}/%{libmaxminddb}/src/.libs"

export CFLAGS="-fPIC ${LIBNET_CFLAGS} ${MAXMINDDB_CFLAGS}"
export LIBS="${LIBNET_LIBS} ${MAXMINDDB_LIBS}"

OPTIONS=(
  --enable-regexp
  --enable-fmhash
  # --enable-fmhash-xxhash
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
  # --enable-mysql
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
  --enable-imfile
  --enable-improg
  # --enable-imsolaris
  --enable-imptcp
  --enable-impstats
  --enable-omprog
  --enable-omstdout
  # --enable-journal-tests
  --enable-pmlastmsg
  # --enable-pmcisconames
  # --enable-pmciscoios
  --enable-pmnull
  --enable-pmnormalize
  # --enable-pmaixforwardedfrom
  # --enable-pmsnare
  # --enable-pmpanngfw
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
)

(
  cd rsyslog-%{version}
  export > config.exports # save environments vars
  %configure --enable-static=no --enable-shared=yes ${OPTIONS[@]}
  make %{?_smp_mflags} pkglibdir=%{_libdir}/rsyslog
)

%install
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
%else
sed -i -e '/^#imjournal# /d' %{buildroot}%{_sysconfdir}/rsyslog.conf
sed -i -e 's/^#imklog# //' %{buildroot}%{_sysconfdir}/rsyslog.conf
%endif
install -D -p -m 644 %{SOURCE12} %{buildroot}%{_sysconfdir}/logrotate.d/syslog

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

%preun
%systemd_preun rsyslog.service

%postun
%systemd_postun_with_restart rsyslog.service
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
%{_libdir}/rsyslog/imdiag.so
%{_libdir}/rsyslog/imfile.so
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
# %{_libdir}/rsyslog/omfile-hardened.so
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
%{_libdir}/rsyslog/pmnormalize.so
%{_libdir}/rsyslog/pmnull.so
%{_sbindir}/rsyslog_diag_hostname
%if 0%{?rhel} >= 7
%{_libdir}/rsyslog/imjournal.so
%{_libdir}/rsyslog/omjournal.so
%endif
%{_bindir}/rsyslog-recover-qi.pl
%config(noreplace) %{_sysconfdir}/rsyslog.conf
%dir %{_sysconfdir}/rsyslog.d
%config(noreplace) %{_sysconfdir}/sysconfig/rsyslog
%config(noreplace) %{_sysconfdir}/logrotate.d/syslog
%if 0%{?rhel} >= 7
%{_unitdir}/rsyslog.service
%endif
%dir %{_var}/lib/rsyslog
