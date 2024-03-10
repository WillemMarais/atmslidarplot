__default_opts__ = {
    "transform_range_to_km_bl": False,
    "transform_altitude_to_km_bl": False,
    "transform_agl_altitude_to_km_bl": False
}


def opts(**kwargs):
    """Global options.

    Parameters
    ----------
    transform_range_to_km_bl: bool
        Transform range coordinates to kilometer.
    transform_altitude_to_km_bl: bool
        Transform altitude coordinates to kilometer.
    transform_agl_altitude_to_km_bl: bool
        Transform AGL altitude coordinates to kilometer.
    """

    for key, val in kwargs.items():
        if key in __default_opts__:
            __default_opts__[key] = val


def set_default_hvplot_opts():
    """Set default holoview options."""

    import holoviews as hv

    hv.config.image_rtol = 10
    hv.opts.defaults(hv.opts.Image(active_tools=["box_zoom"]))
    hv.opts.defaults(hv.opts.QuadMesh(active_tools=["box_zoom"]))
    hv.opts.defaults(hv.opts.Curve(active_tools=["box_zoom"], show_grid=True))
    hv.opts.defaults(hv.opts.Scatter(active_tools=["box_zoom"], show_grid=True))
