# -*- coding: utf-8 -*-

"""Visualization functions"""

import numpy as np
import matplotlib.pyplot as plt
from munging.ctl_utils import nano_to_sec


def plot_durations(durs, label="Duration (minutes)", tmin=None, tmax=None, title=None, ax=None):
    """Utility to plot a histogram of duration values.
    """
    durs_in_sec = nano_to_sec(np.asarray(durs.dropna(), dtype='float'))
    if ax is not None:
        a = ax
    else:
        f, a = plt.subplots()

    if tmin is None:
        tmin = 0.
    tmax = tmax or 240 * 60.

    a.hist(durs_in_sec, bins=np.linspace(tmin, tmax, 100))
    a.set_xlabel(label)
    a.set_ylabel("Count")
    a.set_xlim((tmin, tmax))
    a.set_xticklabels(map(lambda x: int(x / 60), a.get_xticks()))
    if title:
        a.set_title(title)
    return a
