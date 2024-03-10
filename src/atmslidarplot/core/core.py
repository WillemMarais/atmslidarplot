from enum import Enum


class Wavelength(Enum):
    """The various lidar wavelengths."""

    WL532 = "532nm"
    """532nm wavelength."""
    WL1064 = "1064nm"
    """1064nm wavelength."""

    def to_float(self) -> float:
        match self:
            case Wavelength.WL532:
                return 532e-9
            case Wavelength.WL1064:
                return 1064e-9
            case _:
                raise NotImplementedError


class GV(Enum):
    """Geophysical variable."""

    PARTICULATE_BACKSCATTER = "particulate_backscatter"
    PARTICULATE_OPTICAL_DEPTH = "particulate_optical_depth"
    PARTICULATE_LINEAR_DEPOLARIZATION = "particulate_linear_depolarization"
    PARTICULATE_MOLECULAR_OPTICAL_DEPTH = "particulate_molecular_optical_depth"
    ATTENUATED_COLOR_RATIO_1064NM_532NM = "attenuated_color_ratio_1064nm_532nm"

    PARTICULATE_BACKSCATTER_UNCERTAINTY = "particulate_backscatter_uncertainty"
    PARTICULATE_OPTICAL_DEPTH_UNCERTAINTY = "particulate_optical_depth_uncertainty"
    PARTICULATE_LINEAR_DEPOLARIZATION_UNCERTAINTY = "particulate_linear_depolarization_uncertainty"
    PARTICULATE_MOLECULAR_OPTICAL_DEPTH_UNCERTAINTY = "particulate_molecular_optical_depth_uncertainty"
    ATTENUATED_COLOR_RATIO_1064NM_532NM_UNCERTAINTY = "attenuated_color_ratio_1064nm_532nm_uncertainty"
