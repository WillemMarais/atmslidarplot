import json
import xarray as xr
from jsmin import jsmin

from atmslidarplot.core import GV
from atmslidarplot.config import gv_metadata_cfg_fileP

from typing import Literal


def __load_gv_metadata__(
    gv: GV,
    range_unit: Literal["m", "km"],
    time_axis: Literal["raw_time", "time"],
    range_axis: Literal["raw_range", "range", "altitude", "agl_altitude"]
) -> dict:
    """Load the metadata config."""

    with open(gv_metadata_cfg_fileP, "r") as file_obj:
        json_str = jsmin(file_obj.read())

        for trgt_str, rplc_str in zip(
            ["range_unit", "time_axis", "range_axis"],
            [range_unit, time_axis, range_axis]
        ):
            json_str = json_str.replace(
                "{" + f"{trgt_str}" + "}",
                rplc_str
            )

        gv_metadata_dct = json.loads(json_str)[gv.value]

    return gv_metadata_dct


def embellish_attr_ds(
    ds: xr.Dataset,
    range_unit: Literal["m", "km"],
    time_axis: Literal["raw_time", "time"],
    range_axis: Literal["raw_range", "range", "altitude", "agl_altitude"]
) -> xr.Dataset:
    """Embellish the attributes of geophysical
    data arrays.

    Parameters
    ----------
    ds: xr.Dataset
        The dataset with the geophysical data arrays.
    range_unit: Literal["m", "km"]
        The range axis unit.
    time_axis: Literal["raw_time", "time"]
        The time axis name.
    range_axis: Literal["raw_range", "range", "altitude", "agl_altitude"]
        The range axis name.

    Returns
    -------
    ds: xr.Dataset
        The updated dataset.
    """

    for gv in list(GV):
        if gv.value in ds.data_vars:
            ds[gv.value] = embellish_attr_da(
                ds[gv.value],
                gv,
                range_unit,
                time_axis,
                range_axis
            )

    return ds


def embellish_attr_da(
    da: xr.DataArray,
    gv: GV,
    range_unit: Literal["m", "km"],
    time_axis: Literal["raw_time", "time"],
    range_axis: Literal["raw_range", "range", "altitude", "agl_altitude"]
) -> xr.DataArray:
    """Embellish the attribute of xarray
    data array.

    Parameters
    ----------
    da: xr.DataArray
        The geophysical data array.
    gv: GV
        The geophysical of interest.
    range_unit: Literal["m", "km"]
        The range axis unit.
    time_axis: Literal["raw_time", "time"]
        The time axis name.
    range_axis: Literal["raw_range", "range", "altitude", "agl_altitude"]
        The range axis name.

    Returns
    -------
    da: xr.DataArray
        The data array with the set attribute.
    """

    # Load the metadata config
    gv_metadata_dct = __load_gv_metadata__(
        gv,
        range_unit,
        time_axis,
        range_axis
    )

    # Set the data array attribute
    da.attrs |= gv_metadata_dct

    return da
