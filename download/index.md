---
layout: default
title: Boomaga - Download
menuItem: Download
---

Ubuntu and Debian
======

Boomaga is available from Ubuntu repositories in older version of Ubuntu and Debian

    sudo apt-get install boomaga

In recent versions of Ubuntu and Debian, boomaga got removed because it lacked Qt6 support. However, Qt6 support has been reinstated in the latest version, and you can install a prebuilt .deb package from [GitHub releases](https://github.com/Boomaga/boomaga/releases/latest).

Alternatively, you can install Boomaga from [our PPA repositories](https://launchpad.net/~boomaga/+archive/ppa), which are available for all modern Ubuntu releases. Open up a terminal and input these commands:

    sudo add-apt-repository ppa:boomaga
    sudo apt-get update
    sudo apt-get install boomaga



Rosa
====
Latest version of Boomaga is available from Rosa repositories and can be installed via Software Center or with this command in a terminal:

    sudo urpmi boomaga


Fedora
======
Boomaga is available from Fedora repositories and can be installed via Software Center or with this command in a terminal:

    sudo dnf install boomaga

Arch
======
You can install boomaga from the AUR with your favorite AUR manager, e.g. `yay`.

    yay -S boomaga

Other distribution
==================
_Please let me know about packages for your distribution._

Source code
===========

Stable release {{ site.program.release.version }}
------------------------------------------------
* [Lates stable version]({{ site.program.release.link }}/v{{ site.program.release.version }}.tar.gz)

Development version
-------------------
Development on Boomaga happens in the [git repository](https://github.com/Boomaga/boomaga). Check out the code by running:

    git clone https://github.com/Boomaga/boomaga.git

Or you can download sourses as [tarball](https://github.com/Boomaga/boomaga/archive/master.tar.gz)

[Full instructions and list of dependencies](https://github.com/Boomaga/boomaga/wiki/Instalation)


<br><br><br><br><br><br><br>
