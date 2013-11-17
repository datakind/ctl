# -*- coding: utf-8 -*-

"""Processing data"""

import numpy as np
import pandas as pd
from collections import OrderedDict


def pctile_of(series, Npctiles=10):
    """Return a series with category labels for quantile breakdowns of
    values.
    """
    series = series.dropna()
    series.sort()
    sorted_index = series.index
    N = len(sorted_index)
    return pd.Series(np.asarray(np.arange(N) / (float(N) / Npctiles), 'int'),
                     index=sorted_index)


def group_summary(group, field='duration_to_first_resp_nonneg'):
    """Summarize a field value per group.
    """
    ratings = group.conv_rating
    dur = group[field]
    out = OrderedDict()
    out['dur_min_minutes'] = dur.min() / (10 ** 9) / 60
    out['dur_max_minutes'] = dur.max() / (10 ** 9) / 60
    out['rating_mean'] = ratings.mean()
    out['count'] = len(group)
    return pd.Series(out)
