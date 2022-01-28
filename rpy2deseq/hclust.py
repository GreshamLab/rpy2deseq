from rpy2deseq.rpy2utils import _importr, _r_to_list, _r_to_numpy, _pandas_to_r, _numpy_to_r
import numpy as _np
import pandas as _pd
    
_stats = _importr('stats')
_hclust_converts = {'merge': _r_to_numpy,
                    'height': _r_to_list,
                    'order': lambda x: _np.array(_r_to_list(x)),
                    'labels': lambda x: _np.array(_r_to_list(x)),
                    'method': _r_to_list,
                    'call': _r_to_list,
                    'dist.method': _r_to_list}

def hclust(mat, method="euclidean"):
    if isinstance(mat, _pd.DataFrame):
        rmat = _pandas_to_r(mat, as_matrix=True)
    else:
        rmat = _numpy_to_r(mat)

    hclust_obj = _stats.hclust(_stats.dist(rmat, method=method))
    hclust_obj = {k: _hclust_converts[k](v) for k, v in zip(hclust_obj.names, hclust_obj)}
    hclust_obj['labels'] = _np.array(mat.index.tolist())
    return hclust_obj
