import numpy as np
import pandas as pd

from pandas.api.types import is_numeric_dtype
from scipy.interpolate import interpn

def MultiInterp(df, x):
    """
    Interpolates over a 1D or 2D grid on a pandas DataFrame.

    Args:
    data: A pandas Series / DataFrame containing the interpolation data.
    x: A 1D or 2D array containing the columns to interpolate at.

    Returns:
    f: The interpolated value(s) corresponding to the input points.
    """
    
    if isinstance(df, pd.Series):
        if np.ndim(x) == 1 and is_numeric_dtype(df.index):
            xp = df.index.values
            f = interpn((xp,), df.values, x)
        else:
            raise ValueError('x must be a 1D array with numeric indexes for 1D interpolation.')
    elif isinstance(df, pd.DataFrame):
        if np.ndim(x) == 2 and x.shape[1] == 2 and is_numeric_dtype(df.index) and is_numeric_dtype(df.columns):
            xp = df.index.values
            yp = df.columns.values
            f = interpn((xp, yp), df.values, x)
        else:
            raise ValueError('x must be a 2D array of 2 columns with numeric indexes and columns for 2D interpolation.')
    else:
        raise ValueError('df must be a pandas DataFrame or Series')
    return f