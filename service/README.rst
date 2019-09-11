*****************************
Packaging for Fledge Service
*****************************

This directory contains the deb and rpm scripts used to create a Fledge service package.

Internal Structure
==================

The directory contains the following set of files:

- Files named with **make_** prefix, such as ``make_deb``, ``make_rpm``, are the shell scripts used to build the package.
- The **packages** folder contains the list package types to build. It contains *DEBIAN* and *RPM*

  - Inside the *packages/DEBIAN* folder, which contains all the Debian-based files, i.e. control, postinst, needed for the creation of the package.

    - In the *archive/DEBIAN/architecture_name* folder which contains the build package.

  - Inside the *packages/RPM/SPECS* folder, which contains RPM spec-based file, i.e. service.spec needed for the creation of the package.

    - In the *archive/Rpm/architecture_name* folder which contains the build package.


The make_deb Script
===================

.. code-block:: console

  $ ./make_deb -h
  make_deb [-h] [-a] [-b <branch>] repository ...
  This script is used to create the Debian package for a Fledge service

  Arguments:
  -h	- Display this help text
  -a	- Remove all the versions
  -b	- Branch to base package on
  $


Building a Debian Package
=========================

First, make sure that Fledge_ROOT is set.
Finally, run the ``make_deb`` command:

.. code-block:: console

  $ ./make_deb -b develop fledge-service-notification
  Cloning into 'fledge-service-notification'...
  Checking connectivity... done.
  The package root directory is     : /tmp/fledge-service-notification
  The package build directory is    : /tmp/fledge-service-notification/build
  The Fledge required version      : >=1.6
  The architecture is set as        : x86_64
  The package will be built in      : /home/fledge/Development/fledge-pkg/service/archive/DEBIAN/x86_64
  The package name is               : fledge-service-notification-1.6.0-x86_64

  Populating the package and updating version file...Done.
  Building the package...
  dpkg-deb: building package 'fledge-service-notification' in 'fledge-service-notification-1.6.0-x86_64.deb'.
  Building Complete.
  $
  
The result will be:
  
.. code-block:: console

  $ ls -l archive/DEBIAN/x86_64/
  total 8
  drwxrwxr-x 4 fledge fledge  4096 fledge-service-notification-1.6.0-x86_64
  -rw-r--r-- 1 fledge fledge  3338 fledge-service-notification-1.6.0-x86_64-1.6.0.deb
  $

The make_rpm Script
===================
.. code-block:: console

  $ ./make_rpm --help
  make_rpm [-a] [-c] [-h] [-b <branch>] repository ...
  This script is used to create the RPM package for a Fledge service
  Arguments:
    -h	- Display this help text
    -c	- Remove all the old versions saved in format .XXXX
    -a	- Remove all the versions, including the last one
    -b	- Branch to base package on
  $

Building a RPM Package
======================

First, make sure that Fledge_ROOT is set.
Finally, run the ``make_rpm`` command:

.. code-block:: console

  $ ./make_rpm -b develop fledge-service-notification
  Cloning into 'fledge-service-notification'...
  Checking connectivity... done.
  The package root directory is                           : /tmp/fledge-service-notification
  The package build directory is                          : /tmp/fledge-service-notification/build
  The Fledge required version                            : >= 1.6
  The Fledge service notification version is             : 1.6.0
  The architecture is set as                              : x86_64
  The package will be built in                            : /home/fledge/Development/fledge-pkg/service/archive/Rpm/
  The package name is                                     : fledge-service-notification-1.6.0


  Building the package...
  Processing files: fledge-service-notification-1.6.0-1.x86_64
  Checking for unpackaged file(s): /usr/lib/rpm/check-files /tmp/fledge-service-notification/build/fledge-service-notification-1.6.0/BUILDROOT/fledge-service-notification-1.6.0-1.x86_64
  Wrote: /tmp/fledge-service-notification/build/fledge-service-notification-1.6.0/RPMS/x86_64/fledge-service-notification-1.6.0-1.x86_64.rpm
  Building Complete.
  $

The result will be:

.. code-block:: console

  $ ls -l archive/Rpm/x86_64
  total 12 -rw-rw-r-- 1 fledge fledge 11805 fledge-service-notification-1.6.0-1.x86_64.rpm
  $

Cleaning the Package Folder
===========================

Use the ``-a`` option to remove all the packages and the files used to make the package.
