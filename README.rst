
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
- The **packages** folder contains the list package types to build. At the moment, the only package type we provide is *Debian*
  - Inside the *packages/Debian* folder, we have the **architecture** folders, plus a *common* folder containing files that are common to all the architectures. The architectures that we provide at the moment are *armhf* and *x86_64*.
    - Inside the architecture folder we have the DEBIAN folder, which contains all the Debian-based files, i.e. control, pre/post inst/rm, needed for the creation of the package.
  - After the first build, the *packages/Debian* will also contain a **build** folder. This folder contains a copy of what will be used to build the package (in a directory with the same name of the package) and the package itself.
    - In the *build* folder, folders and files that have a sequence number are a previous package build.


Building a Package
==================

First, make sure that FogLAMP is properly installed via ``make install`` somewhere on your environment (default is */usr/local/foglamp*).
Next, select the architecture to use, *x86* or *arm*.
Finally, run the ``make_deb`` command:

.. code-block:: console

  $ ./make_deb x86
  The package root directory is : /home/foglamp/foglamp-pkg
  The FogLAMP directory is      : /usr/local/foglamp
  The FogLAMP version is        : 1.2
  The Package will be built in  : /home/foglamp/foglamp-pkg/packages/Debian/build
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
   The Package will be built in  : /home/foglamp/foglamp-pkg/packages/Debian/build
   The architecture is set as    : x86_64
   The package name is           : foglamp-1.2-x86_64

   Saving the old working environment as foglamp-1.2-x86_64.0001
   Populating the package...Done.
   Saving the old package as foglamp-1.2-x86_64.deb.0001
   Building the new package...
   dpkg-deb: building package 'foglamp' in 'foglamp-1.2-x86_64.deb'.
   Building Complete.
   $ ls -l packages/Debian/build/
   total 1128
   drwxrwxr-x 4 foglamp foglamp   4096 Mar 23 17:53 foglamp-1.2-x86_64
   drwxrwxr-x 4 foglamp foglamp   4096 Mar 23 17:35 foglamp-1.2-x86_64.0001
   -rw-r--r-- 1 foglamp foglamp 573080 Mar 23 17:54 foglamp-1.2-x86_64.deb
   -rw-r--r-- 1 foglamp foglamp 572742 Mar 23 17:35 foglamp-1.2-x86_64.deb.0001
   $
   
... where the previous build is now marked with the suffix *.0001*.

  
