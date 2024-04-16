import os
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


def load_from_yaml(filename: str) -> Dict[str, Any]:
    with open(filename, "r") as file:
        return yaml.safe_load(file)


class Potts_Param:

    def __init__(self, filename: str):
        """
        The Potts_Param object prepare all necessary simulation parameters
        for a Potts model kinetic Monte Carlo simulation.
        """
        self.params = load_from_yaml(filename)
        self.initialize_parameters()

    def initialize_parameters(self):
        """
        Initializes simulation parameters by loading different types of values.

        load_discrete_values(): Handles loading of simple key-value pairs from configuration.
        load_range_values(): Handles loading and calculation of ranged parameters.
        load_values_with_offset(): Handles calculation of parameters based on other,
                                   previously loaded parameters with additional offsets.
        """
        self.load_discrete_values()
        self.load_range_values()
        self.load_values_with_offset()

    def load_discrete_values(self):
        """
        Loads discrete values directly from the configuration.
        These are standalone parameters that do not depend on other parameters.
        """
        # Assuming 'discrete_values' is a key in the YAML's root dictionary
        discrete_values = self.params["discrete_values"]
        for key, value in discrete_values.items():
            setattr(self, key, value)

    def load_range_values(self):
        """
        Loads continuous range values specified by start, stop, and step values
        They may depend on other parameters, defined by 'base'.
        """
        range_values = self.params.get("range", {})
        for key, details in range_values.items():
            if "base" in details:
                base_value = self._get_attribute_value(details["base"])

                start = base_value[0] + details["start"]
                stop = base_value[0] + details["stop"]
            else:
                start = details["start"]
                stop = details["stop"]

            step = details["step"]

            # Use np. linspace() when the exact values for the start and end points of your range are the important attributes.
            # Use np. arange() when the step size between values is more important.
            values = np.arange(start, stop, step)
            setattr(self, key, values)

    def load_values_with_offset(self):
        """Compute values by adding an offset to a base value."""
        offset_values = self.params.get("offset", {})
        for key, details in offset_values.items():
            base_value = self._get_attribute_value(details["base"])
            offset = details.get("offset")

            values = [x + offset for x in base_value]
            setattr(self, key, values)


    def _get_attribute_value(self, key):
        """
        Retrieve the value for a given parameter.
        Raise an error if value not found.
        """
        try:
            value = getattr(self, key)
            if value is not None:
                return value
            else:
                raise AttributeError(f"Attribute {key} is None.")
        except AttributeError:
            raise ValueError(
                f"Required attribute '{key}' not found in class attributes."
            )

    def print_attributes(self):
        """Prints all attributes of the instance in a nicely formatted manner."""
        print("Potts_Param Attributes:")
        for attr, value in sorted(vars(self).items()):
            print(f"{attr}: {value}")


if __name__ == "__main__":
    # Path to the YAML configuration file
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, "./param_space.yaml")

    params = Potts_Param(filename)

    params.print_attributes()
