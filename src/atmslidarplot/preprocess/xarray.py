import json
import xarray as xr
from jsmin import jsmin

from atmslidarplot.core import GV
from atmslidarplot.config import gv_clip_cfg_fileP

from typing import cast


def __load_gv_clip__(
    gv: GV,
    units: str | None
) -> dict:
    """Load the xarray clip kwargs."""

    with open(gv_clip_cfg_fileP, "r") as file_obj:
        json_str = jsmin(file_obj.read())

        gv_clip_dct = cast(dict, json.loads(json_str)[gv.value])

    if (units is None) or (units not in gv_clip_dct):
        units = "default"

    clip_dct = gv_clip_dct[units]

    return clip_dct


def clip_ds(
    ds: xr.Dataset
) -> xr.Dataset:
    """Clip the geophysical variable within
    specific ranges in the dataset.

    Parameters
    ----------
    ds: xr.Dataset
        The dataset with the geophysical data arrays.

    Returns
    -------
    ds: xr.Dataset
        The updated dataset.
    """

    for gv in list(GV):
        if gv.value in ds.data_vars:
            ds[gv.value] = clip_da(
                ds[gv.value],
                gv
            )

    return ds


def clip_da(
    da: xr.DataArray,
    gv: GV
):
    """Clip the geophysical variable within
    specific ranges.

    Parameters
    ----------
    da: xr.DataArray
        The geophysical data array.
    gv: GV
        The geophysical of interest.

    Returns
    -------
    da: xr.DataArray
        The data array with the set attribute.
    """

    clip_dct = __load_gv_clip__(
        gv, da.attrs.get("units", None)
    )

    return da.clip(**clip_dct)
