# Web of activities at MU for high-school students

[http://prostredoskolaky.muni.cz/](http://prostredoskolaky.muni.cz)

Developer version is available at
[http://dev.ks.fi.muni.cz](http://dev.ks.fi.muni.cz/).

## Howto build web from repo

 1. Run `make all`.
 2. Serve web from `build` directory.

## Howto update repo from gDrive

 1. Download table of activities into `activities.csv`.
 2. Download folder `web-data` as zip file and unzip it into `static/drive-data`
    folder. The unzip could be done automatically by calling `unzip-web-data.sh`
    script.
 3. Build web according to steps described in previous section.
 4. Commit new static data into repo.

## How it works

Whole web page is basically a static web page with some js. New page is
generated from `csv` input file, which should contain data from Table of
Activities, and html template files located in `templates` directory.

The whole process in maintained by `scr/generator.py` script and `make`.

## How to edit web page

 * `css`, `js`, `static`: edit files in relevant directories, no build is
   required.
 * `html`: edit file in `templates` directory, run `make` on desired file
   or `make all`.

## Tools

 * Bootstrap generated from
   [https://getbootstrap.com/docs/3.3/customize/](https://getbootstrap.com/docs/3.3/customize/).
 * Gridder:
   [https://github.com/oriongunning/gridder](https://github.com/oriongunning/gridder)

## Authors

 * Design: Adela Miklikova
 * Technology & maintenance: Jan Horacek ([me@apophis.cz](mailto:me@apophis.cz))
