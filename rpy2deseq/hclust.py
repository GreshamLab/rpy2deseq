from rpy2deseq.rpy2utils import (
    _importr,
    _r_to_list,
    _r_to_numpy,
    _pandas_to_r,
    _numpy_to_r
)

import numpy as _np
import pandas as _pd

# Import stats
_stats = _importr('stats')
_hclust_converts = {
    'merge': _r_to_numpy,
    'height': _r_to_list,
    'order': lambda x: _np.array(_r_to_list(x)),
    'labels': lambda x: _np.array(_r_to_list(x)),
    'method': _r_to_list,
    'call': _r_to_list,
    'dist.method': _r_to_list
}

def hclust(mat, method="euclidean"):
    """
    Call R hclust on a DataFrame or numpy array

    :param mat: Data for clustering
    :type mat: pd.DataFrame, np.ndarray
    :param method: Distance metric, defaults to "euclidean"
    :type method: str, optional
    :return: Dict of hclust return values converted to
        python objects
    :rtype: dict
    """

    # Convert matrix to an R object
    if isinstance(mat, _pd.DataFrame):
        rmat = _pandas_to_r(mat, as_matrix=True)
        mat_labels = mat.index.tolist()
    else:
        rmat = _numpy_to_r(mat)
        mat_labels = None

    # Run hclust
    hclust_obj = _stats.hclust(
        _stats.dist(rmat, method=method)
    )

    # Convert returned object to a dict of python objects
    hclust_obj = {
        k: _hclust_converts[k](v)
        for k, v in zip(hclust_obj.names, hclust_obj)
    }

    # Add labels from dataframe if it was a dataframe

    if mat_labels is not None:
        hclust_obj['labels'] = mat_labels

    return hclust_obj
