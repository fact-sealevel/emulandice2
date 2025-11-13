"""
Logic for the CLI.
"""

import enum
import logging

import click

from emulandice2.emulandice_project import emulandice_project


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class IceSource(enum.Enum):
    GIS = enum.auto()
    AIS = enum.auto()
    GLA = enum.auto()


class Region(enum.Enum):
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
    default=Region.ALL,
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
    "--cyear-start",
    help="Constant rate calculation for projections starts at this year",
    envvar="EMULANDICE2_CYEAR_START",
    default=None,
    type=int,
)
@click.option(
    "--cyear-end",
    help="Constant rate calculation for projections ends at this year",
    envvar="EMULANDICE2_CYEAR_YEAR",
)
@click.option(
    "--no-rebase",
    help="Do not rebase samples to baseyear or regrid time",
    envvar="EMULANDICE2_NO_REBASE",
    default=False,
    type=bool,
)
@click.option("--debug/--no-debug", default=False, envvar="EMULANDICE2_DEBUG")
def main(
    pipeline_id,
    ice_source,
    region,
    emu_file,
    climate_data_file,
    scenario,
    baseyear,
    seed,
    pyear_start,
    pyear_end,
    pyear_step,
    cyear_start,
    cyear_end,
    no_rebase,
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

    emulandice_project(
        pipeline_id,
        ice_source,
        region,
        emu_file,
        climate_data_file,
        scenario,
        baseyear,
        seed,
        pyear_start,
        pyear_end,
        pyear_step,
        cyear_start,
        cyear_end,
        doRebaseSamples=do_rebase,
    )

    logger.info("emulandice2 complete")
