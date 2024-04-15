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
        """Initialize the Potts_Param object by loading parameters from a YAML file."""
        self.params = load_from_yaml(filename)
        self.initialize_parameters()


    def initialize_parameters(self):
        # load discrete values, values within a range, and compute values with dependencies
        self.load_discrete_values()
        self.load_range_values()
        self.load_values_with_offset()
        

    def load_discrete_values(self):
        # Assuming 'discrete_values' is a key in the YAML's root dictionary
        discrete_values = self.params['discrete_values']
        for key, value in discrete_values.items():
            setattr(self, key, value)

    def load_range_values(self):
        range_values = self.params.get('range', {})
        for key, details in range_values.items():
            if 'base' in details:
                base_value = self._get_attribute_value(details['base'])
                start = base_value[0] + details['start']
                stop = base_value[0] + details['stop']
            else:
                start = details['start']
                stop = details['stop']

            step = details['step']

            # Use np. linspace() when the exact values for the start and end points of your range are the important attributes. 
            # Use np. arange() when the step size between values is more important.
            values = np.arange(start, stop, step)
            setattr(self, key, values)

    def load_values_with_offset(self):
        """Compute values by adding an offset to a base value."""
        offset_values = self.params.get('offset', {})
        for key, details in offset_values.items():
            values = [x + details['offset'] for x in self._get_attribute_value(details['base'])]
            setattr(self, key, values)
    

    def _get_attribute_value(self, key):
        """Retrieve the base value for a given parameter."""
        return getattr(self, key)


if __name__ == "__main__":
    # Path to the YAML configuration file
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, './param_space.yaml')

    params = Potts_Param(filename)

    print(params.hatch)