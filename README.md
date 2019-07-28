# Web of activities at MU for high-school students

[http://prostredoskolaky.muni.cz/](http://prostredoskolaky.muni.cz)

## Howto build web from repo

 1. Run `make all`.
 2. Serve web from `build` directory.

## Howto update repo from gDrive

 1. Download table of activities into `activities.csv`.
 2. Download table of SOC topics into `soc_topics.csv`.
 3. Download table of SOC garants into `soc_garants.csv`.
 4. Download gDrive folder `web-data` as a zip file and unzip it into
    `static/drive-data` folder. The unzip could be done automatically by
    calling `unzip-web-data.sh` script.
 5. Test it locally (see previous chapter).
 6. Commit new csv files & data, deploy will be done automatically.

## How it works

Whole web page is basically a static web page with some js. New page is
generated from `csv` input files, which should contain data from Table of
Activities and Table of SOC. Template files are located in `templates`
directory.

The whole process in maintained by `scr/*generator.py` scripts and `make`.

## How to edit web page

 * `css`, `js`, `static`: edit files in relevant directories, no build is
   required.
 * `html`: edit files in `templates` directory, run `make` on desired file
   or `make all`.

## Auto-deployment

When pushed to *master* branch of the repository on Github, new changes are
automatically deployed to the production web. Please, do not deploy the web
manually on the production server, you may break auto-deployment.

## Tools

 * Bootstrap generated from
   [https://getbootstrap.com/docs/3.3/customize/](https://getbootstrap.com/docs/3.3/customize/).
 * Gridder:
   [https://github.com/oriongunning/gridder](https://github.com/oriongunning/gridder)

## Authors, contact

 * Primary contact: [prostredoskolaky@fi.muni.cz](mailto:prostredoskolaky@fi.muni.cz)
 * Design: Adela Miklikova
 * Technology: Jan Horacek ([me@apophis.cz](mailto:me@apophis.cz))
