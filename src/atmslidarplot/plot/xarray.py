import xarray as xr
import hvplot.xarray

from atmslidarplot import __default_opts__

from typing import Any, Callable


# The list of hvplot plot methods that are supported
__hvplot_methods_str_lst__ = [
    "andrews_curves",
    "area",
    "bar",
    "barh",
    "bivariate",
    "box",
    "errorbars",
    "heatmap",
    "hexbin",
    "hist",
    "kde",
    "labels",
    "lag_plot",
    "line",
    "ohlc",
    "parallel_coordinates",
    "scatter",
    "step",
    "table",
    "violin",
    "polygons",
    "contour",
    "contourf",
    "image",
    "kde",
    "line",
    "quadmesh",
    "rgb",
    "vectorfield",
    "violin"
]


class hvplotWrapper:
    """hvplot wrapper."""

    def __init__(
        self,
        plot_method: Callable,
        call_kwargs: dict,
        opts_kwargs: dict
    ):
        self._plot_method = plot_method
        self._call_kwargs = call_kwargs
        self._opts_kwargs = opts_kwargs

    def __repr__(self) -> str:
        return str(
            {
                "plot_method": self._plot_method,
                "call_kwargs": self._call_kwargs,
                "opts_kwargs": self._opts_kwargs
            }
        )

    def __call__(
        self,
        **kwargs
    ):
        return self._plot_method(
            **self._call_kwargs | kwargs
        ).opts(
            **self._opts_kwargs
        )


@xr.register_dataarray_accessor("lidarplot")
class LidarPlotAccessor:
    def __init__(
        self,
        da: xr.DataArray
    ):
        self.da = da

        self.transform_range_to_km_bl = False
        self.transform_altitude_to_km_bl = False
        self.transform_agl_altitude_to_km_bl = False

        for attr_str in [
            "transform_range_to_km_bl",
            "transform_altitude_to_km_bl",
            "transform_agl_altitude_to_km_bl"
        ]:
            if attr_str in __default_opts__:
                setattr(
                    self,
                    attr_str,
                    __default_opts__[attr_str]
                )

    def _transform_da(self) -> xr.DataArray:
        da = self.da

        if self.transform_range_to_km_bl is True:
            da = da.assign_coords(
                range=1e-3 * da.range
            )
            da.range.attrs |= {
                "units": "km"
            }

        if self.transform_altitude_to_km_bl is True:
            da = da.assign_coords(
                altitude=1e-3 * da.altitude
            )
            da.altitude.attrs |= {
                "units": "km"
            }

        if self.transform_agl_altitude_to_km_bl is True:
            da = da.assign_coords(
                agl_altitude=1e-3 * da.agl_altitude
            )
            da.agl_altitude.attrs |= {
                "units": "km"
            }

        return da

    def _get_default_opts_kwargs(
        self
    ) -> dict:

        if "__hvplot__" not in self.da.attrs:
            return dict()

        if "default" not in self.da.attrs["__hvplot__"]:
            return dict()

        if "opts" not in self.da.attrs["__hvplot__"]["default"]:
            return dict()

        return self.da.attrs["__hvplot__"]["default"]["opts"]

    def _get_opts_kwargs(
        self,
        plot_method_str: str
    ) -> dict:

        opts_kwargs = self._get_default_opts_kwargs()

        if "__hvplot__" not in self.da.attrs:
            return opts_kwargs

        if plot_method_str not in self.da.attrs["__hvplot__"]:
            return opts_kwargs

        if "opts" not in self.da.attrs["__hvplot__"][plot_method_str]:
            return opts_kwargs

        opts_kwargs |= self.da.attrs["__hvplot__"][plot_method_str]["opts"]

        return opts_kwargs

    def _get_default_call_kwargs(
        self
    ) -> dict:

        if "__hvplot__" not in self.da.attrs:
            return dict()

        if "default" not in self.da.attrs["__hvplot__"]:
            return dict()

        if "call" not in self.da.attrs["__hvplot__"]["default"]:
            return dict()

        return self.da.attrs["__hvplot__"]["default"]["call"]

    def _get_call_kwargs(
        self,
        plot_method_str: str
    ) -> dict:

        call_kwargs = self._get_default_call_kwargs()

        if "__hvplot__" not in self.da.attrs:
            return call_kwargs

        if plot_method_str not in self.da.attrs["__hvplot__"]:
            return call_kwargs

        if "call" not in self.da.attrs["__hvplot__"][plot_method_str]:
            return call_kwargs

        call_kwargs |= self.da.attrs["__hvplot__"][plot_method_str]["call"]

        return call_kwargs

    def _plot(
        self,
        plot_method_str: str,
        **kwargs
    ):
        # Do the requested transformations
        da = self._transform_da()

        if plot_method_str == "hvplot":
            plot_method = da.hvplot

        else:
            plot_method = getattr(da.hvplot, plot_method_str)

        # Get the opts kwargs
        opts_kwargs = self._get_opts_kwargs(
            plot_method_str
        )

        # Get the plot kwargs
        call_kwargs = self._get_call_kwargs(
            plot_method_str
        ) | kwargs

        return hvplotWrapper(
            plot_method,
            call_kwargs | kwargs,
            opts_kwargs
        )

    def __getattr__(
        self,
        name_str: str
    ) -> Any:
        if name_str == "hvplot":
            return self.da.hvplot

        elif hasattr(self.da.hvplot, name_str) is True:
            if name_str in __hvplot_methods_str_lst__:
                return self._plot(name_str)
            else:
                return getattr(self.da.hvplot, name_str)

        elif hasattr(self, name_str) is True:
            return getattr(self, name_str)

        else:
            return self

    def __call__(
        self,
        **kwargs
    ):
        return self._plot("hvplot", **kwargs)
