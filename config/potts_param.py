import numpy as np
import yaml
from typing import List, Dict, Any

"""
    Load configuration parameters for a Potts kMC simulation.

    This class handles the calculation of parameters based on a YAML
    configuration file. It supports direct ranges, dependent ranges based on other
    parameters, and offsets added to existing parameters.

    See also https://spparks.github.io/doc/app_am_ellipsoid.html
"""

class Potts_Param:

    def __init__(self, filename: str):
        """Initialize the Potts_Param object by loading parameters from a YAML file."""
        self.params = self.load_from_yaml(filename)
        self.initialize_parameters()


    def load_from_yaml(self, filename: str) -> Dict[str, Any]:
        try:
            with open(filename, "r") as file:
                return yaml.safe_load(file)
        except (FileNotFoundError, IOError, yaml.YAMLError) as e:
            print(f"Error with file '{filename}': {e}")
            raise

    def _compute_range(self, param_dict: dict) -> List[float]:
        """Compute a range based on a parameter dictionary."""
        start = param_dict["start"]
        stop = param_dict["stop"]
        step = param_dict["step"]
        return np.arange(start, stop, step)

    def _base_value(self, key: str) -> List[float]:
        """Retrieve the base value for a given parameter."""
        return getattr(self, key)

    def _compute_range_with_base(self, key: str) -> List[float]:
        """Compute range considering a base value."""
        base_value = self._base_value(self.params[key]["base"])[0]
        return self._compute_range(
            {
                **self.params[key],
                "start": base_value + self.params[key]["start_offset"],
                "stop": base_value + self.params[key]["stop_offset"],
            }
        )

    def _compute_with_offset(self, base_key: str, offset: int) -> List[float]:
        """Compute values by adding an offset to a base value."""
        return [x + offset for x in self._base_value(base_key)]

    def initialize_parameters(self):
        """Initialize parameters including direct and derived parameters."""
        self.init_direct_parameters()
        self.init_derived_parameters()

    def init_direct_parameters(self):
        """Initialize direct parameters from YAML data."""
        self.v_scan = self._compute_range(self.params["v_scan"])
        self.hatch = self.params["hatch"]
        self.starting_pos = self.params["starting_pos"]
        self.heading = self.params["heading"]

    def load_parameters(self):
        # Direct parameters
        self.hatch = self.params["hatch"]
        self.starting_pos = self.params["starting_pos"]
        self.heading = self.params["heading"]

        self.v_scan = self._compute_range(self.params["v_scan"])
        self.melt_tail_length = self._compute_range(self.params["melt_tail_length"])
        self.melt_depth = self._compute_range(self.params["melt_depth"])
        self.cap_height = self._compute_range(self.params["cap_height"])

        self.exp_factor = self.params["exp_factor"]

        # Derived parameters
        self.spot_width = self._compute_range_with_base("spot_width")
        self.HAZ_width = self._compute_range_with_base("HAZ_width")

        self.HAZ_tail = self._compute_with_offset(
            "melt_tail_length", self.params["HAZ_tail"]["offset"]
        )
        self.depth_HAZ = self._compute_with_offset(
            "melt_depth", self.params["depth_HAZ"]["offset"]
        )
        self.cap_HAZ = self._compute_with_offset(
            "cap_height", self.params["cap_HAZ"]["offset"]
        )
