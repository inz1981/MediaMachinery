# MediaMachinery

## Introduction
This project holds information on how to setup a media downloader,
player and server for contents aiming for TV Series and Movies.
With that, the aim of this project is not to inspire nor to encourage
to piracy in any way.

The end goal is to is to have a NUC running on Linux Ubuntu 18.04
with the following installed on the host:

* Ubuntu 18.04
* [Kodi][KODI]
* [Docker][DOCKER]
* [Docker-Compose][DOCKER-COMPOSE]

And the following shall be run as docker instances:

* [Sonarr][SONARR]
* [Radarr][RADARR]
* [Bazarr][BAZARR]
* [Jackett][JACKETT]
* [Emby][EMBY]
* [FileBrowser][FILEBROWSER]

Now, the Kodi shall be run upon startup of the machine.
All the docker services are run in the background. Once the docker
services are started the shall be reached through the web interfaces on
the private network. The purpose of these services is to look for new
TV-Series/Movies that the user is subscribed to. Once found, they are
downloaded and once completed the Kodi (media player) is updated.

## Hardware
The server and player used for the purpose of downloading and playing
media is an INTEL® NUC KIT NUC6CAYH of which I found to be perfect
for this purpose. Its small, quite cheap and yet just enough powerful
for the tasks required. I did complement it with a 2.5" SSD disk with a
capacity of 1 TB, as well as a 4GB DDR memory card. The complete specs
are the following:

* [INTEL® NUC KIT NUC6CAYH (BOXNUC6CAYH)][NUC]
* [Crucial 4GB DDR3L-1600 SODIMM (CT51264BF160BJ)][MEMORY]
* [860 QVO SATA III 2.5 inch SSD (MZ-76Q1T0BW)][DISK]

![Image NUC][NUC_IMAGE]

<img src="https://pics.crucial.com/wcsstore/CrucialSAS/images/resources/medium/package/204-pinsodimmddr3.png" width="300" height="132">
<br>
<img src="https://images.samsung.com/is/image/samsung/sg-860-qvo-sata-3-2-5-ssd-mz-76q1t0bw-frontblack-128845821?$PD_GALLERY_L_JPG$" width="300" height="220">

### Setting up Hardware



[DOCKER]: https://www.docker.com/
[DOCKER-COMPOSE]: https://docs.docker.com/compose/
[KODI]: https://kodi.tv/
[RADARR]: https://radarr.video/
[SONARR]: https://sonarr.tv/
[BAZARR]: https://github.com/morpheus65535/bazarr
[JACKETT]: https://github.com/Jackett/Jackett
[EMBY]: https://emby.media/
[FILEBROWSER]: https://github.com/filebrowser/filebrowser
[NUC]: https://www.intel.com/content/www/us/en/products/boards-kits/nuc/kits/nuc6cayh.html
[MEMORY]: https://www.crucial.com/usa/en/ct51264bf160bj
[DISK]: https://www.samsung.com/sg/memory-storage/860-qvo-sata-3-2-5-ssd/MZ-76Q1T0BW/
[NUC_IMAGE]: https://www.intel.com/content/dam/products/hero/foreground/nuc6cays-nuc6cayh-front-angle-16x9.png.rendition.intel.web.320.180.png
[MEM_IMAGE]: https://pics.crucial.com/wcsstore/CrucialSAS/images/resources/medium/package/204-pinsodimmddr3.png
[DISK_IMAGE]: https://images.samsung.com/is/image/samsung/sg-860-qvo-sata-3-2-5-ssd-mz-76q1t0bw-frontblack-128845821?$PD_GALLERY_L_JPG$
