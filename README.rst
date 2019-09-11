
.. Links
.. _main repository: https://github.com/fledge/Fledge


*****************************
Packaging Project for Fledge
*****************************

This repo contains the scripts used to create a Fledge package.

We have separated the package build from the `main repository`_ in order to provide a more flexible packaging and to maintain the smallest possible footprint of the main project, even in terms of source code and development.


Internal Structure
==================

The repository contains the following set of files:

- Files named with **make_** prefix, such as ``make_deb``, ``make_rpm``, are the shell scripts used to build the package. The script runs as per the architecture to build.
- The **packages** folder contains the list package types to build. It contains *Debian* and *rpmbuild*, latter for RedHat/Centos RPM creation.

  - Inside the *packages/Debian* folder, we have the **architecture** folders, plus a *common* folder containing files that are common to all the architectures. The architectures that we provide at the moment are *aarch64*, *armv7l* and *x86_64*.

    - Inside the architecture folder we have the DEBIAN folder, which contains only control file
    - Inside the common folder we have the DEBIAN folder, which contains pre/post inst/rm, needed for the creation of the package.

  - After the first build, the *packages/Debian* will also contain a **build/architecture** folder. This folder contains a copy of what will be used to build the package (in a directory with the same name of the package) and the package itself.

    - In the *build/architecture* folder, folders and files that have a sequence number are a previous package build.


The make_deb Script
===================

.. code-block:: console

  $ ./make_deb help
  make_deb [help|clean|cleanall]
  This script is used to create the Debian package of Fledge
  Arguments:
   help     - Display this help text
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

First, make sure that Fledge is properly installed via ``make install`` somewhere on your environment (default is */usr/local/fledge*).
Finally, run the ``make_deb`` command and it will make as per ``arch``:

.. code-block:: console

  $ ./make_deb
  The package root directory is : /home/fledge/fledge-pkg
  The Fledge directory is      : /usr/local/fledge
  The Fledge version is        : 1.6.0
  The package will be built in  : /home/fledge/fledge-pkg/packages/Debian/build/x86_64
  The architecture is set as    : x86_64
  The package name is           : fledge-1.6.0-x86_64

  Populating the package...Done.
  Building the new package...
  dpkg-deb: building package 'fledge' in 'fledge-1.6.0-x86_64.deb'.
  Building Complete.
  $
  
The result will be:
  
.. code-block:: console

  $ ls -l packages/Debian/build/x86_64
  total 564
  drwxrwxr-x 4 fledge fledge   4096 Mar 23 17:35 fledge-1.6.0-x86_64
  -rw-r--r-- 1 fledge fledge 572742 Mar 23 17:35 fledge-1.6.0-x86_64.deb
  $
  
If you execute the ``make_deb`` command again, you will see:

.. code-block:: console

  $ ./make_deb
  The package root directory is : /home/fledge/fledge-pkg
  The Fledge directory is      : /usr/local/fledge
  The Fledge version is        : 1.6.0
  The package will be built in  : /home/fledge/fledge-pkg/packages/Debian/build/x86_64
  The architecture is set as    : x86_64
  The package name is           : fledge-1.6.0-x86_64

  Saving the old working environment as fledge-1.6.0-x86_64.0001
  Populating the package...Done.
  Saving the old package as fledge-1.6.0-x86_64.deb.0001
  Building the new package...
  dpkg-deb: building package 'fledge' in 'fledge-1.6.0-x86_64.deb'.
  Building Complete.
  $
  $ ls -l packages/Debian/build/x86_64
  total 1128
  drwxrwxr-x 4 fledge fledge   4096 Mar 23 17:53 fledge-1.6.0-x86_64
  drwxrwxr-x 4 fledge fledge   4096 Mar 23 17:35 fledge-1.6.0-x86_64.0001
  -rw-r--r-- 1 fledge fledge 573080 Mar 23 17:54 fledge-1.6.0-x86_64.deb
  -rw-r--r-- 1 fledge fledge 572742 Mar 23 17:35 fledge-1.6.0-x86_64.deb.0001
  $
   
... where the previous build is now marked with the suffix *.0001*.


The make_rpm Script
===================
.. code-block:: console

  $ ./make_rpm --help
  make_rpm help [clean|cleanall]
  This script is used to create the RPM package of Fledge
  Arguments:
   help     - Display this help text
   clean    - Remove all the old versions saved in format .XXXX
   cleanall - Remove all the versions, including the last one
  $

