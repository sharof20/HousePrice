"""Utilities used in various parts of the project."""
import matplotlib.pyplot as plt
import yaml

def save_close_plt(path):
    figure = plt.gcf() # get current figure
    figure.set_size_inches(8, 6)
    plt.savefig(path)
    plt.close()

def read_yaml(path):
    """Read a YAML file.

    Args:
        path (str or pathlib.Path): Path to file.

    Returns:
        dict: The parsed YAML file.

    """
    with open(path) as stream:
        try:
            out = yaml.safe_load(stream)
        except yaml.YAMLError as error:
            info = (
                "The YAML file could not be loaded. Please check that the path points "
                "to a valid YAML file."
            )
            raise ValueError(info) from error
    return out
