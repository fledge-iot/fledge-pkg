**********************************
Packaging for Additional libraries
**********************************

This directory contains the deb scripts used to create a additional library package.

Internal Structure
==================

The directory contains the following set of files:

- File name ``make_deb`` is the shell script used to build the package.
- The **packages** folder contains *DEBIAN* structure
  - Inside the *packages/DEBIAN* folder, which contains all the Debian-based files, i.e. control, postinst, needed for the creation of the package.

- The **archive** folder contains the debian package
    - Actual debian files and package exists in the *archive/DEBIAN/architecture_name/{additional_lib_name}*

- The **scripts** folder contains the internal files for additional package
  - In the *scripts/{additional_lib_name}/Description* which contains the description of a package.
  - In the *scripts/{additional_lib_name}/VERSION* which contains the version info for the additional and the fledge core version.
  - In the *scripts/{additional_lib_name}/requirements.sh* which is shell script to obtain the actual additional libraries.


The make_deb Script
===================

.. code-block:: console

    $ ./make_deb -h
    make_deb [-h] [-a] ...
    This script is used to create the Debian package for to support other additional libraries as separately such as mqtt

    Arguments:
      -h	- Display this help text
      -a	- Remove all the archive versions
    $

Building a Debian Package
=========================

.. code-block:: console

    $ ./make_deb mqtt
    Cloning into 'paho.mqtt.c'...
    remote: Enumerating objects: 10055, done.
    remote: Total 10055 (delta 0), reused 0 (delta 0), pack-reused 10055
    Receiving objects: 100% (10055/10055), 7.82 MiB | 2.80 MiB/s, done.
    Resolving deltas: 100% (7112/7112), done.
    [sudo] password for aj:
    Reading package lists... Done
    Building dependency tree
    Reading state information... Done
    pkg-config is already the newest version (0.29.1-0ubuntu2).
    libssl-dev is already the newest version (1.1.1-1ubuntu2.1~18.04.7).
    The following packages were automatically installed and are no longer required:
      libatlas-base-dev libatlas3-base libboost-filesystem-dev libboost-program-options-dev libgfortran4 linux-hwe-5.4-headers-5.4.0-42
      linux-hwe-5.4-headers-5.4.0-47 linux-hwe-5.4-headers-5.4.0-48 linux-hwe-5.4-headers-5.4.0-51 linux-hwe-5.4-headers-5.4.0-52
      linux-hwe-5.4-headers-5.4.0-54
    Use 'sudo apt autoremove' to remove them.
    0 upgraded, 0 newly installed, 0 to remove and 28 not upgraded.
    -- The C compiler identification is GNU 7.5.0
    -- Check for working C compiler: /usr/bin/cc
    -- Check for working C compiler: /usr/bin/cc -- works
    -- Detecting C compiler ABI info
    -- Detecting C compiler ABI info - done
    -- Detecting C compile features
    -- Detecting C compile features - done
    -- CMake version: 3.10.2
    -- CMake system name: Linux
    -- Timestamp is 2021-01-11T11:14:26Z
    -- Found OpenSSL: /usr/lib/x86_64-linux-gnu/libcrypto.so (found version "1.1.1")
    -- Configuring done
    -- Generating done
    -- Build files have been written to: /home/aj/Development/fledge-pkg/others/paho.mqtt.c/build
    Scanning dependencies of target common_obj
    [  1%] Building C object src/CMakeFiles/common_obj.dir/MQTTTime.c.o
    [  2%] Building C object src/CMakeFiles/common_obj.dir/MQTTProtocolClient.c.o
    [  3%] Building C object src/CMakeFiles/common_obj.dir/Clients.c.o
    [  4%] Building C object src/CMakeFiles/common_obj.dir/utf-8.c.o
    [  5%] Building C object src/CMakeFiles/common_obj.dir/MQTTPacket.c.o
    [  6%] Building C object src/CMakeFiles/common_obj.dir/MQTTPacketOut.c.o
    [  7%] Building C object src/CMakeFiles/common_obj.dir/Messages.c.o
    [  8%] Building C object src/CMakeFiles/common_obj.dir/Tree.c.o
    [  9%] Building C object src/CMakeFiles/common_obj.dir/Socket.c.o
    [ 10%] Building C object src/CMakeFiles/common_obj.dir/Log.c.o
    [ 11%] Building C object src/CMakeFiles/common_obj.dir/MQTTPersistence.c.o
    [ 12%] Building C object src/CMakeFiles/common_obj.dir/Thread.c.o
    [ 13%] Building C object src/CMakeFiles/common_obj.dir/MQTTProtocolOut.c.o
    [ 15%] Building C object src/CMakeFiles/common_obj.dir/MQTTPersistenceDefault.c.o
    [ 16%] Building C object src/CMakeFiles/common_obj.dir/SocketBuffer.c.o
    [ 17%] Building C object src/CMakeFiles/common_obj.dir/LinkedList.c.o
    [ 18%] Building C object src/CMakeFiles/common_obj.dir/MQTTProperties.c.o
    [ 19%] Building C object src/CMakeFiles/common_obj.dir/MQTTReasonCodes.c.o
    [ 20%] Building C object src/CMakeFiles/common_obj.dir/Base64.c.o
    [ 21%] Building C object src/CMakeFiles/common_obj.dir/SHA1.c.o
    [ 22%] Building C object src/CMakeFiles/common_obj.dir/WebSocket.c.o
    [ 23%] Building C object src/CMakeFiles/common_obj.dir/StackTrace.c.o
    [ 24%] Building C object src/CMakeFiles/common_obj.dir/Heap.c.o
    [ 24%] Built target common_obj
    Scanning dependencies of target paho-mqtt3a
    [ 25%] Building C object src/CMakeFiles/paho-mqtt3a.dir/MQTTAsync.c.o
    [ 26%] Building C object src/CMakeFiles/paho-mqtt3a.dir/MQTTAsyncUtils.c.o
    [ 27%] Linking C shared library libpaho-mqtt3a.so
    [ 27%] Built target paho-mqtt3a
    Scanning dependencies of target paho-mqtt3c
    [ 29%] Building C object src/CMakeFiles/paho-mqtt3c.dir/MQTTClient.c.o
    [ 30%] Linking C shared library libpaho-mqtt3c.so
    [ 30%] Built target paho-mqtt3c
    Scanning dependencies of target common_ssl_obj
    [ 31%] Building C object src/CMakeFiles/common_ssl_obj.dir/MQTTTime.c.o
    [ 31%] Building C object src/CMakeFiles/common_ssl_obj.dir/MQTTProtocolClient.c.o
    [ 32%] Building C object src/CMakeFiles/common_ssl_obj.dir/Clients.c.o
    [ 33%] Building C object src/CMakeFiles/common_ssl_obj.dir/utf-8.c.o
    [ 34%] Building C object src/CMakeFiles/common_ssl_obj.dir/MQTTPacket.c.o
    [ 35%] Building C object src/CMakeFiles/common_ssl_obj.dir/MQTTPacketOut.c.o
    [ 36%] Building C object src/CMakeFiles/common_ssl_obj.dir/Messages.c.o
    [ 37%] Building C object src/CMakeFiles/common_ssl_obj.dir/Tree.c.o
    [ 38%] Building C object src/CMakeFiles/common_ssl_obj.dir/Socket.c.o
    [ 39%] Building C object src/CMakeFiles/common_ssl_obj.dir/Log.c.o
    [ 40%] Building C object src/CMakeFiles/common_ssl_obj.dir/MQTTPersistence.c.o
    [ 41%] Building C object src/CMakeFiles/common_ssl_obj.dir/Thread.c.o
    [ 43%] Building C object src/CMakeFiles/common_ssl_obj.dir/MQTTProtocolOut.c.o
    [ 44%] Building C object src/CMakeFiles/common_ssl_obj.dir/MQTTPersistenceDefault.c.o
    [ 45%] Building C object src/CMakeFiles/common_ssl_obj.dir/SocketBuffer.c.o
    [ 46%] Building C object src/CMakeFiles/common_ssl_obj.dir/LinkedList.c.o
    [ 47%] Building C object src/CMakeFiles/common_ssl_obj.dir/MQTTProperties.c.o
    [ 48%] Building C object src/CMakeFiles/common_ssl_obj.dir/MQTTReasonCodes.c.o
    [ 49%] Building C object src/CMakeFiles/common_ssl_obj.dir/Base64.c.o
    [ 50%] Building C object src/CMakeFiles/common_ssl_obj.dir/SHA1.c.o
    [ 51%] Building C object src/CMakeFiles/common_ssl_obj.dir/WebSocket.c.o
    [ 52%] Building C object src/CMakeFiles/common_ssl_obj.dir/StackTrace.c.o
    [ 53%] Building C object src/CMakeFiles/common_ssl_obj.dir/Heap.c.o
    [ 53%] Built target common_ssl_obj
    Scanning dependencies of target paho-mqtt3cs
    [ 54%] Building C object src/CMakeFiles/paho-mqtt3cs.dir/MQTTClient.c.o
    [ 55%] Building C object src/CMakeFiles/paho-mqtt3cs.dir/SSLSocket.c.o
    [ 56%] Linking C shared library libpaho-mqtt3cs.so
    [ 56%] Built target paho-mqtt3cs
    Scanning dependencies of target MQTTVersion
    [ 58%] Building C object src/CMakeFiles/MQTTVersion.dir/MQTTVersion.c.o
    [ 59%] Linking C executable MQTTVersion
    [ 59%] Built target MQTTVersion
    Scanning dependencies of target paho-mqtt3as
    [ 60%] Building C object src/CMakeFiles/paho-mqtt3as.dir/MQTTAsync.c.o
    [ 61%] Building C object src/CMakeFiles/paho-mqtt3as.dir/MQTTAsyncUtils.c.o
    [ 62%] Building C object src/CMakeFiles/paho-mqtt3as.dir/SSLSocket.c.o
    [ 63%] Linking C shared library libpaho-mqtt3as.so
    [ 63%] Built target paho-mqtt3as
    Scanning dependencies of target test_connect_destroy
    [ 64%] Building C object test/CMakeFiles/test_connect_destroy.dir/test_connect_destroy.c.o
    [ 65%] Linking C executable test_connect_destroy
    [ 65%] Built target test_connect_destroy
    Scanning dependencies of target test4
    [ 66%] Building C object test/CMakeFiles/test4.dir/test4.c.o
    [ 67%] Linking C executable test4
    [ 67%] Built target test4
    Scanning dependencies of target test1
    [ 67%] Building C object test/CMakeFiles/test1.dir/test1.c.o
    [ 68%] Linking C executable test1
    [ 68%] Built target test1
    Scanning dependencies of target test6
    [ 69%] Building C object test/CMakeFiles/test6.dir/test6.c.o
    [ 70%] Linking C executable test6
    [ 70%] Built target test6
    Scanning dependencies of target test2
    [ 72%] Building C object test/CMakeFiles/test2.dir/test2.c.o
    [ 73%] Linking C executable test2
    [ 73%] Built target test2
    Scanning dependencies of target test11
    [ 74%] Building C object test/CMakeFiles/test11.dir/test11.c.o
    [ 75%] Linking C executable test11
    [ 75%] Built target test11
    Scanning dependencies of target test15
    [ 76%] Building C object test/CMakeFiles/test15.dir/test15.c.o
    [ 77%] Linking C executable test15
    [ 77%] Built target test15
    Scanning dependencies of target thread
    [ 78%] Building C object test/CMakeFiles/thread.dir/thread.c.o
    [ 79%] Building C object test/CMakeFiles/thread.dir/__/src/Thread.c.o
    [ 80%] Linking C executable thread
    [ 80%] Built target thread
    Scanning dependencies of target test45
    [ 81%] Building C object test/CMakeFiles/test45.dir/test45.c.o
    [ 82%] Linking C executable test45
    [ 82%] Built target test45
    Scanning dependencies of target test5
    [ 83%] Building C object test/CMakeFiles/test5.dir/test5.c.o
    [ 84%] Linking C executable test5
    [ 84%] Built target test5
    Scanning dependencies of target test8
    [ 86%] Building C object test/CMakeFiles/test8.dir/test8.c.o
    [ 87%] Linking C executable test8
    [ 87%] Built target test8
    Scanning dependencies of target test3
    [ 88%] Building C object test/CMakeFiles/test3.dir/test3.c.o
    [ 89%] Linking C executable test3
    [ 89%] Built target test3
    Scanning dependencies of target test9
    [ 90%] Building C object test/CMakeFiles/test9.dir/test9.c.o
    [ 91%] Linking C executable test9
    [ 91%] Built target test9
    Scanning dependencies of target test_sync_session_present
    [ 92%] Building C object test/CMakeFiles/test_sync_session_present.dir/test_sync_session_present.c.o
    [ 93%] Linking C executable test_sync_session_present
    [ 93%] Built target test_sync_session_present
    Scanning dependencies of target test95
    [ 94%] Building C object test/CMakeFiles/test95.dir/test95.c.o
    [ 95%] Linking C executable test95
    [ 95%] Built target test95
    Scanning dependencies of target test10
    [ 96%] Building C object test/CMakeFiles/test10.dir/test10.c.o
    [ 97%] Linking C executable test10
    [ 97%] Built target test10
    Scanning dependencies of target test_issue373
    [ 98%] Building C object test/CMakeFiles/test_issue373.dir/test_issue373.c.o
    [100%] Linking C executable test_issue373
    [100%] Built target test_issue373
    [ 24%] Built target common_obj
    [ 27%] Built target paho-mqtt3a
    [ 30%] Built target paho-mqtt3c
    [ 53%] Built target common_ssl_obj
    [ 56%] Built target paho-mqtt3cs
    [ 59%] Built target MQTTVersion
    [ 63%] Built target paho-mqtt3as
    [ 65%] Built target test_connect_destroy
    [ 67%] Built target test4
    [ 68%] Built target test1
    [ 70%] Built target test6
    [ 73%] Built target test2
    [ 75%] Built target test11
    [ 77%] Built target test15
    [ 80%] Built target thread
    [ 82%] Built target test45
    [ 84%] Built target test5
    [ 87%] Built target test8
    [ 89%] Built target test3
    [ 91%] Built target test9
    [ 93%] Built target test_sync_session_present
    [ 95%] Built target test95
    [ 97%] Built target test10
    [100%] Built target test_issue373
    Install the project...
    -- Install configuration: ""
    -- Installing: /usr/local/share/doc/Eclipse Paho C/samples/MQTTAsync_publish.c
    -- Installing: /usr/local/share/doc/Eclipse Paho C/samples/MQTTAsync_publish_time.c
    -- Installing: /usr/local/share/doc/Eclipse Paho C/samples/MQTTAsync_subscribe.c
    -- Installing: /usr/local/share/doc/Eclipse Paho C/samples/MQTTClient_publish.c
    -- Installing: /usr/local/share/doc/Eclipse Paho C/samples/MQTTClient_publish_async.c
    -- Installing: /usr/local/share/doc/Eclipse Paho C/samples/MQTTClient_subscribe.c
    -- Installing: /usr/local/share/doc/Eclipse Paho C/samples/paho_c_pub.c
    -- Installing: /usr/local/share/doc/Eclipse Paho C/samples/paho_c_sub.c
    -- Installing: /usr/local/share/doc/Eclipse Paho C/samples/paho_cs_pub.c
    -- Installing: /usr/local/share/doc/Eclipse Paho C/samples/paho_cs_sub.c
    -- Installing: /usr/local/share/doc/Eclipse Paho C/samples/pubsub_opts.c
    -- Installing: /usr/local/share/doc/Eclipse Paho C/CONTRIBUTING.md
    -- Installing: /usr/local/share/doc/Eclipse Paho C/epl-v20
    -- Installing: /usr/local/share/doc/Eclipse Paho C/edl-v10
    -- Installing: /usr/local/share/doc/Eclipse Paho C/README.md
    -- Installing: /usr/local/share/doc/Eclipse Paho C/notice.html
    -- Installing: /usr/local/lib/libpaho-mqtt3c.so.1.3.8
    -- Installing: /usr/local/lib/libpaho-mqtt3c.so.1
    -- Up-to-date: /usr/local/lib/libpaho-mqtt3c.so
    -- Installing: /usr/local/lib/libpaho-mqtt3a.so.1.3.8
    -- Installing: /usr/local/lib/libpaho-mqtt3a.so.1
    -- Up-to-date: /usr/local/lib/libpaho-mqtt3a.so
    -- Installing: /usr/local/bin/MQTTVersion
    -- Set runtime path of "/usr/local/bin/MQTTVersion" to ""
    -- Installing: /usr/local/include/MQTTAsync.h
    -- Installing: /usr/local/include/MQTTClient.h
    -- Installing: /usr/local/include/MQTTClientPersistence.h
    -- Installing: /usr/local/include/MQTTProperties.h
    -- Installing: /usr/local/include/MQTTReasonCodes.h
    -- Installing: /usr/local/include/MQTTSubscribeOpts.h
    -- Installing: /usr/local/include/MQTTExportDeclarations.h
    -- Installing: /usr/local/lib/libpaho-mqtt3cs.so.1.3.8
    -- Installing: /usr/local/lib/libpaho-mqtt3cs.so.1
    -- Up-to-date: /usr/local/lib/libpaho-mqtt3cs.so
    -- Installing: /usr/local/lib/libpaho-mqtt3as.so.1.3.8
    -- Installing: /usr/local/lib/libpaho-mqtt3as.so.1
    -- Up-to-date: /usr/local/lib/libpaho-mqtt3as.so
    -- Installing: /usr/local/lib/cmake/eclipse-paho-mqtt-c/eclipse-paho-mqtt-cConfig.cmake
    -- Installing: /usr/local/lib/cmake/eclipse-paho-mqtt-c/eclipse-paho-mqtt-cConfig-noconfig.cmake
    -- Installing: /usr/local/lib/cmake/eclipse-paho-mqtt-c/eclipse-paho-mqtt-cConfigVersion.cmake
    Additional mqtt Package version is                   : 1.8.2
    The Fledge required version is                       : >=1.8
    The architecture is set as                           : x86_64
    The package will be built in                         : /home/aj/Development/fledge-pkg/others/archive/DEBIAN/x86_64
    The package name is                                  : fledge-mqtt-1.8.2-x86_64

    Populating the package and updating version file...Done.
    Building the fledge-mqtt-1.8.2-x86_64 package...
    dpkg-deb: building package 'fledge-mqtt' in 'fledge-mqtt-1.8.2-x86_64.deb'.
    Building Complete.
    $
  
The result will be:

.. code-block:: console

    $ ls -la archive/DEBIAN/x86_64/
    total 216
    drwxr-xr-x 4 aj aj   4096 Jan 11 16:44 fledge-mqtt-1.8.2-x86_64
    -rw-r--r-- 1 aj aj 208116 Jan 11 16:44 fledge-mqtt-1.8.2-x86_64.deb
    $

Cleaning the Package Folder
===========================

Use the ``-a`` option to remove all the packages and the files which we used to make the package.
