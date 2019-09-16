*****************************
Packaging for FogLAMP Plugins
*****************************

This directory contains the deb and rpm scripts used to create a FogLAMP plugins package.

Internal Structure
==================

The directory contains the following set of files:

- Files named with **make_** prefix, such as ``make_deb``, ``make_rpm``, are the shell scripts used to build the package.
- The **packages** folder contains the list package types to build. It contains *DEBIAN* and *RPM*

  - Inside the *packages/DEBIAN* folder, which contains all the Debian-based files, i.e. control, postinst, needed for the creation of the package.

    - In the *archive/DEBIAN/architecture_name* folder which contains the build package.

  - Inside the *packages/RPM/SPECS* folder, which contains RPM spec-based file, i.e. plugin.spec needed for the creation of the package.

    - In the *archive/architecture_name* folder folder which contains the build package.


The make_deb Script
===================

.. code-block:: console

  $ ./make_deb -h
  make_deb [-h] [-a] [-b <branch>] repository ...
  This script is used to create the Debian package for a FogLAMP plugin

  Arguments:
  -h	- Display this help text
  -a	- Remove all the versions
  -b	- Branch to base package on
  $


Building a Debian Package
=========================

First, make sure that FogLAMP_ROOT is set.
Finally, run the ``make_deb`` command:

.. code-block:: console

  $ ./make_deb -b develop foglamp-south-sinusoid
  Cloning into 'foglamp-south-sinusoid'...

  Checking connectivity... done.
  Version is 1.6.0
  The package root directory is                         : /tmp/foglamp-south-sinusoid
  The FogLAMP south sinusoid  version is                : 1.6.0
  The package will be built in                          : /tmp/foglamp-south-sinusoid/packages/build
  The package name is                                   : foglamp-south-sinusoid-1.6.0

  Populating the package and updating version file...Done.
  Building the new package...
  dpkg-deb: building package 'foglamp-south-sinusoid' in 'foglamp-south-sinusoid-1.6.0.deb'.
  Building Complete.
  $
  
The result will be:
  
.. code-block:: console

  $ ls -l archive/DEBIAN/x86_64/
  total 8
  drwxrwxr-x 4 foglamp foglamp  4096 foglamp-south-sinusoid-1.6.0
  -rw-r--r-- 1 foglamp foglamp  3338 foglamp-south-sinusoid-1.6.0.deb
  $

The make_rpm Script
===================
.. code-block:: console

  $ ./make_rpm --help
  make_rpm [-a] [-c] [-h] [-b <branch>] repository ...
  This script is used to create the RPM package for a FogLAMP plugin

  Arguments:
    -h	- Display this help text
    -c	- Remove all the old versions saved in format .XXXX
    -a	- Remove all the versions, including the last one
    -b	- Branch to base package on
  $

Building a RPM Package
======================

First, make sure that FogLAMP_ROOT is set.
Finally, run the ``make_rpm`` command:

.. code-block:: console

  $ ./make_rpm -b develop foglamp-south-sinusoid
  Cloning into 'foglamp-south-sinusoid'...
  Checking connectivity... done.
  Version is 1.6.0
  The package root directory is                        : /tmp/foglamp-south-sinusoid
  The FogLAMP south sinusoid version is                : 1.6.0
  The package will be built in                         : /tmp/foglamp-south-sinusoid/packages/build
  The package name is                                  : foglamp-south-sinusoid-1.6.0

  Populating the package and updating version file...Done.
  Building the new package...
  Processing files: foglamp-south-sinusoid-1.6.0-1.x86_64
  Checking for unpackaged file(s): /usr/lib/rpm/check-files /tmp/foglamp-south-sinusoid/packages/build/foglamp-south-sinusoid-1.6.0/BUILDROOT/foglamp-south-sinusoid-1.6.0-1.x86_64
  Wrote: /tmp/foglamp-south-sinusoid/packages/build/foglamp-south-sinusoid-1.6.0/RPMS/x86_64/foglamp-south-sinusoid-1.6.0-1.x86_64.rpm
  Building Complete.
  $

The result will be:

.. code-block:: console

  $ ls -l archive/x86_64
  total 12
  -rw-rw-r-- 1 foglamp foglamp 11805 foglamp-south-sinusoid-1.6.0-1.x86_64.rpm
  $

Cleaning the Package Folder
===========================

Use the ``-a`` option to remove all the packages and the files used to make the package.
