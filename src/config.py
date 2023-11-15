import os
import pathlib

import yaml

CONFIGFILE = "config.yaml"
FILEPATH = os.path.join(pathlib.Path(__file__).parent, CONFIGFILE)


def get(option: str):
    """
    Get the value of the configuration option.

    Usage examples:
    >>> get('myoption')
    >>> get('mysection.mysubsection.myoption')

    :param option: Single option or dot-separated path to option.
    :returns: The value of the option.

    """
    with open(FILEPATH) as file:
        config = yaml.safe_load(file)
        keys = option.split(".")
        for key in keys:
            config = config[key]
        return config
