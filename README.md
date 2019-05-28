# MediaMachinery

## Introduction

This project holds information on how to setup a media downloader,
player and server for contents aiming for TV Series and Movies.
With that, the aim of this project is not to inspire nor to encourage
to piracy in any way.

The end goal is to is to have a NUC running on Linux Ubuntu 18.04
with the following installed on the host:

* [Ubuntu 18.04][UBUNTU1804]
* [Kodi 18.2 (Leia)][KODI]
* [Docker][DOCKER]
* [Docker-Compose][DOCKER-COMPOSE]

And the following shall be run as docker services:

* [Sonarr][SONARR]
* [Radarr][RADARR]
* [Bazarr][BAZARR]
* [Jackett][JACKETT]
* [Emby][EMBY]
* [Portainer][PORTAINER]
* [FileBrowser][FILEBROWSER]

Kodi shall be run upon startup of the machine and used as a media
player.
All the docker services are run in the background. Once the docker
services are started they shall be reached through the web interfaces on
the private network. The purpose of these services is to look for new
TV-Series/Movies that the user is subscribed to. Once found, they are
downloaded and once completed the Kodi (media player) and Emby (media
server) are updated.

## Overview

The flowchart is the complete setup where the blue boxes are services
run as docker containers. The green boxes are services installed on the
host machine.

![Image Flow][MM_FLOW_IMAGE]

### Jackett

Jackett is an indexer that is used for finding media content using
torrent sites.

### Transmission

Transmission is a torrent client that is used to download content from
torrent peers. Completed download of content is stored in a download
folder on the NUC.

### Radarr / Sonarr

These services are used to subscribe to and initiate download of
TV Series (Sonarr) and Movies (Radarr). They both come with a beautiful
web interface where you can search for contents and select which quality
that is preferred to download. If an episode of a show or a movie is not
available, Radarr/Sonarr will download it for you as soon as its made
availble.

Both Radarr and Sonarr uses Jackett as the indexer to find content from
torrent providers and they use Transmission to downloaded content.
Once completed, Radarr/Sonarr moves the downloaded content from the
download directory to a Library Media directory where the content is
categorized and placed into folders so that it can be found and used by
media player and media server.

### Bazarr

This service download subtitles for movies and tv series. It will only
download subtitles for shows/movies that are known by Radarr and/or
Sonarr.

### Emby

Emby is a Media server that can stream Movies or TV series to other
devices than the host its run on. This service read contents from the
Media Library directory. Emby can also be configured to download
subtitles as soon as a TV episode or movie is found.

### Kodi

Kodi is a media player that is used to playback media and display it on
a device (TV in this case) that is connected to the host it is run on.
For this project Kodi is installed on the NUC and the NUC is connected
to a TV via HDMI.

### Portainer

Used as a docker management service that comes with a nice web GUI.
Monitor, check logs, login to your containers via this nice service.

### FileBrowser
Simply used to browse the files of a selected folder (Storage Directory)
to be able to supervise the files.

## Hardware

The server and player used for the purpose of downloading and playing
media is an _INTEL® NUC KIT NUC6CAYH_ of which I found to be perfect
for this purpose. Its small, quiet, quite cheap and yet just enough
powerful for the tasks required. I did complement it with a 2.5" SSD
disk with a capacity of 1 TB, as well as a 4GB DDR3L memory card. The
complete specs are the following:

* [INTEL® NUC KIT NUC6CAYH (BOXNUC6CAYH)][NUC]
* [Crucial 4GB DDR3L-1600 SODIMM (CT51264BF160BJ)][MEMORY]
* [860 QVO SATA III 2.5 inch SSD (MZ-76Q1T0BW)][DISK]

![Image NUC][NUC_IMAGE]

### Setting up Hardware

Installing the disk and Memory card is pretty straight forward. I have
not altered any BIOS settings as I did not find a need of doing so.

## Installations

### Ubuntu 18.04
Create a boot disk of Ubuntu 18.04 on a USB stick and boot from the USB
and follow the installation instructions. Standard installation is fine
for this purpose. The user created is `inzbox`.
For the partition table, I used only one partition for the root (`/`).

#### Additional packages

To be able to connect to the box with SSH, install the following:

    $ sudo apt-get update
    $ sudo apt-get install openssh-server

