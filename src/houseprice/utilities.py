"""Utilities used in various parts of the project."""
import matplotlib.pyplot as plt
import yaml

def save_close_plt(path):
    figure = plt.gcf() # get current figure
    figure.set_size_inches(8, 6)
    plt.savefig(path)
    plt.close()
