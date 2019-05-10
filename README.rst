
.. Links
.. _main repository: https://github.com/foglamp/FogLAMP


*****************************
Packaging Project for FogLAMP
*****************************

This repo contains the scripts used to create a FogLAMP package.

We have separated the package build from the `main repository`_ in order to provide a more flexible packaging and to maintain the smallest possible footprint of the main project, even in terms of source code and development.


Internal Structure
==================

The repository contains the following set of files:

- Files named with **make_** prefix, such as ``make_deb``, are the shell scripts used to build the package. The scripts accept the architecture to build as argument (currently *x86* and *arm*).
- The **packages** folder contains the list package types to build. It contains *Debian* and *rpmbuild*, latter for RedHat/Centos RPM creation.

  - Inside the *packages/Debian* folder, we have the **architecture** folders, plus a *common* folder containing files that are common to all the architectures. The architectures that we provide at the moment are *armhf* and *x86_64*.

    - Inside the architecture folder we have the DEBIAN folder, which contains all the Debian-based files, i.e. control, pre/post inst/rm, needed for the creation of the package.

  - After the first build, the *packages/Debian* will also contain a **build** folder. This folder contains a copy of what will be used to build the package (in a directory with the same name of the package) and the package itself.

    - In the *build* folder, folders and files that have a sequence number are a previous package build.


The make_deb Script
===================

.. code-block:: console

  $ ./make_deb --help
  make_deb {x86|arm} [clean|cleanall]
  This script is used to create the Debian package of FogLAMP
  Arguments:
   x86      - Build an x86_64 package
   arm      - Build an armv7l package
   clean    - Remove all the old versions saved in format .XXXX
   cleanall - Remove all the versions, including the last one
  $

.. warning::

  Postgres dependencies will not be installed automatically.
  In order to use postgres storage engine, you will need manual installation of `postgresql`.

    .. code-block:: console

       yes Y | sudo apt install postgresql



Building a Debian Package
=========================

First, make sure that FogLAMP is properly installed via ``make install`` somewhere on your environment (default is */usr/local/foglamp*).
Next, select the architecture to use, *x86* or *arm*.
Finally, run the ``make_deb`` command:

.. code-block:: console

  $ ./make_deb x86
  The package root directory is : /home/foglamp/foglamp-pkg
  The FogLAMP directory is      : /usr/local/foglamp
  The FogLAMP version is        : 1.2
  The package will be built in  : /home/foglamp/foglamp-pkg/packages/Debian/build
  The architecture is set as    : x86_64
  The package name is           : foglamp-1.2-x86_64

  Populating the package...Done.
  Building the new package...
  dpkg-deb: building package 'foglamp' in 'foglamp-1.2-x86_64.deb'.
  Building Complete.
  $
  
The result will be:
  
.. code-block:: console

  $ ls -l packages/Debian/build/
  total 564
  drwxrwxr-x 4 foglamp foglamp   4096 Mar 23 17:35 foglamp-1.2-x86_64
  -rw-r--r-- 1 foglamp foglamp 572742 Mar 23 17:35 foglamp-1.2-x86_64.deb
  $
  
If you execute the ``make_deb`` command again, you will see:

.. code-block:: console

  $ ./make_deb x86
  The package root directory is : /home/foglamp/foglamp-pkg
  The FogLAMP directory is      : /usr/local/foglamp
  The FogLAMP version is        : 1.2
  The package will be built in  : /home/foglamp/foglamp-pkg/packages/Debian/build
  The architecture is set as    : x86_64
  The package name is           : foglamp-1.2-x86_64

  Saving the old working environment as foglamp-1.2-x86_64.0001
  Populating the package...Done.
  Saving the old package as foglamp-1.2-x86_64.deb.0001
  Building the new package...
  dpkg-deb: building package 'foglamp' in 'foglamp-1.2-x86_64.deb'.
  Building Complete.
  $
  $ ls -l packages/Debian/build/
  total 1128
  drwxrwxr-x 4 foglamp foglamp   4096 Mar 23 17:53 foglamp-1.2-x86_64
  drwxrwxr-x 4 foglamp foglamp   4096 Mar 23 17:35 foglamp-1.2-x86_64.0001
  -rw-r--r-- 1 foglamp foglamp 573080 Mar 23 17:54 foglamp-1.2-x86_64.deb
  -rw-r--r-- 1 foglamp foglamp 572742 Mar 23 17:35 foglamp-1.2-x86_64.deb.0001
  $
   
... where the previous build is now marked with the suffix *.0001*.


The make_rpm Script
===================
.. code-block:: console

  $ ./make_prm --help
  make_rpm help [clean|cleanall]
  This script is used to create the RPM package of FogLAMP
  Arguments:
   help     - Display this help text
   clean    - Remove all the old versions saved in format .XXXX
   cleanall - Remove all the versions, including the last one
  $

