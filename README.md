| Package&nbsp;name | Supported&nbsp;targets |
| :--- | :--- |
| rsyslog8z, rsyslog8z-mysql | el6, el7, el8, el9 |
<br/>

## Build:

The package can be built easily using the rpmbuild-docker script provided in this repository. In order to use this script, _**a functional Docker environment is needed**_, with ability to pull CentOS (el6, el7) or Rocky Linux (el8, el9) images from internet if not already downloaded.

```
$ ./rpmbuild-docker -d el6
$ ./rpmbuild-docker -d el7
$ ./rpmbuild-docker -d el8
$ ./rpmbuild-docker -d el9
```

## Prebuilt packages:

Builds of these packages are available on ZENETYS yum repositories:<br/>
https://packages.zenetys.com/latest/redhat/