Building a RPM Package
======================

First, make sure that Fledge is properly installed via ``make install`` somewhere on your environment (default is */usr/local/fledge*).
Next, *x86* is the only currently supported architecture for RedHat/Centos.
Finally, run the ``make_rpm`` command:

.. code-block:: console

  $ ./make_rpm
  The package root directory is : /home/fledge/repos/fledge-pkg
  The Fledge directory is      : /home/fledge/fledge
  The Fledge version is        : 1.5.2
  The package will be built in  : /home/fledge/repos/fledge-pkg/packages/rpmbuild/RPMS/x86_64
  The package name is           : fledge-1.5.2-1.x86_64

  Saving the old working environment as fledge-1.5.2-1.x86_64.0077
  Populating the package and updating version in control file...Done.
  Prepare data directory
  Saving the old package as fledge-1.5.2-1.x86_64.rpm.0001
  Building the new package...
  Processing files: fledge-1.5.2-1.x86_64
  Provides: fledge = 1.5.2-1 fledge(x86-64) = 1.5.2-1
  Requires(interp): /bin/sh /bin/sh /bin/sh
  Requires(rpmlib): rpmlib(FileDigests) <= 4.6.0-1 rpmlib(PayloadFilesHavePrefix) <= 4.0-1 rpmlib(CompressedFileNames) <= 3.0.4-1
  Requires(pre): /bin/sh
  Requires(post): /bin/sh
  Requires(preun): /bin/sh
  Checking for unpackaged file(s): /usr/lib/rpm/check-files /home/fledge/repos/fledge-pkg/packages/rpmbuild/BUILDROOT/fledge-1.5.2-1.x86_64
  Wrote: /home/fledge/repos/fledge-pkg/packages/rpmbuild/RPMS/x86_64/fledge-1.5.2-1.x86_64.rpm
  Building Complete.
  $

The result will be:

.. code-block:: console

  $ ls -l packages/rpmbuild/RPMS/x86_64
  total 6444
  -rw-rw-r-- 1 fledge fledge 6597376 May 10 02:08 fledge-1.5.2-1.x86_64.rpm
  $

If you execute the ``make_rpm`` command again, you will see:

.. code-block:: console

  $ ./make_rpm
  The package root directory is : /home/fledge/repos/fledge-pkg
  The Fledge directory is      : /home/fledge/fledge
  The Fledge version is        : 1.5.2
  The package will be built in  : /home/fledge/repos/fledge-pkg/packages/rpmbuild/RPMS/x86_64
  The package name is           : fledge-1.5.2-1.x86_64

  Saving the old working environment as fledge-1.5.2-1.x86_64.0079
  Populating the package and updating version in control file...Done.
  Prepare data directory
  Saving the old package as fledge-1.5.2-1.x86_64.rpm.0001
  Building the new package...
  Processing files: fledge-1.5.2-1.x86_64
  Provides: fledge = 1.5.2-1 fledge(x86-64) = 1.5.2-1
  Requires(interp): /bin/sh /bin/sh /bin/sh
  Requires(rpmlib): rpmlib(FileDigests) <= 4.6.0-1 rpmlib(PayloadFilesHavePrefix) <= 4.0-1 rpmlib(CompressedFileNames) <= 3.0.4-1
  Requires(pre): /bin/sh
  Requires(post): /bin/sh
  Requires(preun): /bin/sh
  Checking for unpackaged file(s): /usr/lib/rpm/check-files /home/fledge/repos/fledge-pkg/packages/rpmbuild/BUILDROOT/fledge-1.5.2-1.x86_64
  Wrote: /home/fledge/repos/fledge-pkg/packages/rpmbuild/RPMS/x86_64/fledge-1.5.2-1.x86_64.rpm
  Building Complete.
  $ ls -l packages/rpmbuild/RPMS/x86_64
  total 12888
  -rw-rw-r-- 1 fledge fledge 6597420 May 10 02:10 fledge-1.5.2-1.x86_64.rpm
  -rw-rw-r-- 1 fledge fledge 6597376 May 10 02:08 fledge-1.5.2-1.x86_64.rpm.0001
  $

... where the previous build is now marked with the suffix *.0001*.



Cleaning the Package Folder
===========================

Use the ``clean`` option to remove all the old packages and the files used to make the package.
Use the ``cleanall`` option to remove all the packages and the files used to make the package.


Packaging for Plugins
======================

Please refer to documentation `here <plugins/README.rst>`_