#### Storage Directory
The storage dir is where all the downloaded content shall be stored as
well as the docker container configuration files. The structure is as
follows:

Create the storage dir:

    inzbox@inzbox-NUC6CAYH:$ sudo mkdir -p /media/storage/docker
    inzbox@inzbox-NUC6CAYH:$ sudo chown -R inzbox:inzbox /media/storage

### Install Docker
Follow the instructions on:
https://docs.docker.com/install/linux/docker-ce/ubuntu/

### Install compose
Follow the instructions on:
https://docs.docker.com/compose/install/

### Install Kodi
follow the instructions on:
https://www.omgubuntu.co.uk/2019/01/install-kodi-on-ubuntu-linux

Copy the GUI settings ([`guisettings.xml`][kodi_guisettings]) of the
kodi where the main interface is changed to only display:

* Movies
* TV shows
* Add-ons
* Videos
* Favourites
* Weather

Also changed is the regional settings to be:

* 24 hour clock
* Dateformat (YYYY-MM-DD)
* Swedish keyboard layout

And enabled web service for user kodi, password kodi on 8080 for
remote control.

#### Setting up Kodi to autostart

Following this thread on kodi.tv:
https://forum.kodi.tv/showthread.php?tid=231955

The user that was created during Ubuntu installation can be used
instead, e.g. `inzbox`.

Restart the box and Kodi shall be automatically started.

#### Add-ons

Once Kodi is started, install the following Add-ons

Subtitles

* OpenSubtitles.org (requires login credentials)
* Addic7ed
* Podnapisi.net
* Subscene

Video:

* SVT Play
* (Unofficial) [Retrospect][Retrospect] (`net.rieter.xot-4.1.7.39.zip`)

Retrospect is used for a lot of play channels of the major Swedish TV
networks. Install it with:
_Add-ons -> Install From Zip file -> Browse to the file..._

Weather

* Yahoo! Weather

## Start docker services

Copy the files from `docker/*` directory to the NUC and put it in
`/media/storage/docker/`.

Login to the NUC with SSH and run the script to start the containers:

    $ /media/storage/docker/mediamachinery.sh start

The services will be reached through these web interfaces:

    Jackett:      http://<IP_OF_NUC>:9117
    Radarr:       http://<IP_OF_NUC>:7878
    Sonarr:       http://<IP_OF_NUC>:8989
    Bazarr:       http://<IP_OF_NUC>:6767
    Emby:         http://<IP_OF_NUC>:8096
    Transmission: http://<IP_OF_NUC>:9091
    FileBrowser:  http://<IP_OF_NUC>:1000
    Portainer:    http://<IP_OF_NUC>:9000


[UBUNTU1804]: http://releases.ubuntu.com/18.04/
[DOCKER]: https://www.docker.com/
[DOCKER-COMPOSE]: https://docs.docker.com/compose/
[KODI]: https://kodi.tv/
[RADARR]: https://radarr.video/
[SONARR]: https://sonarr.tv/
[BAZARR]: https://github.com/morpheus65535/bazarr
[JACKETT]: https://github.com/Jackett/Jackett
[PORTAINER]: https://www.portainer.io/
[EMBY]: https://emby.media/
[FILEBROWSER]: https://github.com/filebrowser/filebrowser
[NUC]: https://www.intel.com/content/www/us/en/products/boards-kits/nuc/kits/nuc6cayh.html
[MEMORY]: https://www.crucial.com/usa/en/ct51264bf160bj
[DISK]: https://www.samsung.com/sg/memory-storage/860-qvo-sata-3-2-5-ssd/MZ-76Q1T0BW/
[NUC_IMAGE]: https://www.intel.com/content/dam/products/hero/foreground/nuc6cays-nuc6cayh-front-angle-16x9.png.rendition.intel.web.320.180.png
[MEM_IMAGE]: https://pics.crucial.com/wcsstore/CrucialSAS/images/resources/medium/package/204-pinsodimmddr3.png
[DISK_IMAGE]: https://images.samsung.com/is/image/samsung/sg-860-qvo-sata-3-2-5-ssd-mz-76q1t0bw-frontblack-128845821?$PD_GALLERY_L_JPG$
[MM_FLOW_IMAGE]: images/mm-flow.png
[Retrospect]: https://www.rieter.net/content/
[kodi_guisettings]: kodi/userdata/guisettings.xml
