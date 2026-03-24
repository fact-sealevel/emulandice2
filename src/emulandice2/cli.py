"""
Logic for the CLI.
"""

from emulandice2.emulandice_postprocess import emulandice_postprocess

import enum
import logging

import click
from pathlib import Path
import tempfile

from emulandice2.emulandice_project import emulandice_project


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class IceSource(enum.StrEnum):
    GIS = enum.auto()
    AIS = enum.auto()
    GLA = enum.auto()


class Region(enum.StrEnum):
    ALL = enum.auto()
    RGI01 = enum.auto()
    RGI02 = enum.auto()
    RGI03 = enum.auto()
    RGI04 = enum.auto()
    RGI05 = enum.auto()
    RGI06 = enum.auto()
    RGI07 = enum.auto()
    RGI08 = enum.auto()
    RGI09 = enum.auto()
    RGI10 = enum.auto()
    RGI11 = enum.auto()
    RGI12 = enum.auto()
    RGI13 = enum.auto()
    RGI14 = enum.auto()
    RGI15 = enum.auto()
    RGI16 = enum.auto()
    RGI17 = enum.auto()
    RGI18 = enum.auto()
    RGI19 = enum.auto()


@click.command(context_settings={"show_default": True})
@click.option(
    "--pipeline-id",
    envvar="EMULANDICE2_PIPELINE_ID",
    help="Unique identifier for this instance of the module.",
    required=True,
)
@click.option(
    "--ice-source",
    help="Ice source: GIS, AIS or GLA",
    default=IceSource.AIS,
    envvar="EMULANDICE2_ICE_SOURCE",
    type=click.Choice(IceSource, case_sensitive=False),
)
@click.option(
    "--region",
    help="Ice source region: ALL for GIS/AIS and RGI01-RGI19 for GLA",
    envvar="EMULANDICE2_REGIONS",
    multiple=True,
    default=[Region.ALL],
    type=click.Choice(Region, case_sensitive=False),
)
@click.option(
    "--emu-file",
    help="Emulator file",
    envvar="EMULANDICE2_EMU_FILES",
    multiple=True,
    required=True,
)
@click.option(
    "--scenario",
    help="SSP Emissions scenario",
    envvar="EMULANDICE2_SCENARIO",
    default="ssp245",
)
@click.option(
    "--climate-data-file",
    help="NetCDF4 file containing surface temperature data",
    envvar="EMULANDICE2_CLIMATE_DATA_FILE",
    required=True,
)
@click.option(
    "--output-gslr-file",
    envvar="EMULANDICE2_OUTPUT_GSLR_FILE",
    help="Path to write output global SLR file.",
    required=True,
    type=str,
)
@click.option(
    "--output-lslr-file",
    envvar="EMULANDICE2_OUTPUT_LSLR_FILE",
    help="Path to write output local SLR file.",
    required=True,
    type=str,
)
@click.option(
    "--seed",
    help="Seed for random number generator",
    envvar="EMULANDICE2_SEED",
    default=1234,
    type=int,
)
@click.option(
    "--pyear-start",
    help="Year for which projections start",
    envvar="EMULANDICE2_PYEAR_START",
    default=2020,
    type=int,
)
@click.option(
    "--pyear-end",
    help="Year for which projections end",
    envvar="EMULANDICE2_PYEAR_END",
    default=2300,
    type=int,
)
@click.option(
    "--pyear-step",
    help="Step size in years between pyear-start and pyear-end at which projections are produced",
    envvar="EMULANDICE2_PYEAR_STEP",
    default=10,
    type=int,
)
@click.option(
    "--baseyear",
    help="Base year to which slr projections are centered",
    type=int,
    default=2005,
    envvar="EMULANDICE2_BASE_YEAR",
)
@click.option(
    "--chunksize",
    envvar="EMULANDICE2_CHUNKSIZE",
    help="Number of locations to process at a time [default=50].",
    default=50,
)
@click.option(
    "--location-file",
    envvar="EMULANDICE2_LOCATION_FILE",
    help="File containing name, id, lat, and lon of points for localization.",
    type=str,
    required=True,
)
@click.option(
    "--grdfingerprintfile",
    envvar="EMULANDICE2_GRDFINGERPRINTFILE",
    help="YAML file that contains the fingerprints for each region.",
    type=str,
    required=True,
)
@click.option(
    "--fingerprint-dir",
    envvar="EMULANDICE2_FINGERPRINT_DIR",
    help="Path to directory containing fprint files.",
    type=str,
    required=True,
)
@click.option(
    "--cyear-start",
    help="Constant rate calculation for projections starts at this year",
    envvar="EMULANDICE2_CYEAR_START",
    default=None,
    type=int,
)
@click.option(
    "--cyear-end",
    help="Constant rate calculation for projections ends at this year",
    envvar="EMULANDICE2_CYEAR_END",
)
@click.option(
    "--no-rebase",
    help="Do not rebase samples to baseyear or regrid time",
    envvar="EMULANDICE2_NO_REBASE",
    default=False,
    type=bool,
)
@click.option(
    "--r-script-path",
    help="Path to R script to launch emulandice2",
    type=str,
    required=True,
    envvar="EMULANDICE2_R_SCRIPT_PATH",
)
@click.option("--debug/--no-debug", default=False, envvar="EMULANDICE2_DEBUG")
def main(
    pipeline_id,
    ice_source,
    region,
    emu_file,
    climate_data_file,
    output_gslr_file,
    output_lslr_file,
    scenario,
    baseyear,
    chunksize,
    location_file,
    grdfingerprintfile,
    fingerprint_dir,
    seed,
    pyear_start,
    pyear_end,
    pyear_step,
    cyear_start,
    cyear_end,
    no_rebase,
    r_script_path,
    debug,
) -> None:
    """
    Application projecting sea-level change from ice following the Gaussian process emulators
    """
    if debug:
        logging.root.setLevel(logging.DEBUG)
    else:
        logging.root.setLevel(logging.INFO)

    logger.info("Starting emulandice2")

    do_rebase = not no_rebase

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        emulandice2_r_output_dir = tmpdir / "results"
        emulandice2_r_output_dir.mkdir(parents=True, exist_ok=True)

        r_projected_paths = emulandice_project(
            pipeline_id,
            ice_source,
            region,
            emu_file,
            climate_data_file,
            output_gslr_file,
            emulandice2_r_output_dir,
            scenario,
            baseyear,
            seed,
            pyear_start,
            pyear_end,
            pyear_step,
            cyear_start,
            cyear_end,
            doRebaseSamples=do_rebase,
            r_script_path=r_script_path,
        )

        # Takes R output files as input so need to run postprocessing before tmp
        # working dir gets cleaned up.
        emulandice_postprocess(
            locationfile=location_file,
            chunksize=chunksize,
            pipeline_id=pipeline_id,
            ncfiles=r_projected_paths,
            grdfingerprintfile=grdfingerprintfile,
            fingerprint_dir=fingerprint_dir,
            scenario=scenario,
            baseyear=baseyear,
            output_lslr_file=output_lslr_file,
        )

    logger.info("emulandice2 complete")
