# emulandice2

Application projecting sea-level change from muli-model land-ice Gaussian process emulation using Tamsin Edward's [emulandice2](https://github.com/tamsinedwards/emulandice2).

> [!WARNING]
> At the time of writing, this application and Edward's upstream `emulandice2` R library are in early development. Expect bugs and breaking changes.

## Example

First let's create directories for input and output data.

```shell
mkdir -p ./data/input
mkdir -p ./data/output
```

This application can run with input data available online from https://rutgers.app.box.com/v/facts-module-data/file/1449938771233. Download (~170 MB) and uncompress the tarball in the above link into the `./data/input` directory just created.

Now run the container, for example with Docker, like

```shell
docker run --rm \
  -v ./data:/data \
  ghcr.io/fact-sealevel/emulandice2:latest \
  --pipeline-id=1234 \
  --ice-source=GIS \
  --emu-file="/data/input/emu_file/GIS_ALL_CISM_pow_exp_01_EMULATOR.RData" \
  --scenario="ssp585" \
  --climate-data-file="/data/input/emulandice2.ssp585.GrIS2300.temperature.fair.temperature_climate.nc" \
  --pyear-start=2020 \
  --pyear-end=2300 \
  --output-gslr-file="/data/output/gslr.nc"
```

If the run is successful, the output projection will appear in `./data/output`.

> [!TIP]
> For this example we use `ghcr.io/fact-sealevel/emulandice2:latest`. We do not recommend using `latest` for production runs because it is not reproducible. Instead, use a tag for a specific version of the image or an image's digest hash. You can find tagged image versions and digests [here](https://github.com/fact-sealevel/emulandice2/pkgs/container/emulandice2).


## Features

Several options and configurations are available when running the container.

```
Usage: emulandice2 [OPTIONS]

  Application projecting sea-level change from ice following the Gaussian
  process emulators

Options:
  --pipeline-id TEXT              Unique identifier for this instance of the
                                  module.  [required]
  --ice-source [gis|ais|gla]      Ice source: GIS, AIS or GLA  [default: AIS]
  --region [all|rgi01|rgi02|rgi03|rgi04|rgi05|rgi06|rgi07|rgi08|rgi09|rgi10|rgi11|rgi12|rgi13|rgi14|rgi15|rgi16|rgi17|rgi18|rgi19]
                                  Ice source region: ALL for GIS/AIS and
                                  RGI01-RGI19 for GLA  [default: all]
  --emu-file TEXT                 Emulator file  [required]
  --scenario TEXT                 SSP Emissions scenario  [default: ssp245]
  --climate-data-file TEXT        NetCDF4 file containing surface temperature
                                  data  [required]
  --output-gslr-file TEXT         Path to write output global SLR file.
                                  [required]
  --seed INTEGER                  Seed for random number generator  [default:
                                  1234]
  --pyear-start INTEGER           Year for which projections start  [default:
                                  2020]
  --pyear-end INTEGER             Year for which projections end  [default:
                                  2300]
  --pyear-step INTEGER            Step size in years between pyear-start and
                                  pyear-end at which projections are produced
                                  [default: 10]
  --baseyear INTEGER              Base year to which slr projections are
                                  centered  [default: 2005]
  --cyear-start INTEGER           Constant rate calculation for projections
                                  starts at this year
  --cyear-end TEXT                Constant rate calculation for projections
                                  ends at this year
  --no-rebase BOOLEAN             Do not rebase samples to baseyear or regrid
                                  time  [default: False]
  --r-script-path TEXT            Path to R script to launch emulandice2
                                  [required]
  --debug / --no-debug            [default: no-debug]
  --help                          Show this message and exit.
```

See this help by running

```shell
docker run --rm ghcr.io/fact-sealevel/emulandice2:latest --help
```

The various options and configurations can also be set with environment variables prefixed by EMULANDICE2_*. For example, set `--chunksize` with `EMULANDICE2_CHUNKSIZE`.

## Building the container image locally

You can build the container with Docker by cloning the repository and then running

```shell
docker build -t emulandice2:dev .
```

from the repository root.


## Support

Source code is available online at https://github.com/fact-sealevel/emulandice2. This software is open source, available under the MIT license.

Please file issues relating to the CLI Python application in the issue tracker at https://github.com/fact-sealevel/emulandice2/issues.

The R library used by this application is based on Edwards et al. 2021 (https://doi.org/10.1038/s41586-021-03302-y) available at https://github.com/tamsinedwards/emulandice2 under the MIT license.