Building a RPM Package
======================

First, make sure that FogLAMP is properly installed via ``make install`` somewhere on your environment (default is */usr/local/foglamp*).
Next, *x86* is the only currently supported architecture for RedHat/Centos.
Finally, run the ``make_prm`` command:

.. code-block:: console

  $ ./make_prm
  The package root directory is : /home/foglamp/repos/foglamp-pkg
  The FogLAMP directory is      : /home/foglamp/foglamp
  The FogLAMP version is        : 1.5.2
  The package will be built in  : /home/foglamp/repos/foglamp-pkg/packages/rpmbuild/RPMS/x86_64
  The package name is           : foglamp-1.5.2-0.00.x86_64

  Saving the old working environment as foglamp-1.5.2-0.00.x86_64.0077
  Populating the package and updating version in control file...Done.
  Prepare data directory
  Saving the old package as foglamp-1.5.2-0.00.x86_64.rpm.0001
  Building the new package...
  Processing files: foglamp-1.5.2-0.00.x86_64
  Provides: foglamp = 1.5.2-0.00 foglamp(x86-64) = 1.5.2-0.00
  Requires(interp): /bin/sh /bin/sh /bin/sh
  Requires(rpmlib): rpmlib(FileDigests) <= 4.6.0-1 rpmlib(PayloadFilesHavePrefix) <= 4.0-1 rpmlib(CompressedFileNames) <= 3.0.4-1
  Requires(pre): /bin/sh
  Requires(post): /bin/sh
  Requires(preun): /bin/sh
  Checking for unpackaged file(s): /usr/lib/rpm/check-files /home/foglamp/repos/foglamp-pkg/packages/rpmbuild/BUILDROOT/foglamp-1.5.2-0.00.x86_64
  Wrote: /home/foglamp/repos/foglamp-pkg/packages/rpmbuild/RPMS/x86_64/foglamp-1.5.2-0.00.x86_64.rpm
  Building Complete.
  $

The result will be:

.. code-block:: console

  $ ls -l packages/rpmbuild/RPMS/x86_64
  total 6444
  -rw-rw-r-- 1 foglamp foglamp 6597376 May 10 02:08 foglamp-1.5.2-0.00.x86_64.rpm
  $

If you execute the ``make_rpm`` command again, you will see:

.. code-block:: console

  $ ./make_rpm
  The package root directory is : /home/foglamp/repos/foglamp-pkg
  The FogLAMP directory is      : /home/foglamp/foglamp
  The FogLAMP version is        : 1.5.2
  The package will be built in  : /home/foglamp/repos/foglamp-pkg/packages/rpmbuild/RPMS/x86_64
  The package name is           : foglamp-1.5.2-0.00.x86_64

  Saving the old working environment as foglamp-1.5.2-0.00.x86_64.0079
  Populating the package and updating version in control file...Done.
  Prepare data directory
  Saving the old package as foglamp-1.5.2-0.00.x86_64.rpm.0001
  Building the new package...
  Processing files: foglamp-1.5.2-0.00.x86_64
  Provides: foglamp = 1.5.2-0.00 foglamp(x86-64) = 1.5.2-0.00
  Requires(interp): /bin/sh /bin/sh /bin/sh
  Requires(rpmlib): rpmlib(FileDigests) <= 4.6.0-1 rpmlib(PayloadFilesHavePrefix) <= 4.0-1 rpmlib(CompressedFileNames) <= 3.0.4-1
  Requires(pre): /bin/sh
  Requires(post): /bin/sh
  Requires(preun): /bin/sh
  Checking for unpackaged file(s): /usr/lib/rpm/check-files /home/foglamp/repos/foglamp-pkg/packages/rpmbuild/BUILDROOT/foglamp-1.5.2-0.00.x86_64
  Wrote: /home/foglamp/repos/foglamp-pkg/packages/rpmbuild/RPMS/x86_64/foglamp-1.5.2-0.00.x86_64.rpm
  Building Complete.
  $ ls -l packages/rpmbuild/RPMS/x86_64
  total 12888
  -rw-rw-r-- 1 foglamp foglamp 6597420 May 10 02:10 foglamp-1.5.2-0.00.x86_64.rpm
  -rw-rw-r-- 1 foglamp foglamp 6597376 May 10 02:08 foglamp-1.5.2-0.00.x86_64.rpm.0001
  $

... where the previous build is now marked with the suffix *.0001*.



Cleaning the Package Folder
===========================

Use the ``clean`` option to remove all the old packages and the files used to make the package.
Use the ``cleanall`` option to remove all the packages and the files used to make the package.
